#!/usr/bin/env bash

set -ex

cd $(dirname $0)/..

COMMON_ARGS="--quiet --annotation-style=line"

pip-compile $COMMON_ARGS -o requirements/base.txt requirements/base.in
pip-compile $COMMON_ARGS -o requirements/dev.txt requirements/dev.in
