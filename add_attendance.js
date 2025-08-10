// Capture image logic
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureButton = document.getElementById('capture');
const submitButton = document.getElementById('submitBtn');
const nameInput = document.getElementById('name');
const studentIdInput = document.getElementById('student_id');
const statusMessage = document.getElementById('status');

// Request access to the user's camera
navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
        video.srcObject = stream;
    })
    .catch((err) => {
        console.error("Camera access denied:", err);
        alert("Unable to access camera. Please check your device settings.");
    });

// Capture the image when the button is clicked
let capturedImage = null;
captureButton.addEventListener('click', () => {
    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    capturedImage = canvas.toDataURL('image/png');
    console.log("Captured Image: ", capturedImage);

    alert("Image Captured!");
});

// Save the captured image and student details when the form is submitted
submitButton.addEventListener('click', () => {
    if (!capturedImage) {
        alert("Please capture an image first!");
        return;
    }

    const studentId = studentIdInput.value.trim();
    const name = nameInput.value.trim();
    if (!studentId || !name) {
        alert("Please enter both student ID and name!");
        return;
    }

    // Show a saving status message
    statusMessage.style.display = "block";
    statusMessage.textContent = "Saving...";

    // Send image and student details to the backend
    fetch('/save_student', {  // Changed route to '/save_student' as per the Flask backend
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            student_id: studentId,
            name: name,
            image: capturedImage,
        }),
    })
    .then((response) => response.json())
    .then((data) => {
        alert(data.message || "Attendance added successfully!");
    })
    .catch((error) => {
        console.error("Error saving attendance:", error);
        alert("Error saving attendance. Please try again.");
    })
    .finally(() => {
        statusMessage.style.display = "none";
    });
});
