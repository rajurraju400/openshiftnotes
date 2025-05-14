(function() {
  // Check if user is already authenticated in this session
  if (sessionStorage.getItem("authenticated") === "true") {
    return; // User is already logged in
  }

  const validUsers = {
    "admin": "redhat",
    "venkat": "openshift123",
    "raj": "ztpsecure"
  };

  const inputUser = prompt("Enter username:");
  const inputPass = prompt("Enter password:");

  if (validUsers[inputUser] && validUsers[inputUser] === inputPass) {
    // Save login in session (cleared on tab close or refresh)
    sessionStorage.setItem("authenticated", "true");
    sessionStorage.setItem("username", inputUser);
  } else {
    // Redirect to a custom "Access Denied" page
    window.location.href = "https://www.redhat.com/en";
  }
})();

// Optional logout button logic
window.addEventListener("DOMContentLoaded", function() {
  const logoutBtn = document.getElementById("logout-button");
  if (logoutBtn && sessionStorage.getItem("authenticated") === "true") {
    logoutBtn.style.display = "block";
  }
});
