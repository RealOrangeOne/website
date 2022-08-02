window.addEventListener("DOMContentLoaded", () => {
  const searchResults = document.getElementById("search-results");
  const resultsCountDisplay = document.getElementById("result-count");

  function handleSearchResults(event) {
    const resultsCount = event.target.querySelectorAll(".listing-item").length;
    if (resultsCount) {
      resultsCountDisplay.textContent =
        `Found ${resultsCount} result` + (resultsCount > 1 ? "s" : "");
    } else {
      resultsCountDisplay.textContent = "";
    }
  }
  searchResults.addEventListener("htmx:afterSwap", handleSearchResults);
});
