const Elevator = require("elevator.js");
const debounce = require("lodash.debounce");

const HERO = document.querySelector("section.hero");
const ROOT = document.querySelector(":root");

function getHeroHeight() {
  return HERO.getBoundingClientRect().height;
}

function setHeroHeight() {
  ROOT.style.setProperty("--hero-height", `${getHeroHeight()}px`);
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
      const rect = document
        .querySelector(event.target.hash)
        .getBoundingClientRect();
      const top = rect.top - getHeroHeight();
      window.scrollBy({ top: top, behavior: "smooth" });
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

window.addEventListener("resize", debounce(setHeroHeight, 2000));
window.addEventListener("load", setHeroHeight);
