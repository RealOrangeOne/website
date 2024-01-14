FROM node:20-slim as frontend

RUN apt-get update --yes --quiet && apt-get install --yes --quiet curl

COPY package.json package-lock.json ./
RUN npm ci --no-audit - -progress=false --omit=dev

# Compile static files
COPY ./scripts ./scripts
COPY ./static/src ./static/src
RUN npm run build

# The actual container
FROM python:3.12-slim as production

ENV VIRTUAL_ENV=/venv

# renovate: datasource=github-tags depName=gchq/cyberchef
ENV S6_OVERLAY_VERSION=3.1.6.2

RUN useradd website --create-home -u 1000 && mkdir /app $VIRTUAL_ENV && chown -R website /app $VIRTUAL_ENV

WORKDIR /app

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    git \
    nginx \
    libnginx-mod-http-headers-more-filter \
    # wand dependencies
    libmagickwand-6.q16-6 libmagickwand-6.q16hdri-6 \
    && apt-get autoremove && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/aptible/supercronic/releases/download/v0.2.1/supercronic-linux-amd64 -o /usr/local/bin/supercronic && chmod +x /usr/local/bin/supercronic
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz /tmp
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz && tar -C / -Jxpf /tmp/s6-overlay-x86_64.tar.xz

ENV PATH=$VIRTUAL_ENV/bin:$PATH \
    PYTHONUNBUFFERED=1

EXPOSE 8000

RUN ln -fs /app/etc/nginx.conf /etc/nginx/sites-available/default && chown -R website /var/log/nginx

USER website

RUN python -m venv $VIRTUAL_ENV
COPY --chown=website requirements.txt ./

RUN pip install --no-cache -r requirements.txt

COPY --chown=website --from=frontend ./static/build ./static/build

COPY --chown=website ./etc ./etc
COPY --chown=website ./manage.py ./manage.py
COPY --chown=website ./website ./website

RUN cat ./etc/bashrc.sh >> ~/.bashrc

RUN SECRET_KEY=none python manage.py collectstatic --noinput --clear

COPY ./etc/s6-rc.d /etc/s6-overlay/s6-rc.d

ENTRYPOINT [ "/init" ]

# Just dev stuff
FROM production as dev

# Swap user, so the following tasks can be run as root
USER root

RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && apt-get install -y nodejs
RUN apt-get update --yes --quiet && apt-get install -y postgresql-client inotify-tools
RUN curl -sSf https://just.systems/install.sh | bash -s -- --to /usr/bin

# Restore user
USER website

COPY --chown=website dev-requirements.txt ./
RUN pip install --no-cache -r dev-requirements.txt

ENTRYPOINT []
CMD sleep infinity
