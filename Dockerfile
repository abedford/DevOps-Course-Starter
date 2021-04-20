# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster as python-base

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1 \
# Turns off buffering for easier container logging
PYTHONUNBUFFERED=1 \
POETRY_VERSION=1.0.0 \
 # make poetry install to this location
POETRY_HOME="/poetry"


# `builder-base` stage is used to build deps 
FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        # deps for installing poetry
        curl \
        # deps for building python deps
        build-essential

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
WORKDIR /todo_app
COPY poetry.lock pyproject.toml /todo_app/

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN poetry config virtualenvs.create false \
  && poetry install --no-dev  --no-interaction --no-ansi

FROM builder-base as production
COPY ./todo_app /todo_app/todo_app
EXPOSE 5000
CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:5000", "todo_app.wsgi:wsgi_app", "--log-file", "gunicorn_logs_docker.txt" ]


FROM builder-base as development
COPY ./todo_app /todo_app/todo_app
EXPOSE 5000
CMD ["poetry", "run", "flask", "run", "--host", "0.0.0.0" ]
