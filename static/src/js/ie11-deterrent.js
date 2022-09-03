const { isIE11 } = require("@ledge/is-ie-11");

if (isIE11()) {
  // Stop using internet explorer!
  window.location.assign("https://stopinternetexplorer.com/");
}
