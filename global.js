
function toggleSettings() {
  const dropdown = document.getElementById("settings-dropdown");
  const arrow = document.getElementById("settings-arrow");

  if (dropdown.style.display === "flex") {
    dropdown.style.display = "none";
    arrow.textContent = "▼";
  } else {
    dropdown.style.display = "flex";
    arrow.textContent = "▲";
  }
}

function togglePreferences(event) {
  event.stopPropagation();
  const dropdown = document.getElementById("preferences-dropdown");
  const arrow = document.getElementById("preferences-arrow");

  if (dropdown.style.display === "flex") {
    dropdown.style.display = "none";
    arrow.textContent = "▼";
  } else {
    dropdown.style.display = "flex";
    arrow.textContent = "▲";
  }
}

function setDarkMode() {
  document.body.style.background = "#1a1a1a";
  document.body.style.color = "white";
}

function setLightMode() {
  document.body.style.background = "";
  document.body.style.color = "";
}
function setDarkMode() {
  document.body.classList.add("dark-mode");
  localStorage.setItem("theme", "dark");
}

function setLightMode() {
  document.body.classList.remove("dark-mode");
  localStorage.setItem("theme", "light");
}
// Keep theme after page reload
window.onload = function() {
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "dark") {
    document.body.classList.add("dark-mode");
  }
};
