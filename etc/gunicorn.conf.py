wsgi_app = "website.wsgi:application"
disable_redirect_access_to_syslog = True
preload_app = True
bind = "127.0.0.1:8080"
max_requests = 1200
max_requests_jitter = 50
forwarded_allow_ips = "*"

# Run additional threads so the GIL isn't sitting completely idle
threads = 4
