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
mkcontrib fira-code node_modules/firacode/distr/{fira_code.css,woff2,woff}
