# Python: Rivian API Client

Currently a Work In Progress

## Dependencies

[uv](https://docs.astral.sh/uv/)

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Setup

Install project dependencies into the uv virtual environment and run pre-commit

```
uv sync --all-extras
pre-commit install
```

## Run Tests

```
uv run pytest
```
