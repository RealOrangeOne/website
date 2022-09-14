set dotenv-load

DEV_COMPOSE := justfile_directory() + "/docker/dev/docker-compose.yml"

# Recipes
@default:
  just --list

build:
  docker-compose -f {{ DEV_COMPOSE }} pull
  docker-compose -f {{ DEV_COMPOSE }} build
  docker-compose -f {{ DEV_COMPOSE }} run --rm --no-deps web npm ci

@compose +ARGS:
  docker-compose -f {{ DEV_COMPOSE }} {{ ARGS }}

@start:
  honcho start

@manage +ARGS:
  ./manage.py {{ ARGS }}

@pip +ARGS:
  pip {{ ARGS }}

test *ARGS:
  ./manage.py test {{ ARGS }}

coverage:
  coverage run ./manage.py test --keepdb
  coverage report
  coverage html

format:
  black .
  isort .
  find website/ -name '*.html' | xargs djhtml -i --tabwidth 2
  npm run format

lint: lint_python lint_node

lint_python:
  black --check .
  isort --check .
  flake8
  mypy . --show-error-codes
  curlylint .
  find website/ -name '*.html' | xargs djhtml --check --tabwidth 2

@lint_node:
  npm run lint

@sh:
  docker-compose -f {{ DEV_COMPOSE }} up -d
  docker-compose -f {{ DEV_COMPOSE }} exec web bash

@down:
  docker-compose -f {{ DEV_COMPOSE }} down
