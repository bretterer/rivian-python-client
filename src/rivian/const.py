"""Rivian constants."""

from __future__ import annotations

import sys
from typing import Final

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from backports.strenum import StrEnum

LIVE_SESSION_PROPERTIES: Final[set[str]] = {
    "chargerId",
    "current",
    "currentCurrency",
    "currentMiles",
    "currentPrice",
    "isFreeSession",
    "isRivianCharger",
    "kilometersChargedPerHour",
    "locationId",
    "power",
    "rangeAddedThisSession",
    "soc",
    "startTime",
    "timeElapsed",
    "timeRemaining",
    "totalChargedEnergy",
    "vehicleChargerState",
}

VEHICLE_STATE_PROPERTIES: Final[set[str]] = {
    # VehicleCloudConnection
    "cloudConnection",
    # VehicleLocation
    "geoLocation",
    "gnssLocation",
    "gnssError",
    # TimeStamped(String|[Nullable]Float|Int)
    "activeDriverName",
    "alarmSoundStatus",
    "batteryCapacity",
    "batteryCellType",
    "batteryHvThermalEvent",
    "batteryHvThermalEventPropagation",
    "batteryLevel",
    "batteryLimit",
    "batteryNeedsLfpCalibration",
    "brakeFluidLow",
    "btmFfHardwareFailureStatus",
    "btmIcHardwareFailureStatus",
    "btmLfdHardwareFailureStatus",
    "btmOcHardwareFailureStatus",
    "btmRfdHardwareFailureStatus",
    "btmRfHardwareFailureStatus",
    "cabinClimateDriverTemperature",
    "cabinClimateInteriorTemperature",
    "cabinHoldNotification",
    "cabinHoldStatus",
    "cabinPreconditioningStatus",
    "cabinPreconditioningType",
    "carWashMode",
    "chargerDerateStatus",
    "chargerState",
    "chargerStatus",
    "chargePortState",
    "chargingDisabledAll",
    "closureFrunkClosed",
    "closureFrunkLocked",
    "closureFrunkNextAction",
    "closureLiftgateClosed",
    "closureLiftgateLocked",
    "closureLiftgateNextAction",
    "closureSideBinLeftClosed",
    "closureSideBinLeftLocked",
    "closureSideBinLeftNextAction",
    "closureSideBinRightClosed",
    "closureSideBinRightLocked",
    "closureSideBinRightNextAction",
    "closureTailgateClosed",
    "closureTailgateLocked",
    "closureTailgateNextAction",
    "closureTonneauClosed",
    "closureTonneauLocked",
    "closureTonneauNextAction",
    "defrostDefogStatus",
    "distanceToEmpty",
    "doorFrontLeftClosed",
    "doorFrontLeftLocked",
    "doorFrontRightClosed",
    "doorFrontRightLocked",
    "doorRearLeftClosed",
    "doorRearLeftLocked",
    "doorRearRightClosed",
    "doorRearRightLocked",
    "driveMode",
    "gearGuardLocked",
    "gearGuardVideoMode",
    "gearGuardVideoStatus",
    "gearGuardVideoTermsAccepted",
    "gearStatus",
    "gnssAltitude",
    "gnssBearing",
    "gnssSpeed",
    "limitedRegenCold",
    "limitedAccelCold",
    "otaAvailableVersion",
    "otaAvailableVersionGitHash",
    "otaAvailableVersionNumber",
    "otaAvailableVersionWeek",
    "otaAvailableVersionYear",
    "otaCurrentStatus",
    "otaCurrentVersion",
    "otaCurrentVersionGitHash",
    "otaCurrentVersionNumber",
    "otaCurrentVersionWeek",
    "otaCurrentVersionYear",
    "otaDownloadProgress",
    "otaInstallDuration",
    "otaInstallProgress",
    "otaInstallReady",
    "otaInstallTime",
    "otaInstallType",
    "otaStatus",
    "petModeStatus",
    "petModeTemperatureStatus",
    "powerState",
    "rangeThreshold",
    "rearHitchStatus",
    "remoteChargingAvailable",
    "seatFrontLeftHeat",
    "seatFrontLeftVent",
    "seatFrontRightHeat",
    "seatFrontRightVent",
    "seatRearLeftHeat",
    "seatRearRightHeat",
    "seatThirdRowLeftHeat",
    "seatThirdRowRightHeat",
    "serviceMode",
    "steeringWheelHeat",
    "timeToEndOfCharge",
    "tirePressureStatusFrontLeft",
    "tirePressureStatusFrontRight",
    "tirePressureStatusRearLeft",
    "tirePressureStatusRearRight",
    "tirePressureStatusValidFrontLeft",
    "tirePressureStatusValidFrontRight",
    "tirePressureStatusValidRearLeft",
    "tirePressureStatusValidRearRight",
    "trailerStatus",
    "twelveVoltBatteryHealth",
    "vehicleMileage",
    "windowFrontLeftCalibrated",
    "windowFrontLeftClosed",
    "windowFrontRightCalibrated",
    "windowFrontRightClosed",
    "windowRearLeftCalibrated",
    "windowRearLeftClosed",
    "windowRearRightCalibrated",
    "windowRearRightClosed",
    "windowsNextAction",
    "wiperFluidState",
}

VEHICLE_STATES_SUBSCRIPTION_ONLY_PROPERTIES: Final[set[str]] = {
    # TimeStamped(String|[Nullable]Float|Int)
    "activeDriverName",
    "chargingDisabledACFaultState",
    "chargingTimeEstimationValidity",
    "chargingTripTargetSoc",
    "chargingTripTargetMinsRemaining",
    "closureChargePortDoorNextAction",
    "coldRangeNotification",
    "tirePressureFrontLeft",
    "tirePressureFrontRight",
    "tirePressureRearLeft",
    "tirePressureRearRight",
}

VEHICLE_STATES_SUBSCRIPTION_PROPERTIES = (
    VEHICLE_STATE_PROPERTIES | VEHICLE_STATES_SUBSCRIPTION_ONLY_PROPERTIES
)


class VehicleCommand(StrEnum):
    """Supported vehicle commands."""

    WAKE_VEHICLE = "WAKE_VEHICLE"
    UNLOCK_USER_PREFERENCES_AND_DISABLE_ALARM = (
        "UNLOCK_USER_PREFERENCES_AND_DISABLE_ALARM"
    )

    HONK_AND_FLASH_LIGHTS = "HONK_AND_FLASH_LIGHTS"
    ACTIVATE_EXTERNAL_SOUND = "ACTIVATE_EXTERNAL_SOUND"
    FLASH_EXTERNAL_LIGHTS = "FLASH_EXTERNAL_LIGHTS"

    # Charging
    CHARGING_LIMITS = "CHARGING_LIMITS"
    START_CHARGING = "START_CHARGING"
    STOP_CHARGING = "STOP_CHARGING"

    # Climate
    CABIN_HVAC_DEFROST_DEFOG = "CABIN_HVAC_DEFROST_DEFOG"
    CABIN_HVAC_LEFT_SEAT_HEAT = "CABIN_HVAC_LEFT_SEAT_HEAT"
    CABIN_HVAC_LEFT_SEAT_VENT = "CABIN_HVAC_LEFT_SEAT_VENT"
    CABIN_HVAC_REAR_LEFT_SEAT_HEAT = "CABIN_HVAC_REAR_LEFT_SEAT_HEAT"
    CABIN_HVAC_REAR_RIGHT_SEAT_HEAT = "CABIN_HVAC_REAR_RIGHT_SEAT_HEAT"
    CABIN_HVAC_RIGHT_SEAT_HEAT = "CABIN_HVAC_RIGHT_SEAT_HEAT"
    CABIN_HVAC_RIGHT_SEAT_VENT = "CABIN_HVAC_RIGHT_SEAT_VENT"
    CABIN_HVAC_STEERING_HEAT = "CABIN_HVAC_STEERING_HEAT"
    CABIN_PRECONDITIONING_SET_TEMP = "CABIN_PRECONDITIONING_SET_TEMP"
    CLIMATE_HOLD_OFF = "CLIMATE_HOLD_OFF"
    CLIMATE_HOLD_ON = "CLIMATE_HOLD_ON"
    VEHICLE_CABIN_PRECONDITION_DISABLE = "VEHICLE_CABIN_PRECONDITION_DISABLE"
    VEHICLE_CABIN_PRECONDITION_ENABLE = "VEHICLE_CABIN_PRECONDITION_ENABLE"
    # Gen2 HVAC Controls
    CABIN_HVAC_THIRD_ROW_LEFT_SEAT_HEAT = "CABIN_HVAC_THIRD_ROW_LEFT_SEAT_HEAT"
    CABIN_HVAC_THIRD_ROW_RIGHT_SEAT_HEAT = "CABIN_HVAC_THIRD_ROW_RIGHT_SEAT_HEAT"

    # Closures
    LOCK_ALL_CLOSURES_FEEDBACK = "LOCK_ALL_CLOSURES_FEEDBACK"
    UNLOCK_ALL_CLOSURES = "UNLOCK_ALL_CLOSURES"
    UNLOCK_DRIVER_DOOR = "UNLOCK_DRIVER_DOOR"
    UNLOCK_PASSENGER_DOOR = "UNLOCK_PASSENGER_DOOR"

    # Frunk
    CLOSE_FRUNK = "CLOSE_FRUNK"
    OPEN_FRUNK = "OPEN_FRUNK"

    # Gear guard
    ENABLE_GEAR_GUARD = "ENABLE_GEAR_GUARD"
    ENABLE_GEAR_GUARD_VIDEO = "ENABLE_GEAR_GUARD_VIDEO"
    DISABLE_GEAR_GUARD = "DISABLE_GEAR_GUARD"
    DISABLE_GEAR_GUARD_VIDEO = "DISABLE_GEAR_GUARD_VIDEO"

    # Liftgate (R1S only)
    CLOSE_LIFTGATE = "CLOSE_LIFTGATE"

    # Liftgate/tailgate
    OPEN_LIFTGATE_UNLATCH_TAILGATE = "OPEN_LIFTGATE_UNLATCH_TAILGATE"

    # Chargeport door
    OPEN_CHARGE_PORT_DOOR = "OPEN_CHARGE_PORT_DOOR"
    CLOSE_CHARGE_PORT_DOOR = "CLOSE_CHARGE_PORT_DOOR"

    # OTA
    OTA_INSTALL_NOW_ACKNOWLEDGE = "OTA_INSTALL_NOW_ACKNOWLEDGE"

    # Panic
    PANIC_OFF = "PANIC_OFF"
    PANIC_ON = "PANIC_ON"

    # Side bin (R1T only)
    RELEASE_LEFT_SIDE_BIN = "RELEASE_LEFT_SIDE_BIN"
    RELEASE_RIGHT_SIDE_BIN = "RELEASE_RIGHT_SIDE_BIN"

    # Tonneau (Only for R1T with powered tonneau)
    CLOSE_TONNEAU_COVER = "CLOSE_TONNEAU_COVER"
    OPEN_TONNEAU_COVER = "OPEN_TONNEAU_COVER"

    # Windows
    CLOSE_ALL_WINDOWS = "CLOSE_ALL_WINDOWS"
    OPEN_ALL_WINDOWS = "OPEN_ALL_WINDOWS"
    UNLOCK_ALL_AND_OPEN_WINDOWS = "UNLOCK_ALL_AND_OPEN_WINDOWS"
