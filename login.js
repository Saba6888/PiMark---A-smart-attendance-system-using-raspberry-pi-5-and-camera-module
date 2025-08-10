document.getElementById('login-form').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent default form submission behavior
  
    console.log("Submit event triggered."); // Debugging step
  
    // Retrieve username and password values
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
  
    console.log("Username:", username); // Check what username is being retrieved
    console.log("Password:", password); // Check what password is being retrieved
  
    // Check if the entered credentials match
    if (username === 'admin' && password === '123') {
      console.log("Login successful. Redirecting...");
      alert('Login successful! Redirecting to dashboard...');
      // Redirect to the dashboard page
      window.location.href = 'dashboard.html';
    } else {
      console.log("Invalid login attempt.");
      alert('Invalid username or password. Please try again.');
    }
  });
  