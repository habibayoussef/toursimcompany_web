function togglePassword() {
    var passwordField = document.getElementById("password");
    var eyeIcon = document.getElementById("toggle-eye");

    // Toggle password visibility
    if (passwordField.type === "password") {
        passwordField.type = "text"; // Show the password
        eyeIcon.innerHTML = "&#128065;"; // Change the icon to open eye
    } else {
        passwordField.type = "password"; // Hide the password
        eyeIcon.innerHTML = "&#128065;"; // Change the icon to closed eye
    }
}
