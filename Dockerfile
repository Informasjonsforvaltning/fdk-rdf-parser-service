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

CMD [ "uvicorn", "fdk_rdf_parser_service.app:app", "--host", "0.0.0.0", "--port", "8080", "--no-use-colors", "--log-level", "warning" ] 
