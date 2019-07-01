const enterButton = document.getElementById("login");
const userName = document.getElementById("username");


if (localStorage.getItem("username") == undefined) {
  localStorage.setItem("login", "first");
} else {
  localStorage.setItem("login", "saved");
  window.location.href = "/options";
}

enterButton.addEventListener("click", function() {
  localStorage.setItem("username", userName.value);
  window.location.replace("/options");
});