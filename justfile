set dotenv-load

DEV_COMPOSE := justfile_directory() + "/docker/dev/docker-compose.yml"

# Recipes
@default:
  just --list

build:
  docker-compose -f {{ DEV_COMPOSE }} pull
  docker-compose -f {{ DEV_COMPOSE }} build
  docker-compose -f {{ DEV_COMPOSE }} run --user=website --rm --no-deps web -c "npm ci"

@compose +ARGS:
  docker-compose -f {{ DEV_COMPOSE }} {{ ARGS }}

@start:
  honcho start

@manage +ARGS:
  ./manage.py {{ ARGS }}

@pip +ARGS:
  pip {{ ARGS }}

test *ARGS:
  TEST=true ./manage.py test {{ ARGS }}

coverage:
  TEST=true coverage run ./manage.py test --keepdb
  coverage report
  coverage html

format:
  ruff check . --fix
  black .
  djlint website/ --reformat
  npm run format

lint: lint_python lint_node

lint_python:
  ruff check .
  black --check .
  mypy . --show-error-codes
  djlint website/ --lint --check

@lint_node:
  npm run lint

@sh:
  docker-compose -f {{ DEV_COMPOSE }} up -d
  docker-compose -f {{ DEV_COMPOSE }} exec --user=website web bash

@down:
  docker-compose -f {{ DEV_COMPOSE }} down
