# Website

## Installation

1. Create a virtual environment
2. `pip install -r requirements.txt`
3. Create [`.env` file](#env-file)
4. `./manage.py runserver`

### `.env` file

Local development secrets are stored in a `.env` file.

These values are required for the application to load

- `DEBUG` set to `false`
- `SECRET_KEY` set to [something](https://django-secret-key-generator.netlify.app/) semi-random
