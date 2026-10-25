"""Wait for a signed command's vehicle acknowledgement without retrying it."""

import asyncio
import logging
import uuid

from .command import decode_command_state_message

_LOGGER = logging.getLogger(__name__)


class ParallaxExecutionError(Exception):
    """The command failed or its execution could not be confirmed."""


async def execute_command(
    api,
    vehicle_id,
    rvm,
    payload,
    *,
    identity_id,
    vehicle_key,
    private_key,
    timeout=120.0,
):
    """Subscribe first, send once, and require the vehicle's successful completion.

    A timeout is an unknown outcome; callers must not retry or fall back silently.
    Exception messages intentionally exclude credentials and raw server responses.
    """
    command_id = str(uuid.uuid4())
    result = asyncio.get_running_loop().create_future()

    def on_state(data):
        state = decode_command_state_message(data)
        if (
            not state
            or state["commandId"] != command_id
            or state["rvm"] != rvm
            or result.done()
        ):
            return
        if state["error"] is not None or state["progress"] == "complete":
            result.set_result(state)

    unsubscribe = None
    submitted = False
    try:
        async with asyncio.timeout(timeout):
            unsubscribe = await api.subscribe_for_parallax_command_state(
                vehicle_id, command_id, on_state
            )
            if unsubscribe is None:
                raise ParallaxExecutionError(
                    "Status subscription unavailable; command not sent"
                )
            submitted = True
            accepted = await api.send_parallax_command(
                vehicle_id,
                rvm,
                payload,
                identity_id=identity_id,
                vehicle_key=vehicle_key,
                private_key=private_key,
                command_id=command_id,
            )
            if accepted != command_id:
                raise ParallaxExecutionError(
                    "Cloud acceptance not confirmed; execution unknown"
                )
            state = await result
            if state["error"] is not None or state["status"] != "success":
                status = state["status"]
                known_statuses = {
                    "undefined",
                    "success",
                    "failed",
                    "invalid_request",
                    "not_supported",
                    "timeout",
                }
                safe_status = (
                    status
                    if status in known_statuses or isinstance(status, int)
                    else "unknown"
                )
                error = state["error"]
                code = error.get("code") if isinstance(error, dict) else None
                safe_code = str(code) if isinstance(code, int) else "none"
                if status is None and error is not None:
                    raise ParallaxExecutionError(
                        f"Parallax operation error (error_code={safe_code}); "
                        "outcome unknown; command may have taken effect; "
                        "check vehicle before retrying"
                    )
                raise ParallaxExecutionError(
                    "Vehicle did not confirm successful execution "
                    f"(status={safe_status}, error_code={safe_code})"
                )
            return command_id
    except TimeoutError:
        raise ParallaxExecutionError(
            "Execution timed out; outcome unknown; check vehicle before retrying"
            if submitted
            else "Status subscription timed out; command not sent"
        ) from None
    except ParallaxExecutionError:
        raise
    except Exception:  # noqa: BLE001 -- sanitize transport exceptions at this boundary
        raise ParallaxExecutionError(
            "Command transport failed; execution unknown; check vehicle before retrying"
            if submitted
            else "Status subscription failed; command not sent"
        ) from None
    finally:
        if unsubscribe is not None:
            try:
                async with asyncio.timeout(5):
                    await unsubscribe()
            except Exception:  # noqa: BLE001 -- cleanup must not hide confirmed execution
                _LOGGER.warning("Parallax status subscription cleanup failed")
        if not result.done():
            result.cancel()
