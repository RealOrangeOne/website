FROM node:19-slim as frontend

COPY package.json package-lock.json ./
RUN npm ci --no-audit - -progress=false --omit=dev

# Compile static files
COPY ./scripts ./scripts
COPY ./static/src ./static/src
RUN npm run build

# The actual container
FROM python:3.11-slim as production

ENV VIRTUAL_ENV=/venv

RUN useradd website --create-home -u 1000 && mkdir /app $VIRTUAL_ENV && chown -R website /app $VIRTUAL_ENV

WORKDIR /app

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    git \
    nginx \
    # wand dependencies
    libmagickwand-6.q16-6 libmagickwand-6.q16hdri-6 \
    && apt-get autoremove && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/aptible/supercronic/releases/download/v0.2.1/supercronic-linux-amd64 -o /usr/local/bin/supercronic && chmod +x /usr/local/bin/supercronic

ENV PATH=$VIRTUAL_ENV/bin:$PATH \
    PYTHONUNBUFFERED=1

EXPOSE 8000

RUN ln -fs /app/etc/nginx.conf /etc/nginx/sites-available/default

USER website

RUN python -m venv $VIRTUAL_ENV
COPY --chown=website requirements.txt ./

RUN pip install --no-cache -r requirements.txt

COPY --chown=website --from=frontend ./static/build ./static/build

COPY --chown=website ./etc ./etc
COPY --chown=website ./manage.py ./manage.py
COPY --chown=website ./website ./website

RUN SECRET_KEY=none python manage.py collectstatic --noinput --clear

CMD ["/app/etc/entrypoints/web"]

# Just dev stuff
FROM production as dev

# Swap user, so the following tasks can be run as root
USER root
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && apt-get install -y nodejs
RUN apt-get install -y postgresql-client inotify-tools
RUN curl -sSf https://just.systems/install.sh | bash -s -- --to /usr/bin

# Restore user
USER website

COPY --chown=website dev-requirements.txt ./
RUN pip install --no-cache -r dev-requirements.txt

CMD sleep infinity
