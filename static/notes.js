document.addEventListener('DOMContentLoaded', function() {
    const logoutButton = document.getElementById('logout');
    const deleteUserButton = document.getElementById('deleteUser');

    // Add event listeners
    logoutButton.addEventListener('click', logout);
    deleteUserButton.addEventListener('click', deleteUser);

    function logout() {
        fetch('/logout', { method: 'GET' })
        .then(response => {
            if (response.ok) {
                window.location.href = '/';  // Redirect to the home page after logout
            } else {
                console.error('Logout failed.');
            }
        })
        .catch(error => console.error('Error:', error));
    }

    function deleteUser() {
        if (confirm('Are you sure you want to delete your account?')) {
            logout();
            fetch('/delete_user', { method: 'POST' })
            .then(response => {
                if (response.ok) {
                    window.location.href = '/';  // Redirect to the home page after account deletion
                } else {
                    console.error('Account deletion failed.');
                }
            })
            .catch(error => console.error('Error:', error));
        }
    }
});
