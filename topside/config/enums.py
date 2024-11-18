"""Declaration of enums used in the configuration of the ROV."""

import enum


# Define the Buttons and Axes
class ControllerAxisNames(enum.StrEnum):
    """The axes available on the controller.

    Implements:
        enum.StrEnum

    Properties:
        LEFT_X (str):
            The left x-axis of the controller.
        LEFT_Y (str):
            The left y-axis of the controller.
        RIGHT_X (str):
            The right x-axis of the controller.
        RIGHT_Y (str):
            The right y-axis of the controller.
        LEFT_TRIGGER (str):
            The left trigger of the controller.
        RIGHT_TRIGGER (str):
            The right trigger of the controller.
    """
    LEFT_X = "LEFT_X",
    LEFT_Y = "LEFT_Y",
    RIGHT_X = "RIGHT_X",
    RIGHT_Y = "RIGHT_Y",
    LEFT_TRIGGER = "LEFT_TRIGGER",
    RIGHT_TRIGGER = "RIGHT_TRIGGER"


class ControllerButtonNames(enum.StrEnum):
    """The buttons available on the controller.

    Implements:
        enum.StrEnum

    Properties:
        A (str):
            The A button on the controller.
        B (str):
            The B button on the controller.
        X (str):
            The X button on the controller.
        Y (str):
            The Y button on the controller.
        START (str):
            The start button on the controller.
        SELECT (str):
            The select button on the controller.
        LEFT_BUMPER (str):
            The left bumper on the controller.
        RIGHT_BUMPER (str):
            The right bumper on the controller.
    """
    A = "A",
    B = "B",
    X = "X",
    Y = "Y",
    START = "START",
    SELECT = "SELECT",
    LEFT_BUMPER = "LEFT_BUMPER",
    RIGHT_BUMPER = "RIGHT_BUMPER",


# Define the Thrusters and Orientations
class ThrusterPositions(enum.StrEnum):
    """The thrusters and associated names available to this ROV.

    Implements:
        enum.StrEnum

    Properties:
        FRONT_RIGHT (str):
            The front right thruster.
        FRONT_LEFT (str):
            The front left thruster.
        REAR_RIGHT (str):
            The rear right thruster.
        REAR_LEFT (str):
            The rear left thruster.
        FRONT_RIGHT_VERTICAL (str):
            The front right vertical thruster.
        FRONT_LEFT_VERTICAL (str):
            The front left vertical thruster.
        REAR_RIGHT_VERTICAL (str):
            The rear right vertical thruster.
        REAR_LEFT_VERTICAL (str):
            The rear left vertical thruster.
    """
    FRONT_RIGHT = "FRONT_RIGHT",
    FRONT_LEFT = "FRONT_LEFT",
    REAR_RIGHT = "REAR_RIGHT",
    REAR_LEFT = "REAR_LEFT",
    FRONT_RIGHT_VERTICAL = "FRONT_RIGHT_VERTICAL",
    FRONT_LEFT_VERTICAL = "FRONT_LEFT_VERTICAL",
    REAR_RIGHT_VERTICAL = "REAR_RIGHT_VERTICAL",
    REAR_LEFT_VERTICAL = "REAR_LEFT_VERTICAL",


class Directions(enum.StrEnum):
    """The directions that thrusters can apply force in.

    Implements:
        enum.StrEnum

    Properties:
        FORWARDS (str):
            The force a thruster generates in the forwards direction.
        RIGHT (str):
            The force a thruster generates in the right direction.
        UP (str):
            The force a thruster generates in the up direction.
        YAW (str):
            The force a thruster generates in the clockwise yaw axis.
        PITCH (str):
            The force a thruster generates in the pitch axis (front tipping up).
        ROLL (str):
            The force a thruster generates in the roll axis (left side tipping up).
    """
    FORWARDS = "FORWARDS",
    RIGHT = "RIGHT",
    UP = "UP",
    YAW = "YAW",
    PITCH = "PITCH",
    ROLL = "ROLL",
