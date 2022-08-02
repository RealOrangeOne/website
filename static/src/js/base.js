const Elevator = require("elevator.js");
const debounce = require("lodash.debounce");
const throttle = require("lodash.throttle");

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
  if (HERO.getBoundingClientRect().top === 0) {
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

  document.querySelectorAll(".scroll-top").forEach((element) => {
    element.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  });

  document.querySelectorAll("#table-of-contents li a").forEach((element) => {
    element.addEventListener("click", (event) => {
      event.preventDefault();
      scrollToElement(document.querySelector(event.target.hash));
    });
  });

  const elevatorButton = document.getElementById("to-top-elevator");
  new Elevator({
    element: elevatorButton,
    mainAudio: elevatorButton.dataset.mainAudio,
    endAudio: elevatorButton.dataset.endAudio,
    preloadAudio: false,
  });
});

window.addEventListener("DOMContentLoaded", () => {
  setHeroHeight();

  if (window.location.hash <= 1) {
    return;
  }

  let scrollTarget = null;
  try {
    scrollTarget = document.getElementById(window.location.hash.slice(1));
  } catch {
    // Probably an invalid selector - just ignore it
  }

  if (!scrollTarget) {
    return;
  }

  scrollToElement(scrollTarget, "auto");
});

if (HERO) {
  window.addEventListener("resize", debounce(setHeroHeight, 2000));
  window.addEventListener("scroll", throttle(handleHeroStuck, 100));
}
