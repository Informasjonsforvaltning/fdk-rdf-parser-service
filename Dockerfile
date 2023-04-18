FROM python:3.11

RUN mkdir -p /app
COPY ./ /app/
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir "poetry==1.4.2"

RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

EXPOSE 8000

CMD ./start_service.sh
