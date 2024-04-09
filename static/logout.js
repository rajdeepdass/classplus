document.getElementById("logout").addEventListener("click", function() {
    if (confirm("Are you sure you want to log out?")) {
        window.location.href = "/logout";
    }
});
