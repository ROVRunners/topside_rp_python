"""Declaration of enums used in the configuration of the ROV."""

import enum


# Define the Buttons and Axes
class ControllerAxisNames(enum.IntEnum):
    """The axes available on the controller."""
    LEFT_X = enum.auto(),
    LEFT_Y = enum.auto(),
    RIGHT_X = enum.auto(),
    RIGHT_Y = enum.auto(),
    LEFT_TRIGGER = enum.auto(),
    RIGHT_TRIGGER = enum.auto()


class ControllerButtonNames(enum.IntEnum):
    """The buttons available on the controller."""
    A = enum.auto(),
    B = enum.auto(),
    X = enum.auto(),
    Y = enum.auto(),
    START = enum.auto(),
    SELECT = enum.auto(),
    LEFT_BUMPER = enum.auto(),
    RIGHT_BUMPER = enum.auto(),


# Define the Thrusters and Orientations
class ThrusterPositions(enum.StrEnum):
    """The thrusters and associated names available to this ROV."""
    FRONT_RIGHT = "FRONT_RIGHT",
    FRONT_LEFT = "FRONT_LEFT",
    REAR_RIGHT = "REAR_RIGHT",
    REAR_LEFT = "REAR_LEFT",
    FRONT_RIGHT_VERTICAL = "FRONT_RIGHT_VERTICAL",
    FRONT_LEFT_VERTICAL = "FRONT_LEFT_VERTICAL",
    REAR_RIGHT_VERTICAL = "REAR_RIGHT_VERTICAL",
    REAR_LEFT_VERTICAL = "REAR_LEFT_VERTICAL",

    def __repr__(self):
        return self.value


class ThrusterOrientations(enum.StrEnum):
    """The directions that thrusters can apply force in."""
    FORWARDS = "FORWARDS",
    RIGHT = "RIGHT",
    UP = "UP",
    YAW = "YAW",
    PITCH = "PITCH",
    ROLL = "ROLL",
