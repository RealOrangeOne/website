web: ./manage.py runserver
watch-js: npm run build:js -- --watch
watch-css: npm run build:css -- --watch
watch-contrib: ./scripts/copy-npm-contrib.sh; while inotifywait -e modify ./scripts/copy-npm-contrib.sh; do ./scripts/copy-npm-contrib.sh; done
rqworker: ./manage.py rqworker --with-scheduler
