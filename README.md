<h1 align="center">📸 Face Recognition Attendance System (Flask + OpenCV)</h1>

<p align="center">
  An AI-powered web application for automatic student attendance marking using <b>Face Recognition</b>, built with <code>Flask</code>, <code>OpenCV</code>, and <code>SQLite</code>.
</p>

---

<h2>📌 Project Overview</h2>
<p>
This project is a <b>Flask-based web application</b> that leverages <b>face recognition</b> technology to mark student attendance automatically.  
It integrates:
</p>
<ul>
  <li>Real-time face recognition with <b>OpenCV</b> and <b>face_recognition</b></li>
  <li>Student record management with <b>SQLite</b></li>
  <li>Automatic attendance logging with <b>CSV export</b></li>
  <li>Web-based dashboard for managing and monitoring attendance</li>
</ul>

---

<h2>🛠️ Tech Stack</h2>
<ul>
  <li>Flask (Backend framework)</li>
  <li>OpenCV + face_recognition (Face detection & recognition)</li>
  <li>SQLite (Database for storing students and attendance)</li>
  <li>HTML/CSS/JS (Frontend templates)</li>
  <li>CSV export (Daily attendance records)</li>
</ul>

---

<h2>📂 Features</h2>
<ul>
  <li><b>Student Management</b>: Add, delete, and fetch student details with photo uploads</li>
  <li><b>Face Recognition</b>: Identify students in real-time and mark attendance automatically</li>
  <li><b>Attendance Tracking</b>: Store daily attendance in SQLite and export as CSV</li>
  <li><b>Recognition History</b>: View logs of recognized faces with timestamps</li>
  <li><b>Encodings Optimization</b>: Save and load facial encodings with <code>pickle</code> for faster recognition</li>
</ul>

---

<h2>📊 Database Schema</h2>
<p>The SQLite database (<code>attendance.db</code>) contains the following tables:</p>
<ul>
  <li><code>students</code>: Stores student ID, name, and image path</li>
  <li><code>recognised_faces</code>: Logs recognized faces with timestamps</li>
  <li><code>attendance</code>: Tracks daily attendance per student</li>
</ul>

---

<h2>🚀 How to Run</h2>
<ol>
  <li>Clone the repository:</li>
  <pre><code>git clone https://github.com/yourusername/face-recognition-attendance.git
cd face-recognition-attendance</code></pre>

  <li>Install dependencies:</li>
  <pre><code>pip install -r requirements.txt</code></pre>

  <li>Run the Flask server:</li>
  <pre><code>python app.py</code></pre>

  <li>Access the app in your browser:</li>
  <pre><code>http://127.0.0.1:5001</code></pre>
</ol>

---

<h2>📸 Workflow</h2>
<ol>
  <li>Admin adds students with their details & photo</li>
  <li>Face encodings are generated and stored</li>
  <li>When a student is recognized, attendance is marked in the DB</li>
  <li>Attendance records can be viewed on the dashboard or exported to CSV</li>
</ol>

---

<h2>📈 API Endpoints</h2>
<ul>
  <li><code>/save_student</code> → Add a new student (JSON request)</li>
  <li><code>/students</code> → Get all registered students</li>
  <li><code>/delete_student/&lt;id&gt;</code> → Delete student by ID</li>
  <li><code>/recognize_face</code> → Recognize face & mark attendance</li>
  <li><code>/recognized_faces</code> → Fetch recognition logs</li>
  <li><code>/get_attendance</code> → Fetch today’s attendance</li>
  <li><code>/save_attendance</code> → Save attendance data to CSV</li>
</ul>

---

<h2>✅ Future Improvements</h2>
<ul>
  <li>Live camera integration for real-time recognition</li>
  <li>Admin authentication system</li>
  <li>Email/SMS notifications for absentees</li>
  <li>Analytics dashboard for attendance trends</li>
</ul>

---

<h2>📜 License</h2>
<p>
This project is licensed under the MIT License – feel free to use and modify it.
</p>
