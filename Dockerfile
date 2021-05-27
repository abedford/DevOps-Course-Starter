# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9-slim-buster as python-base

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1 \
# Turns off buffering for easier container logging
PYTHONUNBUFFERED=1 \
POETRY_VERSION=1.1.4 \
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


FROM builder-base as test
COPY ./todo_app /todo_app/todo_app

RUN apt-get update -qqy && apt-get install -qqy wget gnupg unzip
# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
  && apt-get update -qqy \
  && apt-get -qqy install google-chrome-stable \
  && rm /etc/apt/sources.list.d/google-chrome.list \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

# Install Chrome WebDriver
RUN CHROME_MAJOR_VERSION=$(google-chrome --version | sed -E "s/.* ([0-9]+)(\.[0-9]+){3}.*/\1/") \
  && CHROME_DRIVER_VERSION=$(wget --no-verbose -O - "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_MAJOR_VERSION}") \
  && echo "Using chromedriver version: "$CHROME_DRIVER_VERSION \
  && wget --no-verbose -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip \
  && unzip /tmp/chromedriver_linux64.zip -d /usr/bin \
  && rm /tmp/chromedriver_linux64.zip \
  && chmod 755 /usr/bin/chromedriver
ENTRYPOINT ["poetry", "run", "pytest"]