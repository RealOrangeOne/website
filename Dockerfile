FROM node:19-slim as frontend

COPY package.json package-lock.json ./
RUN npm ci --no-audit - -progress=false --omit=dev

# Compile static files
COPY ./scripts ./scripts
COPY ./static/src ./static/src
RUN npm run build

# The actual container
FROM python:3.10-slim as production

ENV VIRTUAL_ENV=/venv

RUN useradd website --create-home -u 1000 && mkdir /app $VIRTUAL_ENV && chown -R website /app $VIRTUAL_ENV

WORKDIR /app

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    git \
    # wand dependencies
    libmagickwand-6.q16-6 libmagickwand-6.q16hdri-6 \
    && apt-get autoremove && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/aptible/supercronic/releases/download/v0.2.1/supercronic-linux-amd64 -o /usr/local/bin/supercronic && chmod +x /usr/local/bin/supercronic

RUN pip install --no-cache poetry==1.2.0

ENV PATH=$VIRTUAL_ENV/bin:$PATH \
    PYTHONUNBUFFERED=1

EXPOSE 8000

USER website

RUN python -m venv $VIRTUAL_ENV
COPY --chown=website pyproject.toml poetry.lock ./

# Clear the poetry and pip caches, as `--no-cache` doesn't do anything
RUN poetry install --without=dev && rm -rf $HOME/.cache

COPY --chown=website --from=frontend ./static/build ./static/build

COPY --chown=website ./etc ./etc
COPY --chown=website ./manage.py ./manage.py
COPY --chown=website ./website ./website

RUN SECRET_KEY=none python manage.py collectstatic --noinput --clear -v3

CMD python manage.py migrate --noinput && gunicorn -c etc/gunicorn.conf.py

# Just dev stuff
FROM production as dev

# Swap user, so the following tasks can be run as root
USER root
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && apt-get install -y nodejs
RUN apt-get install -y postgresql-client inotify-tools
RUN curl -sSf https://just.systems/install.sh | bash -s -- --to /usr/bin

# Restore user
USER website

RUN poetry install --no-cache

CMD sleep infinity
