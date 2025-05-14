(function() {
  if (localStorage.getItem("authenticated") === "true") {
    return; // Already logged in
  }

  const validUsers = {
    "admin": "redhat",
    "venkat": "openshift123",
    "raj": "ztpsecure"
  };

  const inputUser = prompt("Enter username:");
  const inputPass = prompt("Enter password:");

  if (validUsers[inputUser] && validUsers[inputUser] === inputPass) {
    localStorage.setItem("authenticated", "true");
    localStorage.setItem("username", inputUser);
  } else {
    window.location.href = "https://www.redhat.com/en";
  }
})();

window.addEventListener("DOMContentLoaded", function() {
  if (localStorage.getItem("authenticated") !== "true") {
    const logoutBtn = document.getElementById("logout-button");
    if (logoutBtn) logoutBtn.style.display = "none";
  }
});
