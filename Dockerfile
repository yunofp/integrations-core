FROM --platform=linux/amd64 python:3.9

WORKDIR /api-flask

ENV TZ=America/Sao_Paulo

RUN apt-get update && \
    apt-get install -y tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone

COPY .env /api-flask/
COPY pytest.ini /api-flask/
COPY requirements.txt /api-flask/
COPY application/ /api-flask/application/

ARG DOCKER_SETTINGS_TOML
COPY ${DOCKER_SETTINGS_TOML} /api-flask/settings.toml

RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt

EXPOSE 3000

CMD ["waitress-serve", "--listen=*:3000", "application.app:app"]
