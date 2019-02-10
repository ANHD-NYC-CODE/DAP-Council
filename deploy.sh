docker-compose exec app pipenv install
docker-compose exec celery_default pipenv install
docker-compose exec celery_default pipenv install
docker-compose exec celerybeat pipenv install

docker-compose restart app
docker-compose restart nginx

# gracefully shutdown and restart workers after tasks completed (propogates to all workers)

docker-compose exec celery_default celery control shutdown


# docker-compose exec celery_default pkill 'celery'
# docker-compose exec celery_update pkill 'celery'
