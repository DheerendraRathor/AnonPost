fuser -k 5050/tcp
nohup gunicorn anon_post.wsgi:application --timeout 600 --workers 10 --log-level=info --reload --bind=0.0.0.0:5050

