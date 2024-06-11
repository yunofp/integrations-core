FROM --platform=linux/amd64 python:3.9

WORKDIR /api-flask

COPY.env /api-flask/
COPY app.log /api-flask/
COPY pytest.ini /api-flask/
COPY requirements.txt /api-flask/
COPY application/ /api-flask/application/

ARG DOCKER_SETTINGS_TOML
RUN cp $DOCKER_SETTINGS_TOML /api-flask/settings.toml

RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt

EXPOSE 3000

CMD ["waitress-serve", "--listen=*:3000", "application.app:app"]
