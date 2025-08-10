document.addEventListener('DOMContentLoaded', function () {
    // Ensure the page is fully loaded before running the script
    const chartElement = document.getElementById('attendanceChart');
  
    if (!chartElement) {
      console.error("Error: 'attendanceChart' element not found.");
      return;
    }
  
    const ctx = chartElement.getContext('2d');
  
    // Pie chart showing student attendance
    const attendanceChart = new Chart(ctx, {
      type: 'pie',
      data: {
        labels: ['Present', 'Absent'], // Attendance categories
        datasets: [{
          label: 'Student Attendance',
          data: [75, 25], // Example: 75% Present, 25% Absent
          backgroundColor: ['#4CAF50', '#F44336'], // Colors for Present and Absent
          borderColor: ['#4CAF50', '#F44336'], // Border colors
          borderWidth: 1
        }]
      },
      options: {
        responsive: true, // Adjusts to the container size
        plugins: {
          legend: {
            position: 'top', // Place the legend at the top
          },
          tooltip: {
            callbacks: {
              label: function (tooltipItem) {
                return tooltipItem.label + ': ' + tooltipItem.raw + '%';
              }
            }
          }
        }
      }
    });
  });
  