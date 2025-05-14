(function() {
  if (sessionStorage.getItem("authenticated") === "true") {
    return; // Already logged in for this session
  }

  const username = "admin";
  const password = "redhat";

  const inputUser = prompt("Enter username:");
  const inputPass = prompt("Enter password:");

  if (inputUser === username && inputPass === password) {
    sessionStorage.setItem("authenticated", "true");
  } else {
    alert("Access denied!");
    window.location.href = "https://www.redhat.com/en";
  }
})();


window.addEventListener("DOMContentLoaded", function() {
  if (sessionStorage.getItem("authenticated") !== "true") {
    const logoutBtn = document.getElementById("logout-button");
    if (logoutBtn) logoutBtn.style.display = "none";
  }
});