require("lite-youtube-embed");
const GLightbox = require("glightbox");

const SCROLL_INDICATOR = document.getElementById("scroll-indicator");
const CONTENT = document.querySelector(".container.content");

window.addEventListener("load", () => {
  GLightbox({});
});

window.addEventListener("scroll", () => {
  const winScroll =
    document.body.scrollTop || document.documentElement.scrollTop;
  const height = CONTENT.getBoundingClientRect().height;
  const scrolled = Math.min((winScroll / height) * 100, 100);
  SCROLL_INDICATOR.style.width = `${scrolled}%`;
});
