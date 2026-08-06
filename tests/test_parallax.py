"""Tests for the Parallax protobuf decoder."""

from __future__ import annotations

import base64
import struct
from typing import Any

import pytest

from rivian.parallax import (
    CHARGING_RVMS,
    PARALLAX_RVMS,
    _decode_protobuf_fields,
    _decode_varint,
    decode_battery_state,
    decode_cabin_temperatures,
    decode_charge_session_breakdown,
    decode_charging_graph_global,
    decode_charging_session_status,
    decode_closures,
    decode_defrost,
    decode_gnss,
    decode_locks,
    decode_odometer,
    decode_parallax_message,
    decode_power_state,
    decode_preconditioning,
    decode_time_estimation,
    decode_tires,
)


def test_decode_varint_single_byte() -> None:
    """Test decoding single byte varints."""
    val, offset = _decode_varint(b"\x00", 0)
    assert val == 0
    assert offset == 1

    val, offset = _decode_varint(b"\x01", 0)
    assert val == 1
    assert offset == 1

    val, offset = _decode_varint(b"\x7f", 0)
    assert val == 127
    assert offset == 1


def test_decode_varint_multi_byte() -> None:
    """Test decoding multi-byte varints (e.g. 300 = 0xAC 0x02)."""
    data = b"\xac\x02"
    val, offset = _decode_varint(data, 0)
    assert val == 300
    assert offset == 2


def test_decode_protobuf_fields_varint() -> None:
    """Test field decoding for wire type 0 (varint)."""
    # field 1 (tag = 1<<3 | 0 = 8), value = 150 (0x96 0x01)
    raw = b"\x08\x96\x01"
    fields = _decode_protobuf_fields(raw)
    assert len(fields) == 1
    assert fields[0] == (1, 0, 150)


def test_decode_protobuf_fields_fixed64() -> None:
    """Test field decoding for wire type 1 (64-bit float)."""
    # field 2 (tag = 2<<3 | 1 = 17), value = 111.52 (float)
    packed_float = struct.pack("<d", 111.52)
    raw = b"\x11" + packed_float
    fields = _decode_protobuf_fields(raw)
    assert len(fields) == 1
    field_num, wire_type, val = fields[0]
    assert field_num == 2
    assert wire_type == 1
    assert val == pytest.approx(111.52, abs=1e-4)


def test_decode_protobuf_fields_fixed32() -> None:
    """Test field decoding for wire type 5 (32-bit float)."""
    # field 9 (tag = 9<<3 | 5 = 77), value = 5.75 (float)
    packed_float = struct.pack("<f", 5.75)
    raw = bytes([77]) + packed_float
    fields = _decode_protobuf_fields(raw)
    assert len(fields) == 1
    field_num, wire_type, val = fields[0]
    assert field_num == 9
    assert wire_type == 5
    assert val == pytest.approx(5.75, abs=0.01)


def test_decode_protobuf_fields_length_delimited() -> None:
    """Test field decoding for wire type 2 (length-delimited)."""
    # field 3 (tag = 3<<3 | 2 = 26), length = 4, value = b"test"
    raw = b"\x1a\x04test"
    fields = _decode_protobuf_fields(raw)
    assert len(fields) == 1
    assert fields[0] == (3, 2, b"test")


def test_decode_protobuf_truncated_data() -> None:
    """Test graceful handling of truncated protobuf data."""
    # tag indicates 64-bit float, but only 2 bytes follow
    raw = b"\x11\x00\x00"
    fields = _decode_protobuf_fields(raw)
    assert fields == []


def test_decode_battery_state() -> None:
    """Test energy.high_voltage.battery_state decoder."""
    # Nested message: inner field 1 (soc=79.1 float), inner field 2 (capacity=111.52 float)
    inner = b"\x09" + struct.pack("<d", 79.1) + b"\x11" + struct.pack("<d", 111.52)
    # Outer message: field 1 (tag 10), length of inner
    outer = bytes([10, len(inner)]) + inner
    payload_b64 = base64.b64encode(outer).decode()

    result = decode_battery_state(payload_b64)
    assert result.get("soc") == 79.1
    assert result.get("packEnergyKwh") == 111.52


def test_decode_battery_state_empty_and_corrupt() -> None:
    """Test battery_state decoder on empty and corrupt inputs."""
    assert decode_battery_state("") == {}
    assert decode_battery_state("not-valid-base64!") == {}


def test_decode_charge_session_breakdown() -> None:
    """Test energy_edge_compute.graphs.charge_session_breakdown decoder."""
    # field 1 = totalKwh (float: 0.6), field 9 = power (float: 5.7)
    raw = bytes([13]) + struct.pack("<f", 0.6) + bytes([77]) + struct.pack("<f", 5.7)
    payload_b64 = base64.b64encode(raw).decode()

    result = decode_charge_session_breakdown(payload_b64)
    assert result.get("totalChargedEnergy") == 0.6
    assert result.get("power") == 5.7
    assert result.get("rangeAddedThisSession") == round(0.6 * 3.5, 1)
    assert result.get("kilometersChargedPerHour") == round(5.7 * 3.5, 1)


def test_decode_charging_graph_global() -> None:
    """Test energy_edge_compute.graphs.charging_graph_global decoder."""
    # Segment 1: start_ms=1785695977217, power=5.8, end_ms=1785696037217
    seg1 = (
        b"\x08\x48"  # field 1: soc = 72
        + bytes([21])
        + struct.pack("<f", 5.8)  # field 2: power = 5.8
        + b"\x18\x81\xfe\x98\x9e\xfc3"  # field 3: start_ms = 1785695977217
        + b"\x20\xe1\xd2\x9c\x9e\xfc3"  # field 4: end_ms = 1785696037217
    )
    outer = bytes([10, len(seg1)]) + seg1
    payload_b64 = base64.b64encode(outer).decode()

    result = decode_charging_graph_global(payload_b64)
    assert "startTime" in result
    assert result.get("timeElapsed") == 60
    assert result.get("power") == 5.8


def test_decode_charging_graph_global_stopped_state() -> None:
    """Test energy_edge_compute.graphs.charging_graph_global decoder when charging stops."""
    # Active Segment 1: 1785695977217 -> 1785696037217 (60s, 5.8 kW, state=3)
    seg1 = (
        b"\x08\x48"  # field 1: soc = 72
        + bytes([21])
        + struct.pack("<f", 5.8)  # field 2: power = 5.8
        + b"\x18\x81\xfe\x98\x9e\xfc3"  # field 3: start_ms = 1785695977217
        + b"\x20\xe1\xd2\x9c\x9e\xfc3"  # field 4: end_ms = 1785696037217
        + b"\x30\x03"  # field 6: state = 3 (charging)
    )
    # Idle Segment 2: 1785696037217 -> 1785696637217 (600s later, state=8, no power)
    seg2 = (
        b"\x08\x48"  # field 1: soc = 72
        + b"\x18\xe1\xd2\x9c\x9e\xfc3"  # field 3: start_ms = 1785696037217
        + b"\x20\xa1\xa9\xb8\x9e\xfc3"  # field 4: end_ms = 1785696637217
        + b"\x30\x08"  # field 6: state = 8 (suspended/stopped)
    )
    outer = bytes([10, len(seg1)]) + seg1 + bytes([10, len(seg2)]) + seg2
    payload_b64 = base64.b64encode(outer).decode()

    result = decode_charging_graph_global(payload_b64)
    # timeElapsed must reflect active charge time (60s), not total plugged in time (660s)
    assert result.get("timeElapsed") == 60
    assert result.get("power") == 0.0
    assert result.get("kilometersChargedPerHour") == 0.0


def test_decode_charging_session_status() -> None:
    """Test charging.session.status decoder."""
    # field 1 = plugConnectionStatus (1), field 2 = displayStatus (3), field 3 = evseType (2)
    raw = b"\x08\x01\x10\x03\x18\x02"
    payload_b64 = base64.b64encode(raw).decode()

    result = decode_charging_session_status(payload_b64)
    assert result.get("plugConnectionStatus") == 1
    assert result.get("displayStatus") == 3
    assert result.get("evseType") == 2


def test_decode_time_estimation() -> None:
    """Test charging.session.time_estimation decoder."""
    # field 1 = timeToEndOfCharge (3600 seconds) -> tag 8, varint 3600 (0x90 0x1c)
    raw = b"\x08\x90\x1c"
    payload_b64 = base64.b64encode(raw).decode()

    result = decode_time_estimation(payload_b64)
    assert result.get("timeToEndOfCharge") == 3600


def test_decode_odometer() -> None:
    """Test dynamics.vehicle.odometer decoder."""
    # field 1 = varint 17114 (miles) -> converted to meters
    # 17114 = 0xda 0x85 0x01 -> tag 1<<3|0 = 8 -> b"\x08\xda\x85\x01"
    raw = b"\x08\xda\x85\x01"
    payload_b64 = base64.b64encode(raw).decode()

    result = decode_odometer(payload_b64)
    expected_meters = round(17114 * 1609.344, 1)
    assert result.get("vehicleMileage") == expected_meters


def test_decode_tires() -> None:
    """Test dynamics.tires.state decoder."""
    # Nested tire: pos=1 (FL), status=1 (Ok), pressure=3.48 (float)
    inner = (
        b"\x08\x01"  # field 1 = 1 (FL)
        + b"\x10\x01"  # field 2 = 1 (status Ok)
        + b"\x19"
        + struct.pack("<d", 3.48)  # field 3 = 3.48 (float)
    )
    outer = bytes([18, len(inner)]) + inner
    payload_b64 = base64.b64encode(outer).decode()

    result = decode_tires(payload_b64)
    assert result.get("tirePressureFrontLeft") == 3.48
    assert result.get("tirePressureStatusFrontLeft") == "Ok"


def test_decode_closures() -> None:
    """Test body.closures.states decoder."""
    # Closure 1 (FL door, state 2=closed), Closure 5 (Frunk, state 1=open)
    inner1 = b"\x08\x01\x10\x02"  # id 1, state 2 (closed)
    inner2 = b"\x08\x05\x10\x01"  # id 5, state 1 (open)
    outer = bytes([10, len(inner1)]) + inner1 + bytes([10, len(inner2)]) + inner2
    payload_b64 = base64.b64encode(outer).decode()

    result = decode_closures(payload_b64)
    assert result.get("doorFrontLeftClosed") == "closed"
    assert result.get("closureFrunkClosed") == "open"


def test_decode_locks() -> None:
    """Test body.locks.states decoder."""
    # Lock 1 (FL door, state 2=locked), Lock 2 (FR door, state 1=unlocked)
    inner1 = b"\x08\x01\x10\x02"
    inner2 = b"\x08\x02\x10\x01"
    outer = bytes([10, len(inner1)]) + inner1 + bytes([10, len(inner2)]) + inner2
    payload_b64 = base64.b64encode(outer).decode()

    result = decode_locks(payload_b64)
    assert result.get("doorFrontLeftLocked") == "locked"
    assert result.get("doorFrontRightLocked") == "unlocked"


def test_decode_cabin_temperatures() -> None:
    """Test comfort.cabin.cabin_temperatures decoder."""
    # field 4 (tag 4<<3|5 = 37), float 23.5
    raw = bytes([37]) + struct.pack("<f", 23.5)
    payload_b64 = base64.b64encode(raw).decode()

    result = decode_cabin_temperatures(payload_b64)
    assert result.get("cabinClimateInteriorTemperature") == 23.5


def test_decode_power_state() -> None:
    """Test vehicle.power.state decoder."""
    # field 1 = 4 (go / drive)
    raw = b"\x08\x04"
    payload_b64 = base64.b64encode(raw).decode()
    result = decode_power_state(payload_b64)
    assert result.get("powerState") == "go"

    # field 1 = 1 (sleep)
    raw_sleep = b"\x08\x01"
    payload_b64_sleep = base64.b64encode(raw_sleep).decode()
    result_sleep = decode_power_state(payload_b64_sleep)
    assert result_sleep.get("powerState") == "sleep"


def test_decode_gnss() -> None:
    """Test dynamics.vehicle.gnss decoder."""
    # field 1 = lat (33.0834), field 2 = lon (-80.1465)
    raw = b"\x09" + struct.pack("<d", 33.0834) + b"\x11" + struct.pack("<d", -80.1465)
    payload_b64 = base64.b64encode(raw).decode()
    result = decode_gnss(payload_b64)
    assert "gnssLocation" in result
    assert result["gnssLocation"]["latitude"] == 33.0834
    assert result["gnssLocation"]["longitude"] == -80.1465


def test_decode_preconditioning() -> None:
    """Test comfort.cabin.cabin_preconditioning_status decoder."""
    # field 1 = 4 (active)
    raw_active = b"\x08\x04"
    res_active = decode_preconditioning(base64.b64encode(raw_active).decode())
    assert res_active.get("cabinPreconditioningStatus") == "active"

    # field 1 = 1 (initiate)
    raw_init = b"\x08\x01"
    res_init = decode_preconditioning(base64.b64encode(raw_init).decode())
    assert res_init.get("cabinPreconditioningStatus") == "initiate"

    # empty payload (off)
    res_off = decode_preconditioning("")
    assert res_off.get("cabinPreconditioningStatus") == "off"


def test_decode_defrost() -> None:
    """Test comfort.cabin.defrost_defog_status decoder."""
    # field 1 = 2 (Defrost)
    raw_defrost = b"\x08\x02"
    res_defrost = decode_defrost(base64.b64encode(raw_defrost).decode())
    assert res_defrost.get("defrostDefogStatus") == "Defrost"

    # field 1 = 4 (Off)
    raw_off = b"\x08\x04"
    res_off = decode_defrost(base64.b64encode(raw_off).decode())
    assert res_off.get("defrostDefogStatus") == "Off"


def test_decode_parallax_message_dispatch() -> None:
    """Test decode_parallax_message dispatching."""
    # Known topic
    raw = b"\x08\x90\x1c"
    payload_b64 = base64.b64encode(raw).decode()
    res = decode_parallax_message("charging.session.time_estimation", payload_b64)
    assert res is not None
    assert res.get("timeToEndOfCharge") == 3600

    # Dict unpacking as received from GraphQL subscription (rvm, payload, timestamp)
    message: dict[str, Any] = {
        "rvm": "charging.session.time_estimation",
        "payload": payload_b64,
        "timestamp": "2026-08-05T20:00:00.000Z",
        "extra_field": 123,
    }
    res_unpacked = decode_parallax_message(**message)
    assert res_unpacked is not None
    assert res_unpacked.get("timeToEndOfCharge") == 3600

    # Odometer topic
    raw_odo = b"\x08\xda\x85\x01"
    b64_odo = base64.b64encode(raw_odo).decode()
    res_odo = decode_parallax_message("dynamics.vehicle.odometer", b64_odo)
    assert res_odo is not None
    assert "vehicleMileage" in res_odo

    # GNSS topic
    raw_gnss = (
        b"\x09" + struct.pack("<d", 33.0834) + b"\x11" + struct.pack("<d", -80.1465)
    )
    b64_gnss = base64.b64encode(raw_gnss).decode()
    res_gnss = decode_parallax_message("dynamics.vehicle.gnss", b64_gnss)
    assert res_gnss is not None
    assert "gnssLocation" in res_gnss

    # Unknown topic
    unknown = decode_parallax_message("unknown.topic.rvm", payload_b64)
    assert unknown is None


def test_registered_charging_rvms() -> None:
    """Verify standard charging RVM topics are defined."""
    assert "energy.high_voltage.battery_state" in CHARGING_RVMS
    assert "energy_edge_compute.graphs.charge_session_breakdown" in CHARGING_RVMS
    assert "charging.session.status" in CHARGING_RVMS
    assert "charging.session.time_estimation" in CHARGING_RVMS
    assert "charging.session.soc_slider" in CHARGING_RVMS
    assert "dynamics.vehicle.odometer" in PARALLAX_RVMS
    assert "dynamics.tires.state" in PARALLAX_RVMS
    assert "dynamics.vehicle.gnss" in PARALLAX_RVMS
    assert "comfort.cabin.cabin_preconditioning_status" in PARALLAX_RVMS
    assert "comfort.cabin.defrost_defog_status" in PARALLAX_RVMS
