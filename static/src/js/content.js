require("lite-youtube-embed");
const GLightbox = require("glightbox");
const clamp = require("lodash.clamp");

const SCROLL_INDICATOR = document.getElementById("scroll-indicator");
const CONTENT = document.querySelector(".container.content");

function handleScrollIndicator() {
  // How far down the page does the content start?
  const initialScroll = CONTENT.getBoundingClientRect().top + window.scrollY;

  const contentHeight = CONTENT.getBoundingClientRect().height;

  // How far down the page do we consider the content "read"?
  const scrollTarget = window.innerHeight * 0.75;

  const scrolled =
    (window.scrollY - initialScroll + scrollTarget) / contentHeight;

  const scrolledPercentage = clamp(scrolled * 100, 0, 100);

  SCROLL_INDICATOR.style.width = `${scrolledPercentage.toFixed(2)}%`;
}

window.addEventListener("load", () => {
  window.addEventListener("resize", handleScrollIndicator);
  window.addEventListener("scroll", handleScrollIndicator);

  GLightbox({});

  // Initialize the indicator
  handleScrollIndicator();
});
