from flask import Flask, request, jsonify, render_template
import cv2
import face_recognition
import numpy as np
import os
import csv
import sqlite3
import base64
from datetime import datetime
import pickle  # For saving and loading encodings
from PIL import Image  # FIX 1: Import missing module
import io  # FIX 1: Import missing module

app = Flask(__name__)

# Configuration
TRAINING_IMAGES_FOLDER = 'training_images'
os.makedirs(TRAINING_IMAGES_FOLDER, exist_ok=True)
DB_FILE = 'attendance.db'
ATTENDANCE_FILE = 'attendance.csv'
ENCODINGS_FILE = 'encodings.pkl'  # File to store face encodings

# Helper function to get a database connection
def get_db_connection():
    conn = sqlite3.connect("attendance.db")
    conn.row_factory = sqlite3.Row
    return conn

# Initialize the database
def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL UNIQUE,
                            image_path TEXT NOT NULL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS recognised_faces (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            student_id INTEGER NOT NULL,
                            date DATETIME DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (student_id) REFERENCES students (student_id))''')
        conn.commit()

init_db()
def load_or_generate_encodings():
    if os.path.exists(ENCODINGS_FILE):
        with open(ENCODINGS_FILE, 'rb') as f:
            data = pickle.load(f)
            encode_list_known = data['encodings']
            names = data['names']
    else:
        encode_list_known = []
        names = []
        for image_name in os.listdir(TRAINING_IMAGES_FOLDER):
            image_path = os.path.join(TRAINING_IMAGES_FOLDER, image_name)
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)
            if face_encodings:
                encoding = face_encodings[0]  # Take the first face encoding found
                encode_list_known.append(encoding)
                
                # Get the student name from the database using the student_id
                student_id = image_name.split('.')[0]
                with get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM students WHERE student_id = ?", (student_id,))
                    student = cursor.fetchone()
                    if student:
                        names.append(student["name"])
                    else:
                        names.append(student_id)  # Fallback to student_id if name not found

        # Save the encodings and names to a file for future use
        with open(ENCODINGS_FILE, 'wb') as f:
            pickle.dump({'encodings': encode_list_known, 'names': names}, f)

    return encode_list_known, names

# Routes
@app.route('/')
def serve_login():
    return render_template('login.html')

@app.route('/dashboard')
def serve_dashboard():
    return render_template('dashboard.html')

@app.route('/add_attendance')
def serve_add_attendance():
    return render_template('add_attendance.html')

@app.route('/mark_attendance')
def serve_mark_attendance():
    return render_template('mark_attendance.html')

@app.route('/save_student', methods=['POST'])
def save_student():
    try:
        data = request.json
        student_id = data.get('student_id')
        name = data.get('name')
        image_data = data.get('image')

        if not image_data.startswith("data:image/jpeg;base64,"):
            image_data = image_data.replace("data:image/png;base64,", "")

        if not student_id or not name or not image_data:
            return jsonify({'error': 'All fields are required!'}), 400

        image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        image_filename = f"{student_id}.jpg"
        image_path = os.path.join(TRAINING_IMAGES_FOLDER, image_filename)
        
        with open(image_path, 'wb') as image_file:
            image_file.write(image_bytes)

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO students (student_id, name, image_path) VALUES (?, ?, ?)',
                           (student_id, name, image_path))
            conn.commit()

        # **Force encoding update**
        global encode_list_known, names  # Ensure we update the in-memory variables
        encode_list_known, names = load_or_generate_encodings()

        return jsonify({'message': f"Student '{name}' added successfully!"})
    
    except sqlite3.IntegrityError:
        return jsonify({'error': f"Student with ID '{student_id}' already exists!"}), 400
    except Exception as e:
        return jsonify({'error': f'Failed to save student details: {str(e)}'}), 500


@app.route('/students', methods=['GET'])
def get_students():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT student_id, name FROM students')
        students = [{'student_id': row['student_id'], 'name': row['name']} for row in cursor.fetchall()]
    return jsonify(students)
@app.route('/delete_student/<int:id>', methods=['DELETE'])
def delete_student(id):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT image_path FROM students WHERE student_id = ?', (id,))
            row = cursor.fetchone()
            if row:
                os.remove(row['image_path'])
                cursor.execute('DELETE FROM students WHERE student_id = ?', (id,))
                conn.commit()

                # Regenerate encodings after deleting a student
                load_or_generate_encodings()

                return jsonify({'message': f"Student {id} deleted successfully!"})
            else:
                return jsonify({'error': 'Student not found!'}), 404
    except Exception as e:
        return jsonify({'error': 'Failed to delete student'}), 500

# Route for performing face recognition
@app.route('/recognize_face', methods=['POST'])
def recognize_face():
     try:
         data = request.json
         image_data = data.get('image')
         if not image_data:
             return jsonify({'error': 'No image data received'}), 400
         image_data = base64.b64decode(image_data.split(',')[1])
         np_arr = np.frombuffer(image_data, np.uint8)
         frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
         face_locations = face_recognition.face_locations(rgb_frame)
         face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
         encode_list_known, names = load_or_generate_encodings()  # FIX 3: Correct unpacking
         recognized_faces = []
         for face_encoding in face_encodings:
             matches = face_recognition.compare_faces(encode_list_known, face_encoding, tolerance=0.5)
             name = "Unknown"
             if True in matches:
                    match_indices = np.where(matches)[0]  # Get all indices where match is True
                    match_index = match_indices[0]  # Pick the first match
                    name = names[match_index]

                    with get_db_connection() as conn:
                     cursor = conn.cursor()
                     cursor.execute('INSERT INTO recognised_faces (name) VALUES (?)', (name,))
                     conn.commit()
                    mark_attendance(name)  # FIX 5: Ensure this function handles errors properly
             recognized_faces.append({'name': name})
         return jsonify({'recognized_faces': recognized_faces})
     except Exception as e:
         return jsonify({'error': f'Failed to recognize face: {str(e)}'}), 500

# Route for fetching recognized faces
@app.route('/recognized_faces', methods=['GET'])
def recognized_faces():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT name, timestamp FROM recognised_faces')
            recognized_faces = [{'name': row['name'], 'timestamp': row['timestamp']} for row in cursor.fetchall()]
        return jsonify({'recognized_faces': recognized_faces})
    except Exception as e:
        return jsonify({'error': 'Failed to fetch recognized faces'}), 500

def mark_attendance(name):
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d")

    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Check if student exists
        cursor.execute("SELECT student_id FROM students WHERE name = ?", (name,))
        student = cursor.fetchone()
        
        if student:
            student_id = student["student_id"]
            
            # Check if already marked today
            cursor.execute("SELECT * FROM attendance WHERE student_id = ? AND date = ?", (student_id, date_string))
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO attendance (student_id, date) VALUES (?, ?)", (student_id, date_string))
                conn.commit()
@app.route('/get_attendance', methods=['GET'])
def get_attendance():
    today = datetime.now().strftime("%Y-%m-%d")
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.student_id, s.name, 
                   CASE WHEN a.date IS NOT NULL THEN 1 ELSE 0 END as present
            FROM students s 
            LEFT JOIN attendance a ON s.student_id = a.student_id AND a.date = ?
        """, (today,))
        
        data = [{'student_id': row['student_id'], 'name': row['name'], 'present': row['present']} for row in cursor.fetchall()]
    
    return jsonify(data)

# Save attendance data to CSV
@app.route('/save_attendance', methods=['POST'])
def save_attendance():
    data = request.json  # Receive attendance data from frontend
    csv_filename = f"attendance_{datetime.now().strftime('%Y-%m-%d')}.csv"

    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Student ID", "Name", "Present"])
        for student in data:
            writer.writerow([student['student_id'], student['name'], student['present']])

    return jsonify({"message": "Attendance saved successfully!", "file": csv_filename})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)