# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.tempalate` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Connecting to the Mongo DB
To connect to Mongo DB you will need a Mongo Atlas DB connection with user and password. Register with https://www.mongodb.com/cloud/atlas/ to set up your Database.
Put the details in the .env file
MONGO_CONNECTION=mongodb+srv
MONGO_SRV=XXX
MONGO_DB=XXX
MONGO_USER=XXX
MONGO_PWD=XXX

## Running the tests

To run the tests

```bash
$ poetry run pytest
```

To run test coverage

```bash
$ poetry run pytest --cov=report term-missing --cov=tests

```
The UI tests are in a folder called tests_e2e and can be run separately, or not at all if you want the tests to complete more quickly. They rely on chrome browser and chrome driver being available and being added to the path.

A few tests will actually connect directly to mongo db with your API key and server token to create a temporary board but this will be deleted as part of the test tear down. Other tests will just use dummy board data.


## Running in Vagrant
If you install Vagrant, you can run the application in its own vm. Just install Vagrant from https://www.vagrantup.com/docs/installation and then run the following command in the DevOps-Course-Starter direction
```bash
$ vagrant up
```

## Running in Docker

If you want to build and run a docker image of this application using a multi-stage DockerFile you can run:
```bash
$ docker build --tag todo-app-prod --target production .
```
for a production image 

or 
```bash
$ docker build --tag todo-app-dev --target development .
```
for a development image. 

And then to run it:

for production
```bash
$ docker run -p 5000:5000 --env-file .env todo-app-prod
```

for development
```bash
$ docker run -p 5000:5000 --mount type=bind,source="$((Get-Location).tostring())\todo_app",target="/todo_app/todo_app" --env-file .env todo-app-dev
```
This sets up the port forwarding and passes the .env file through to set up the flask environment paramenters. It also sets up a bind mount so that any changes in the source code will automatically be picked up with auto reload. 

You should then be able to see the application as usual at 127.0.0.1:5000
You will need to make sure you create .env as a file to put your environment variables in, this needs to include:
MONGO_CONNECTION=mongodb+srv
MONGO_SRV=XXX
MONGO_DB=XXX
MONGO_USER=XXX
MONGO_PWD=XXX
as before. This won't get checked in.


For testing you can run
```bash
$ docker build --tag todo-app-test --target test .
```
This will create a test container that can run your tests.

To run the tests
```bash
$ docker run --env-file .env.test todo-app-test todo_app/tests
```
This should return the results of your tests

To just run the UI tests
```bash
$ docker run --env-file .env todo-app-test todo_app/tests_e2e

To debug in to this container (or another one) you can run:
```bash
$ docker run -it --entrypoint /bin/bash todo-app-test
```

and then from within the container you can run the tests:
```bash
$ poetry run pytest
```
## Code Documentation
You will find the code documentation diagrams under the documentation folder. These are in C4 model format so show the system context, containter and component architecture as well as a UML diagram for the code.

## Deploying to Docker Hub Registry
The travis continuous integration is set up so that when you check anything in, it will automatically build a development and test image to run the tests for the application. If this all succeeds, and it's on the main branch, then the check-in will trigger a production build which will then get pushed to docker hub, and to heroku. Once this is pushed, it gets released and you can see the application working in heroku. 

## User Authorization
The application uses GitHub OAuth to authorize users. By default any new users will be Read-only and will need an administrator to update their role if they need extra rights to edit tasks, add tasks or manage users. User data is stored in the mongo database. 

