document.addEventListener("DOMContentLoaded", () => {
  const navbarBurger = document.getElementById("navbar-burger");
  const navbar = document.getElementById("navbar");

  navbarBurger.addEventListener("click", () => {
    console.log("click");
    navbarBurger.classList.toggle('is-active');
    navbar.classList.toggle('is-active');
  })
});
