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

## Parallax

`subscribe_for_parallax_messages` streams the vehicle's Parallax RVM topics,
whose payloads are protobuf. `rivian.parallax` decodes them into dicts keyed
like the GraphQL vehicle state where a matching property exists:

```python
from rivian import parallax


def on_message(data):
    if decoded := parallax.decode_parallax_subscription_message(data):
        print(decoded)
```

`parallax.PARALLAX_RVMS` lists every topic with a decoder, and
`parallax.CHARGING_RVMS` the ones relevant to a charging session.

The schemas in `src/rivian/parallax/proto/*.proto` are reverse-engineered. After
editing one, regenerate its `*_pb2` modules (don't edit those by hand):

```
uv run python -m grpc_tools.protoc --proto_path=src --python_out=src \
    --pyi_out=src src/rivian/parallax/proto/*.proto
```
