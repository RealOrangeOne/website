import gunicorn

wsgi_app = "website.wsgi:application"
accesslog = "-"
disable_redirect_access_to_syslog = True
preload_app = True
bind = "0.0.0.0"

# Replace gunicorn's 'Server' HTTP header
gunicorn.SERVER_SOFTWARE = "Wouldn't you like to know"
