ARG PYTHON_VERSION=3.11-slim-buster

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# RUN apt update
# RUN apt install -y gnupg wget lsb-release
# RUN cd /tmp
# RUN wget https://dev.mysql.com/get/mysql-apt-config_0.8.22-1_all.deb
# RUN dpkg -i mysql-apt-config*
# RUN apt update
# RUN apt install -y mysql-server

RUN mkdir -p /code

WORKDIR /code

RUN pip install poetry
COPY pyproject.toml poetry.lock /code/
RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-root --no-interaction
COPY . /code
RUN python /code/manage.py makemigrations
RUN python /code/manage.py migrate

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "conf.wsgi"]
