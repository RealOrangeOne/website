const Elevator = require("elevator.js");

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

  const elevatorButton = document.getElementById("to-top-elevator");
  new Elevator({
    element: elevatorButton,
    mainAudio: elevatorButton.dataset.mainAudio,
    endAudio: elevatorButton.dataset.endAudio,
    preloadAudio: false,
  });
});
