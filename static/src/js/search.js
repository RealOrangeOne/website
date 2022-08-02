window.addEventListener("load", () => {
  const searchResults = document.getElementById("search-results");
  const resultsCount = document.getElementById("result-count");

  function handleSearchResults(event) {
    resultsCount.textContent =
      event.target.querySelectorAll(".listing-item").length;
  }
  searchResults.addEventListener("htmx:after-swap", handleSearchResults);
});
