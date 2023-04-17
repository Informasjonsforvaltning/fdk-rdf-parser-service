FROM python:3.11

RUN mkdir -p /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install "poetry==1.4.1"
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

COPY ./fdk_rdf_parser_service /app/fdk_rdf_parser_service

EXPOSE 8000

COPY ./start_service.sh ./start_service.sh

ENV PYTHONPATH "${PYTHONPATH}:/app/fdk_rdf_parser_service"

CMD ./start_service.sh
