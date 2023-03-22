FROM python:3.9

RUN mkdir -p /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install "poetry==1.3.2"
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

ADD fdk_rdf_parser_service /app/fdk_rdf_parser_service

EXPOSE 8000

CMD gunicorn "fdk_rdf_parser_service:create_app"  --config=fdk_rdf_parser_service/gunicorn_config.py --worker-class aiohttp.GunicornWebWorker
