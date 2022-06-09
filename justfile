set dotenv-load

# Load virtualenv
export PATH := justfile_directory() + "/env/bin:" + env_var('PATH')

# Dev environment
export DEBUG := "true"
export SECRET_KEY := "super-secret-key"

# Recipes
@default:
  just --list

install:
  python -m venv env
  pip install -r dev-requirements.txt

@start:
  honcho start

@manage +ARGS:
  ./manage.py {{ ARGS }}

@collectstatic:
  ./manage.py collectstatic --noinput -v2
