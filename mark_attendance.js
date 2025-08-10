document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('manualAttendanceForm');

  form.addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form from refreshing page

    const studentName = document.getElementById('studentName').value;
    const attendanceDate = document.getElementById('attendanceDate').value;
    const attendanceTime = document.getElementById('attendanceTime').value;
    const isPresent = document.getElementById('isPresent').checked;

    const data = {
      name: studentName,
      date: attendanceDate,
      time: attendanceTime,
      present: isPresent,
    };

    fetch('/add_attendance', {  // Flask backend URL to handle the request
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    .then((response) => response.json())
    .then((data) => {
      alert(data.message || "Attendance successfully marked!");
      // Optionally reset the form here
      form.reset();
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Error marking attendance. Please try again.");
    });
  });
});
