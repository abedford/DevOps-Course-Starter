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

## Connecting to the Trello API
To connect to Trello API you will need an API key, a server token and a board ID. Register with https://developer.atlassian.com/cloud/trello/ to get your API key and server token. 
Create a board on Trello and use this board ID for the ToDo app. 
Put the details in the .env file
API_KEY=XXX
SERVER_TOKEN=XXX
BOARD_ID=XXX

## Running the tests
```bash
$ poetry run pytest
```

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

A few tests will actually connect directly to trello with your API key and server token to create a temporary board but this will be deleted as part of the test tear down. Other tests will just use dummy board data.


## Running in Vagrant
If you install Vagrant, you can run the application in its own vm. Just install Vagrant from https://www.vagrantup.com/docs/installation and then run the following command in the DevOps-Course-Starter direction
```bash
$ vagrant up
```

## Running in Docker
If you want to build and run a docker image of this application using a single stage DockerFile you can backup existing Dockerfile and rename Dockerfile.singlestage to Dockerfile and then run:
```bash
$ docker build --tag todo-app .
```

to build the application and then to run it run:
```bash
$ docker run -p 5000:5000 --env-file ./.env todo-app
```

You should then be able to see the application as usual at 127.0.0.1:5000


You will need to install Docker Desktop for Windows. 

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
$ docker run -p 5000:5000 --mount type=bind,source="C:\Projects\DevOps-Course-Starter\todo_app",target="/todo_app/todo_app" --env-file .env todo-app
```
This sets up the port forwarding and passes the .env file through to set up the flask environment paramenters. It also sets up a bind mount so that any changes in the source code will automatically be picked up with auto reload. 