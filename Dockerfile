FROM python:3.11

RUN pip install --upgrade pip
RUN pip install --no-cache-dir "poetry==1.7.1"

RUN mkdir -p /app
WORKDIR /app

COPY poetry.lock pyproject.toml README.md ./

COPY fdk_rdf_parser_service/ ./fdk_rdf_parser_service/

RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

EXPOSE 8080

CMD [ "gunicorn", "fdk_rdf_parser_service.app:create_app", "--config=fdk_rdf_parser_service/gunicorn_config.py", "--worker-class", "aiohttp.GunicornWebWorker" ] 
