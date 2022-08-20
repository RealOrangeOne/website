const DARK_MODE_CLASS = "dark-mode";
const STORAGE_KEY = "dark-mode";

const htmlTag = document.getElementsByTagName("html")[0];
const darkModeToggle = document.getElementById("dark-mode-toggle");

const matchesDarkMode = window.matchMedia("(prefers-color-scheme: dark)");

const darkModeCodeStyles = document.getElementById("pygments-dark");
const lightModeCodeStyles = document.getElementById("pygments-light");

function handleDarkMode(darkMode) {
  window.localStorage.setItem(STORAGE_KEY, darkMode.toString());

  if (darkMode) {
    htmlTag.classList.add(DARK_MODE_CLASS);
  } else {
    htmlTag.classList.remove(DARK_MODE_CLASS);
  }

  if (darkModeCodeStyles) {
    darkModeCodeStyles.sheet.disabled = !darkMode;
    lightModeCodeStyles.sheet.disabled = darkMode;
  }
}

if (window.localStorage.getItem(STORAGE_KEY) === null) {
  window.localStorage.setItem(STORAGE_KEY, matchesDarkMode.matches);
  handleDarkMode(matchesDarkMode.matches);
} else {
  handleDarkMode(window.localStorage.getItem(STORAGE_KEY) === "true");
}

window.addEventListener("load", () => {
  matchesDarkMode.addEventListener("change", (event) =>
    handleDarkMode(event.matches)
  );

  darkModeToggle.addEventListener("click", () => {
    handleDarkMode(window.localStorage.getItem(STORAGE_KEY) !== "true");
  });

  window.setTimeout(() => {
    htmlTag.classList.add("dark-mode-animate");
  }, 1000);
});
