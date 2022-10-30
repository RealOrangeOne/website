import os

import gunicorn

wsgi_app = "website.wsgi:application"
accesslog = "-"
disable_redirect_access_to_syslog = True
preload_app = True
bind = "0.0.0.0"
max_requests = 1200
max_requests_jitter = 100

# Run an additional thread so the GIL isn't sitting completely idle
threads = 2

# Replace gunicorn's 'Server' HTTP header
gunicorn.SERVER_SOFTWARE = gunicorn.SERVER = "Wouldn't you like to know"

# Allow `X-Forwarded-*` headers from specific IPs
if "FORWARDED_ALLOW_IPS" in os.environ:
    forwarded_allow_ips = os.environ["FORWARDED_ALLOW_IPS"]
