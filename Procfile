web: ./manage.py runserver 0.0.0.0:8080
watch-js: npm run build:js -- --watch
watch-css: npm run build:css -- --watch
watch-contrib: ./scripts/copy-npm-contrib.sh; while inotifywait -e modify ./scripts/copy-npm-contrib.sh; do ./scripts/copy-npm-contrib.sh; done
worker: ./manage.py db_worker --interval 5
