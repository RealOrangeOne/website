set dotenv-load

DEV_COMPOSE := justfile_directory() + "/docker/dev/docker-compose.yml"

# Recipes
@default:
  just --list

@build:
  docker-compose -f {{ DEV_COMPOSE }} pull
  docker-compose -f {{ DEV_COMPOSE }} build

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

format:
  black .
  isort .
  npm run format

lint: lint_python lint_node

lint_python:
  black --check .
  isort --check .
  flake8
  mypy . --show-error-codes

@lint_node:
  npm run lint

@sh:
  docker-compose -f {{ DEV_COMPOSE }} exec web bash
