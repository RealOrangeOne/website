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
  black website
  isort website
  npm run format

lint: lint_python lint_node

lint_python:
  black --check website
  isort --check website
  flake8 website
  mypy website --show-error-codes

@lint_node:
  npm run lint
