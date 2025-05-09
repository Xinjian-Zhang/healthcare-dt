function attemptLogin() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    eel.login(username, password)(function(isValid) {
        if (isValid) {
            window.location.href = "index.html";
        } else {
            document.getElementById("login-error").innerText = "Invalid username or password.";
        }
    });
}
