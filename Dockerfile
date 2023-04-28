FROM python:3.11

RUN pip install --upgrade pip
RUN pip install --no-cache-dir "poetry==1.4.2"

RUN mkdir -p /app
WORKDIR /app

COPY poetry.lock ./poetry.lock
COPY pyproject.toml ./pyproject.toml
COPY README.md ./README.md

COPY fdk_rdf_parser_service/ ./fdk_rdf_parser_service/

RUN poetry install --no-dev --no-interaction --no-ansi

EXPOSE 8080

CMD [ "poetry", "run", "python", "-u", "./fdk_rdf_parser_service/app.py" ]
