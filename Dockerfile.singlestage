# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ENV POETRY_VERSION=1.0.0

RUN pip install "poetry==$POETRY_VERSION"

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
WORKDIR /todo_app
COPY poetry.lock pyproject.toml /todo_app/



# Install pip requirements
#COPY requirements.txt .
#RUN python -m pip install -r requirements.txt
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi


#WORKDIR /todo_app
COPY . /todo_app

EXPOSE 5000
# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
#RUN useradd appuser && chown -R appuser /todo_app
#USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:5000", "todo_app.wsgi:wsgi_app",        "--log-file", "gunicorn_logs_docker.txt" ]
