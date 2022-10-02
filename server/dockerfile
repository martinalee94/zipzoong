FROM python:3.9-buster

# Locale 설정
ENV LANG ko_KR.UTF-8
ENV LC_ALL ko_KR.UTF-8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.2
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_CACHE_DIR='/var/cache/pypoetry'

WORKDIR /usr/src/app

COPY . .


RUN pip3 install --upgrade pip
RUN pip3 install "poetry==$POETRY_VERSION"
RUN poetry install --no-dev --no-interaction --no-ansi

EXPOSE 8000