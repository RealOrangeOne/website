import Darkmode from "darkmode-js";

const DARKMODE_OPTIONS = {
  left: "32px",
  right: "unset",
  time: "0.7s",
  saveInCookies: false,
  label: "🌓",
};

window.addEventListener("load", () => {
  const darkmode = new Darkmode(DARKMODE_OPTIONS);
  darkmode.showWidget();
  window.darkmodejs = darkmode;
});

// Also listen to native theme changes
window
  .matchMedia("(prefers-color-scheme: dark)")
  .addEventListener("change", (e) => {
    if (e.matches !== window.darkmodejs.isActivated()) {
      // HACK: .toggle doesn't work quite right
      window.darkmodejs.button.click();
    }
  });
