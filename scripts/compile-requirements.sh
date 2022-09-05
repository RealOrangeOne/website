#!/usr/bin/env bash

set -e

cd $(dirname $0)/..

COMMON_ARGS="--quiet --annotation-style=line --resolver=backtracking $@"

set -x

pip-compile $COMMON_ARGS -o requirements/base.txt requirements/base.in
pip-compile $COMMON_ARGS -o requirements/dev.txt requirements/dev.in
