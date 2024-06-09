"""Response tests data."""

from __future__ import annotations

import json
import os
from typing import Any

AUTHENTICATION_RESPONSE = {
    "data": {
        "login": {
            "__typename": "MobileLoginResponse",
            "accessToken": "valid_access_token",
            "refreshToken": "valid_refresh_token",
            "userSessionToken": "valid_user_session_token",
        }
    }
}
AUTHENTICATION_OTP_RESPONSE = {
    "data": {
        "loginWithOTP": {
            "__typename": "MobileLoginResponse",
            "accessToken": "token",
            "refreshToken": "token",
            "userSessionToken": "token",
        }
    }
}
CSRF_TOKEN_RESPONSE = {
    "data": {
        "createCsrfToken": {
            "__typename": "CreateCsrfTokenResponse",
            "csrfToken": "valid_csrf_token",
            "appSessionToken": "valid_app_session_token",
        }
    }
}
LIVE_CHARGING_SESSION_RESPONSE = {
    "data": {
        "getLiveSessionData": {
            "isRivianCharger": None,
            "isFreeSession": None,
            "vehicleChargerState": {
                "__typename": "StringValueRecord",
                "value": "charging_active",
                "updatedAt": "2022-10-27T21:25:16.226Z",
            },
            "chargerId": None,
            "startTime": "2022-10-27T20:48:27.222Z",
            "timeElapsed": "2229",
            "timeRemaining": {
                "__typename": "StringValueRecord",
                "value": "9651",
                "updatedAt": "2022-10-27T21:25:27.222Z",
            },
            "kilometersChargedPerHour": {
                "__typename": "FloatValueRecord",
                "value": 32,
                "updatedAt": "2022-10-27T21:25:25.149Z",
            },
            "power": {
                "__typename": "FloatValueRecord",
                "value": 9,
                "updatedAt": "2022-10-27T21:25:16.226Z",
            },
            "rangeAddedThisSession": {
                "__typename": "FloatValueRecord",
                "value": 20,
                "updatedAt": "2022-10-27T21:25:25.149Z",
            },
            "totalChargedEnergy": {
                "__typename": "FloatValueRecord",
                "value": 6,
                "updatedAt": "2022-10-27T21:25:16.226Z",
            },
            "currentPrice": None,
        }
    }
}
OTP_TOKEN_RESPONSE = {
    "data": {
        "login": {
            "__typename": "MobileMFALoginResponse",
            "otpToken": "token",
        }
    }
}
USER_INFORMATION_RESPONSE = {
    "data": {
        "currentUser": {
            "__typename": "User",
            "id": "id",
            "firstName": "firstName",
            "lastName": "lastName",
            "email": "email",
            "vehicles": [
                {
                    "__typename": "UserVehicle",
                    "id": "id",
                    "owner": None,
                    "roles": ["primary-owner"],
                    "name": "R1T",
                    "vin": "vin",
                    "vas": {
                        "__typename": "UserVehicleAccess",
                        "vasVehicleId": "vasVehicleId",
                        "vehiclePublicKey": "vehiclePublicKey",
                    },
                    "vehicle": {
                        "__typename": "Vehicle",
                        "model": "R1T",
                        "mobileConfiguration": {
                            "__typename": "VehicleMobileConfiguration",
                            "trimOption": {
                                "__typename": "VehicleMobileConfigurationOption",
                                "optionId": "PKG-ADV",
                                "optionName": "Adventure Package",
                            },
                            "exteriorColorOption": {
                                "__typename": "VehicleMobileConfigurationOption",
                                "optionId": "EXP-LST",
                                "optionName": "Limestone",
                            },
                            "interiorColorOption": {
                                "__typename": "VehicleMobileConfigurationOption",
                                "optionId": "INT-GYP",
                                "optionName": "Ocean Coast + Dark Ash Wood",
                            },
                        },
                        "vehicleState": {
                            "__typename": "VehicleState",
                            "supportedFeatures": [
                                {
                                    "__typename": "SupportedFeature",
                                    "name": "ADDR_SHR",
                                    "status": "AVAILABLE",
                                },
                                {
                                    "__typename": "SupportedFeature",
                                    "name": "ADDR_SHR_YLP",
                                    "status": "AVAILABLE",
                                },
                                {
                                    "__typename": "SupportedFeature",
                                    "name": "CHARG_CMD",
                                    "status": "AVAILABLE",
                                },
                                {
                                    "__typename": "SupportedFeature",
                                    "name": "CHARG_SCHED",
                                    "status": "AVAILABLE",
                                },
                                {
                                    "__typename": "SupportedFeature",
                                    "name": "CHARG_SLIDER",
                                    "status": "AVAILABLE",
                                },
                                {
                                    "__typename": "SupportedFeature",
                                    "name": "DEFROST_DEFOG",
                                    "status": "AVAILABLE",
                                },
                                {
                                    "__typename": "SupportedFeature",
                                    "name": "FRUNK_NXT_ACT",
                                    "status": "AVAILABLE",
                                },
                                {
                                    "__typename": "SupportedFeature",
                                    "name": "GEAR_GUARD_VIDEO_SETTING",
                                    "status": "AVAILABLE",
                                },
                                {
                                    "__typename": "SupportedFeature",
                                    "name": "SIDE_BIN_NXT_ACT",
                                    "status": "AVAILABLE",
                                },
                                {
                                    "__typename": "SupportedFeature",
                                    "name": "HEATED_SEATS",
                                    "status": "AVAILABLE",
                                },
                                {
                                    "__typename": "SupportedFeature",
                                    "name": "HEATED_WHEEL",
                                    "status": "AVAILABLE",
                                },
                                {
                                    "__typename": "SupportedFeature",
                                    "name": "RENAME_VEHICLE",
                                    "status": "AVAILABLE",
                                },
                                {
                                    "__typename": "SupportedFeature",
                                    "name": "PET_MODE",
                                    "status": "AVAILABLE",
                                },
                                {
                                    "__typename": "SupportedFeature",
                                    "name": "PRECON_CMD_RESP",
                                    "status": "AVAILABLE",
                                },
                                {
                                    "__typename": "SupportedFeature",
                                    "name": "PRECON_SCRN_PROT",
                                    "status": "AVAILABLE",
                                },
                                {
                                    "__typename": "SupportedFeature",
                                    "name": "SET_TEMP_CMD",
                                    "status": "AVAILABLE",
                                },
                                {
                                    "__typename": "SupportedFeature",
                                    "name": "TAILGATE_CMD",
                                    "status": "AVAILABLE",
                                },
                                {
                                    "__typename": "SupportedFeature",
                                    "name": "TAILGATE_NXT_ACT",
                                    "status": "AVAILABLE",
                                },
                                {
                                    "__typename": "SupportedFeature",
                                    "name": "VENTED_SEATS",
                                    "status": "AVAILABLE",
                                },
                                {
                                    "__typename": "SupportedFeature",
                                    "name": "WIN_CALIB_STS",
                                    "status": "AVAILABLE",
                                },
                                {
                                    "__typename": "SupportedFeature",
                                    "name": "TRIP_PLANNER",
                                    "status": "AVAILABLE",
                                },
                            ],
                        },
                    },
                    "settings": {
                        "__typename": "UserVehicleSettingsMap",
                        "name": {
                            "__typename": "NameSetting",
                            "value": "R1T",
                        },
                    },
                }
            ],
            "enrolledPhones": [
                {
                    "__typename": "UserEnrolledPhone",
                    "vas": {
                        "__typename": "UserEnrolledPhoneAccess",
                        "vasPhoneId": "vasPhoneId",
                        "publicKey": "publicKey",
                    },
                    "enrolled": [
                        {
                            "__typename": "UserEnrolledPhoneEntry",
                            "deviceType": "phone/rivian",
                            "deviceName": "deviceName",
                            "vehicleId": "vehicleId",
                            "identityId": "identityId",
                        }
                    ],
                }
            ],
            "pendingInvites": [],
            "address": {"__typename": "UserAddress", "country": "US"},
        }
    }
}
VEHICLE_STATE_RESPONSE = {
    "data": {
        "vehicleState": {
            "__typename": "VehicleState",
            "gnssLocation": {
                "__typename": "VehicleLocation",
                "latitude": 42.3601866,
                "longitude": -71.0589682,
                "timeStamp": "2022-10-26T20:07:01.081Z",
            },
            "alarmSoundStatus": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-07T04:42:39.880Z",
                "value": "false",
            },
            "timeToEndOfCharge": {
                "__typename": "TimeStampedFloat",
                "timeStamp": "2022-10-26T20:04:38.716Z",
                "value": 0,
            },
            "doorFrontLeftLocked": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:45:39.179Z",
                "value": "locked",
            },
            "doorFrontLeftClosed": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:45:39.179Z",
                "value": "closed",
            },
            "doorFrontRightLocked": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:45:39.179Z",
                "value": "locked",
            },
            "doorFrontRightClosed": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:45:39.179Z",
                "value": "closed",
            },
            "doorRearLeftLocked": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:45:39.179Z",
                "value": "locked",
            },
            "doorRearLeftClosed": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:45:39.179Z",
                "value": "closed",
            },
            "doorRearRightLocked": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:45:39.179Z",
                "value": "locked",
            },
            "doorRearRightClosed": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:45:39.179Z",
                "value": "closed",
            },
            "windowFrontLeftClosed": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:45:39.179Z",
                "value": "closed",
            },
            "windowFrontRightClosed": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:45:39.179Z",
                "value": "closed",
            },
            "windowFrontLeftCalibrated": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:45:39.179Z",
                "value": "Calibrated",
            },
            "windowFrontRightCalibrated": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:45:39.179Z",
                "value": "Calibrated",
            },
            "windowRearLeftCalibrated": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:45:39.179Z",
                "value": "Calibrated",
            },
            "windowRearRightCalibrated": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:45:39.179Z",
                "value": "Calibrated",
            },
            "closureFrunkLocked": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:45:39.179Z",
                "value": "locked",
            },
            "closureFrunkClosed": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:45:39.179Z",
                "value": "closed",
            },
            "gearGuardLocked": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:45:39.179Z",
                "value": "unlocked",
            },
            "closureLiftgateLocked": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:45:39.179Z",
                "value": "locked",
            },
            "closureLiftgateClosed": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:45:39.179Z",
                "value": "signal_not_available",
            },
            "windowRearLeftClosed": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:45:39.179Z",
                "value": "closed",
            },
            "windowRearRightClosed": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:45:39.179Z",
                "value": "closed",
            },
            "closureSideBinLeftLocked": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:45:39.179Z",
                "value": "locked",
            },
            "closureSideBinLeftClosed": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:45:39.179Z",
                "value": "closed",
            },
            "closureSideBinRightLocked": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:45:39.179Z",
                "value": "locked",
            },
            "closureSideBinRightClosed": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:45:39.179Z",
                "value": "closed",
            },
            "closureTailgateLocked": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:45:39.179Z",
                "value": "locked",
            },
            "closureTailgateClosed": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:45:39.179Z",
                "value": "closed",
            },
            "closureTonneauLocked": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:45:39.179Z",
                "value": "locked",
            },
            "closureTonneauClosed": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:45:39.179Z",
                "value": "closed",
            },
            "wiperFluidState": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-14T01:01:22.260Z",
                "value": "normal",
            },
            "powerState": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:46:39.763Z",
                "value": "ready",
            },
            "batteryHvThermalEventPropagation": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T16:58:03.936Z",
                "value": "off",
            },
            "vehicleMileage": {
                "__typename": "TimeStampedInt",
                "timeStamp": "2022-10-26T19:43:13.847Z",
                "value": 8928840,
            },
            "brakeFluidLow": None,
            "gearStatus": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:43:18.344Z",
                "value": "park",
            },
            "tirePressureStatusFrontLeft": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:39:27.589Z",
                "value": "OK",
            },
            "tirePressureStatusValidFrontLeft": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:39:27.589Z",
                "value": "valid",
            },
            "tirePressureStatusFrontRight": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:39:27.589Z",
                "value": "OK",
            },
            "tirePressureStatusValidFrontRight": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:39:27.589Z",
                "value": "valid",
            },
            "tirePressureStatusRearLeft": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:39:27.589Z",
                "value": "OK",
            },
            "tirePressureStatusValidRearLeft": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:39:27.589Z",
                "value": "valid",
            },
            "tirePressureStatusRearRight": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:39:27.589Z",
                "value": "OK",
            },
            "tirePressureStatusValidRearRight": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:39:27.589Z",
                "value": "valid",
            },
            "batteryLevel": {
                "__typename": "TimeStampedFloat",
                "timeStamp": "2022-10-26T19:46:30.360Z",
                "value": 53.400002,
            },
            "chargerState": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T18:00:45.533Z",
                "value": "charging_ready",
            },
            "batteryHvThermalEvent": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:40:08.035Z",
                "value": "nominal",
            },
            "rangeThreshold": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:40:08.035Z",
                "value": "vehicle_range_normal",
            },
            "distanceToEmpty": {
                "__typename": "TimeStampedInt",
                "timeStamp": "2022-10-26T19:38:56.266Z",
                "value": 266,
            },
            "otaAvailableVersionNumber": {
                "__typename": "TimeStampedInt",
                "timeStamp": "2022-10-07T09:07:17.231Z",
                "value": 0,
            },
            "otaAvailableVersionWeek": {
                "__typename": "TimeStampedInt",
                "timeStamp": "2022-10-07T09:07:17.231Z",
                "value": 0,
            },
            "otaAvailableVersionYear": {
                "__typename": "TimeStampedInt",
                "timeStamp": "2022-10-07T09:07:17.231Z",
                "value": 0,
            },
            "otaCurrentVersionNumber": {
                "__typename": "TimeStampedInt",
                "timeStamp": "2022-10-07T09:07:17.231Z",
                "value": 3,
            },
            "otaCurrentVersionWeek": {
                "__typename": "TimeStampedInt",
                "timeStamp": "2022-10-07T09:07:17.231Z",
                "value": 35,
            },
            "otaCurrentVersionYear": {
                "__typename": "TimeStampedInt",
                "timeStamp": "2022-10-07T09:07:17.231Z",
                "value": 2022,
            },
            "otaDownloadProgress": {
                "__typename": "TimeStampedInt",
                "timeStamp": "2022-10-07T09:07:17.231Z",
                "value": 0,
            },
            "otaInstallDuration": {
                "__typename": "TimeStampedInt",
                "timeStamp": "2022-10-07T09:07:17.231Z",
                "value": 0,
            },
            "otaInstallProgress": {
                "__typename": "TimeStampedInt",
                "timeStamp": "2022-10-07T09:07:17.231Z",
                "value": 0,
            },
            "otaInstallReady": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:43:18.428Z",
                "value": "ota_available",
            },
            "otaInstallTime": {
                "__typename": "TimeStampedInt",
                "timeStamp": "2022-10-07T09:07:17.231Z",
                "value": 0,
            },
            "otaInstallType": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-07T09:07:17.231Z",
                "value": "Convenience",
            },
            "otaStatus": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-07T09:07:17.231Z",
                "value": "Idle",
            },
            "otaCurrentStatus": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-07T09:07:17.231Z",
                "value": "Install_Success",
            },
            "cabinClimateInteriorTemperature": {
                "__typename": "TimeStampedFloat",
                "timeStamp": "2022-10-26T20:07:04.559Z",
                "value": 21,
            },
            "cabinClimateDriverTemperature": {
                "__typename": "TimeStampedFloat",
                "timeStamp": "2022-10-26T20:07:04.559Z",
                "value": 20,
            },
            "cabinPreconditioningStatus": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:45:39.808Z",
                "value": "undefined",
            },
            "cabinPreconditioningType": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:45:39.808Z",
                "value": "NONE",
            },
            "petModeStatus": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:43:18.485Z",
                "value": "Off",
            },
            "petModeTemperatureStatus": {
                "__typename": "TimeStampedString",
                "timeStamp": "2022-10-26T19:43:18.485Z",
                "value": "Default",
            },
        }
    }
}
WALLBOXES_RESPONSE = {
    "data": {
        "getRegisteredWallboxes": [
            {
                "__typename": "WallboxRecord",
                "wallboxId": "W1-1113-3RV7-1-1234-00012",
                "userId": "01-2a3259ba-0be3-42a7-bf82-69adea27dcdd-2b4532cd",
                "wifiId": "Network",
                "name": "Wall Charger",
                "linked": True,
                "latitude": "42.3601866",
                "longitude": "-71.0589682",
                "chargingStatus": "AVAILABLE",
                "power": None,
                "currentVoltage": None,
                "currentAmps": None,
                "softwareVersion": "V03.01.47",
                "model": "W1-1113-3RV7",
                "serialNumber": "W1-1113-3RV7-1-1234-00012",
                "maxAmps": None,
                "maxVoltage": "224.0",
                "maxPower": "11000",
            }
        ]
    }
}

DISENROLL_PHONE_BAD_REQUEST_RESPONSE = {
    "errors": [
        {
            "extensions": {
                "code": "BAD_REQUEST_ERROR",
                "reason": "DISENROLL_PHONE_BAD_REQUEST",
            },
            "message": "Bad request error",
            "path": ["disenrollPhone"],
        }
    ],
    "data": None,
}


def error_response(
    code: str | None = None, reason: str | None = None
) -> dict[str, Any]:
    """Return an error response."""
    error = {"extensions": {"code": code, "reason": reason or code}} if code else {}
    return {"errors": [error]}


def load_response(response_name: str) -> dict[str, Any]:
    """Load a response."""
    with open(f"{os.path.dirname(__file__)}/fixtures/{response_name}.json") as file:
        return json.load(file)
