FROM python:3.11

RUN mkdir -p /app
COPY fdk_rdf_parser_service poetry.lock pyproject.toml /app/
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir "poetry==1.4.2"

RUN poetry install --no-dev --no-interaction --no-ansi

EXPOSE 8080

CMD ["poetry", "run", "python", "-u", "fdk_rdf_parser_service/app.py"]
