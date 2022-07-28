set dotenv-load

# Recipes
@default:
  just --list

install:
  python -m venv env
  pip install -r dev-requirements.txt
  npm ci

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
