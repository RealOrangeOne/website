const Elevator = require("elevator.js");
const debounce = require("lodash.debounce");
const throttle = require("lodash.throttle");

require("htmx.org");

const HERO = document.querySelector("section.hero");
const ROOT = document.querySelector(":root");

function getHeroHeight() {
  if (!HERO) {
    return 0;
  }
  return HERO.getBoundingClientRect().height;
}

function setHeroHeight() {
  ROOT.style.setProperty("--hero-height", `${getHeroHeight()}px`);
}

function scrollToElement(element, behavior = "smooth") {
  const rect = element.getBoundingClientRect();
  const top = rect.top - getHeroHeight();
  window.scrollBy({ top: top, behavior });
}

function handleHeroStuck() {
  if (
    HERO.getBoundingClientRect().top <= 0 &&
    window.getComputedStyle(HERO).position === "sticky"
  ) {
    HERO.classList.add("stuck");
  } else {
    HERO.classList.remove("stuck");
  }
}

window.addEventListener("load", () => {
  const navbarBurger = document.getElementById("navbar-burger");
  const navbar = document.getElementById("navbar");

  navbarBurger.addEventListener("click", () => {
    navbarBurger.classList.toggle("is-active");
    navbar.classList.toggle("is-active");
  });

  for (const element of document.querySelectorAll(".scroll-top")) {
    element.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  for (const element of document.querySelectorAll("#table-of-contents li a")) {
    element.addEventListener("click", (event) => {
      event.preventDefault();
      scrollToElement(document.querySelector(event.target.hash));
    });
  }

  const elevatorButton = document.getElementById("to-top-elevator");
  new Elevator({
    element: elevatorButton,
    mainAudio: elevatorButton.dataset.mainAudio,
    endAudio: elevatorButton.dataset.endAudio,
    preloadAudio: false,
  });

  for (const codeBlock of document.querySelectorAll(".block-code")) {
    const clipboardIcon = codeBlock.querySelector(".code-copy");

    // There may not be an icon
    if (!clipboardIcon) {
      continue;
    }

    clipboardIcon.addEventListener("click", (event) => {
      event.preventDefault();
      navigator.clipboard
        .writeText(codeBlock.querySelector("pre").textContent)
        .then(() => {
          clipboardIcon.classList.remove("fa-regular", "fa-clipboard");
          clipboardIcon.classList.add("fa-solid", "fa-check");

          setTimeout(() => {
            clipboardIcon.classList.add("fa-regular", "fa-clipboard");
            clipboardIcon.classList.remove("fa-solid", "fa-check");
          }, 3000);
        });
    });
  }
});

window.addEventListener("DOMContentLoaded", () => {
  if (HERO) {
    setHeroHeight();
    handleHeroStuck();

    window.addEventListener("resize", debounce(setHeroHeight, 2000));
    window.addEventListener("scroll", throttle(handleHeroStuck, 100));
  }

  if (window.location.hash <= 1) {
    return;
  }

  let scrollTarget;
  try {
    scrollTarget = document.getElementById(window.location.hash.slice(1));
  } catch (error) {
    // Probably an invalid selector - just ignore it
  }

  if (!scrollTarget) {
    return;
  }

  scrollToElement(scrollTarget, "auto");
});
