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

### Commands

`send_parallax_command` sends a signed command, such as unlocking
(`parallax.UNLOCK_RVM` with `parallax.encode_unlock()`; `LOCK_RVM` and
`encode_lock()` to lock), and `subscribe_for_parallax_command_state` follows it.
Subscribe first, then send:

```python
import uuid

from rivian import parallax


def on_state(data):
    if state := parallax.decode_command_state_message(data):
        print(state["progress"], state["status"], state["error"])


command_id = str(uuid.uuid4())
unsubscribe = await rivian.subscribe_for_parallax_command_state(
    vehicle_id, command_id, on_state
)
if unsubscribe:
    await rivian.send_parallax_command(
        vehicle_id,
        parallax.UNLOCK_RVM,
        parallax.encode_unlock(),
        identity_id=identity_id,
        vehicle_key=vehicle_key,
        private_key=private_key,
        command_id=command_id,
    )
    ...  # wait for the progress "complete", or give up
    await unsubscribe()
```

The keys are those of `send_vehicle_command`. The command is done when the progress
is `complete`, the status `success` and there is no `error`. If you never see that,
check the vehicle before sending it again. This unlocks a real vehicle, so keep the
keys secret.
