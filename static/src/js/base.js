window.addEventListener("load", () => {
  const navbarBurger = document.getElementById("navbar-burger");
  const navbar = document.getElementById("navbar");

  navbarBurger.addEventListener("click", () => {
    navbarBurger.classList.toggle("is-active");
    navbar.classList.toggle("is-active");
  });
});
