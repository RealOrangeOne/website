import * as DarkReader from "darkreader";

const DARK_READER_OPTIONS = {};

const DARK_READER_FIXES = {
  invert: [".wagtail-userbar-icon"],
};

// TODO: Add a UI toggle
DarkReader.auto(DARK_READER_OPTIONS, DARK_READER_FIXES);
