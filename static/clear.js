const clearButton = document.getElementById("clear");
const welcomeMessage = document.getElementById("welcome");
const userName = localStorage.getItem("username");
const login = localStorage.getItem("login");

if (login === "first") {
  welcomeMessage.innerHTML = `Welcome ${userName}!`;
  localStorage.setItem("login", "in");
} else if (login === "saved") {
  welcomeMessage.innerHTML = `Welcome back ${userName}!`;
  localStorage.setItem("login", "in");
} else if (login === "in") {
  welcomeMessage.innerHTML = `You're logged in as ${userName}`;
}

clearButton.addEventListener("click", function() {
  localStorage.clear();
  window.location.replace("/clear");
});