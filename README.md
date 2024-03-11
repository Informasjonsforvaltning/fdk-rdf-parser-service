# fdk-rdf-parser-service

A Python service that parses RDF data to JSON and serves it to frontend applications.

## Developing

### Requirements

- [pyenv](https://github.com/pyenv/pyenv) (recommended)
- [poetry](https://python-poetry.org/)
- [nox](https://nox.thea.codes/en/stable/)
- [nox-poetry](https://pypi.org/project/nox-poetry/)

### Install software

```bash
pyenv install 3.11.8
pyenv local 3.11.8
pip install poetry==1.7.1
pip install nox==2024.3.2
pip install nox-poetry==1.0.3
poetry install
```

### Running the service locally

```bash
docker compose up -d
poetry shell
curl localhost:8080/ping
curl localhost:8080/ready
# Assuming you are in project root:
curl -X POST \
    --header "Content-Type: text/turtle X-API-KEY: test-key Accept: application/json" \
    --upload-file ./tests/data/dataset0.ttl \
    localhost:8080/dataset
```

## Testing

### Running tests

#### All tests

```bash
nox
```

#### Unit tests

```bash
nox -s unit_tests
```

#### Integration tests

```bash
nox -s integration_tests
```

#### Contract tests

```bash
nox -s contract_tests
```

#### Verbose mode

Verbose output from sessions for debugging

```bash
nox -s tests -- -vvv
```

### Other helpful commands

### Linter

```bash
nox -s lint
```

### Static type checking

```bash
nox -s mypy
```

#### Formatting

```bash
nox -s format
```

#### Clear py-cache

```bash
nox -s cache
```

#### Run tests outside of a nox session:

```bash
poetry run pytest
```

#### Run session with specified arguments:

```bash
nox -s tests -- -vv
```
