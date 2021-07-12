#!/bin/bash

set -e
docker build --target production --tag anniebedford/todo-app-prod:latest --tag anniebedford/todo-app-prod:$TRAVIS_COMMIT  .
echo "$DOCKER_PW" | docker login -u "$DOCKER_USER" --password-stdin
docker push $DOCKER_USER/todo-app-prod:latest
docker push $DOCKER_USER/todo-app-prod:$TRAVIS_COMMIT
docker tag $DOCKER_USER/todo-app-prod registry.heroku.com/todo-app-ab/web

docker login --username=_ --password="$HEROKU_API_KEY" registry.heroku.com

docker push registry.heroku.com/todo-app-ab/web
heroku container:release web -a todo-app-ab
