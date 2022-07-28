FROM node:16 as frontend

COPY package.json package-lock.json ./
RUN npm ci --no-audit --progress=false

# Compile static files
COPY ./scripts ./scripts
COPY ./static/src ./static/src
RUN npm run build

# The actual container
FROM python:3.10 as production

ENV VIRTUAL_ENV=/venv

RUN useradd website --create-home -u 1000 && mkdir /app $VIRTUAL_ENV && chown -R website /app $VIRTUAL_ENV

WORKDIR /app

ENV PATH=${POETRY_HOME}/bin:$VIRTUAL_ENV/bin:$PATH \
    PYTHONUNBUFFERED=1

EXPOSE 8000

USER website

RUN python -m venv $VIRTUAL_ENV
COPY --chown=website requirements/base.txt ./requirements/base.txt
RUN pip install --upgrade pip && pip install -r ./requirements/base.txt

COPY --chown=website --from=frontend ./static/build ./static/build

COPY --chown=website ./manage.py ./manage.py
COPY --chown=website ./templates ./templates
COPY --chown=website ./website ./website

RUN SECRET_KEY=none python manage.py collectstatic --noinput --clear -v3

CMD gunicorn

# Just dev stuff
FROM production as dev

# Swap user, so the following tasks can be run as root
USER root
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && apt-get install -y nodejs
RUN apt-get install -y postgresql-client
RUN curl -sSf https://just.systems/install.sh | bash -s -- --to /usr/bin

# Restore user
USER website

COPY --chown=website requirements/dev.txt ./requirements/dev.txt
RUN pip install --upgrade pip && pip install -r requirements/dev.txt

CMD sleep infinity
