// script.js

// Function to validate signup form
function validateSignupForm() {
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirm_password").value;
    if (password != confirmPassword) {
        alert("Passwords do not match.");
        return false;
    }
    return true;
}

// Function to confirm deletion of a note
function confirmDelete() {
    return confirm("Are you sure you want to delete this note?");
}
