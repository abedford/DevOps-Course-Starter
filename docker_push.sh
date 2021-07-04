#!/bin/bash
docker build --target production --tag anniebedford/todo-app-prod:latest --tag anniebedford/todo-app-prod:$TRAVIS_COMMIT  .
echo "$DOCKER_PW" | docker login -u "$DOCKER_USER" --password-stdin
docker push anniebedford/todo-app-prod:latest
docker push anniebedford/todo-app-prod:$TRAVIS_COMMIT
docker tag anniebedford/todo-app-prod registry.heroku.com/todo-app-ab/web


#echo "$HEROKU_API_KEY" | docker login --username="abedford@gmail.com" --password-stdin registry.heroku.com
echo $HEROKU_API_KEY 
docker login --username="abedford@gmail.com" --password="$HEROKU_API_KEY" registry.heroku.com
docker push registry.heroku.com/todo-app-ab/web
heroku container:release web -a todo-app-ab
