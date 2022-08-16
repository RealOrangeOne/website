const DARK_MODE_CLASS = "dark-mode";
const body = document.getElementsByTagName("body")[0];

const matchesDarkMode = window.matchMedia("(prefers-color-scheme: dark)");

function handleDarkMode(darkMode) {
  if (darkMode) {
    body.classList.add(DARK_MODE_CLASS);
  } else {
    body.classList.remove(DARK_MODE_CLASS);
  }
}

matchesDarkMode.addEventListener("change", (event) =>
  handleDarkMode(event.matches)
);

handleDarkMode(matchesDarkMode.matches);
