function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const errorMsg = document.getElementById("errorMsg");

    // Check if username and password match the correct credentials
    if (username === 'admin' && password === 'admin123') {
        window.location.href = 'admin.html'; // Redirect to admin page
    } else {
        errorMsg.textContent = "Invalid username or password."; // Show error message
    }
}
