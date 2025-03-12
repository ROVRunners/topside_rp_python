from typing import NamedTuple
import enums


class FlightControllerConfig(NamedTuple):
    initial_commands: dict[enums.MavlinkMessageTypes, tuple[int, int, int, int, int, int, int]] = {}  # command and 7 parameters
    # attitude_messages: dict[enums.MavlinkMessageTypes, tuple[int, int]]
    # calibration_command: dict[enums.MavlinkMessageTypes, tuple[int, int]]
