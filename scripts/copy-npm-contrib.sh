#!/usr/bin/env bash

set -e

# Make sure we're in the root of the project
cd $(dirname $0)/..

CONTRIB_DIR=$PWD/static/build/contrib

rm -rf $CONTRIB_DIR
mkdir -p $CONTRIB_DIR

mkcontrib() {
  mkdir -p $CONTRIB_DIR/$1
  cp -r "${@:2}" $CONTRIB_DIR/$1/
}

mkcontrib fontawesome node_modules/@fortawesome/fontawesome-free/{css,webfonts}
mkcontrib elevator-js node_modules/elevator.js/demo/music/*
mkcontrib shareon node_modules/shareon/dist/{shareon.iife.*,shareon.min.css*}
mkcontrib fira-code node_modules/@fontsource/fira-code/latin.css
mkcontrib fira-code/files node_modules/@fontsource/fira-code/files/fira-code-latin-*

curl -sf -L https://raw.githubusercontent.com/genmon/aboutfeeds/main/tools/pretty-feed-v3.xsl -o $CONTRIB_DIR/pretty-feed-v3.xsl

# HACK: Make sure Google lighthouse can tell we're using `font-display: swap`
find $CONTRIB_DIR/fira-code -type f -exec sed -i 's/var(--fontsource-display, swap)/swap/g' {} \;
