
import enum
from topside.config import AxisConfig, ButtonConfig, ThrusterPWMConfig, IntRange, ControllerConfig


# Define the Axes
class ControllerAxisNames(enum.IntEnum):
    LEFT_X = enum.auto(),
    LEFT_Y = enum.auto(),
    RIGHT_X = enum.auto(),
    RIGHT_Y = enum.auto(),
    LEFT_TRIGGER = enum.auto(),
    RIGHT_TRIGGER = enum.auto()


class ControllerButtonNames(enum.IntEnum):
    A = enum.auto(),
    B = enum.auto(),
    X = enum.auto(),
    Y = enum.auto(),
    START = enum.auto(),
    SELECT = enum.auto(),
    LEFT_BUMPER = enum.auto(),
    RIGHT_BUMPER = enum.auto(),


class ThrusterPosition(enum.StrEnum):
    """The thrusters and associated names available to this ROV"""
    FRONT_RIGHT = "FRONT_RIGHT",
    FRONT_LEFT = "FRONT_LEFT",
    REAR_RIGHT = "REAR_RIGHT",
    REAR_LEFT = "REAR_LEFT",
    FRONT_RIGHT_VERTICAL = "FRONT_RIGHT_VERTICAL",
    FRONT_LEFT_VERTICAL = "FRONT_LEFT_VERTICAL",
    REAR_RIGHT_VERTICAL = "REAR_RIGHT_VERTICAL",
    REAR_LEFT_VERTICAL = "REAR_LEFT_VERTICAL",


class SpikeConfig:
    """Class for the ROV  configuration."""

    controller_axis_mapping: dict[ControllerAxisNames, int] = {
        ControllerAxisNames.LEFT_X: 0,
        ControllerAxisNames.LEFT_Y: 1,
        ControllerAxisNames.RIGHT_X: 2,
        ControllerAxisNames.RIGHT_Y: 3,
        ControllerAxisNames.LEFT_TRIGGER: 4,
        ControllerAxisNames.RIGHT_TRIGGER: 5,
        # AxisNames.RIGHT_TRIGGER.value: AxisConfig()
    }

    # Put specific settings for each axis here
    axis_configs: dict[ControllerAxisNames, AxisConfig] = {
        controller_axis_mapping[ControllerAxisNames.LEFT_X]: AxisConfig(deadband=0.15),
        controller_axis_mapping[ControllerAxisNames.LEFT_Y]: AxisConfig(deadband=0.15),
        controller_axis_mapping[ControllerAxisNames.RIGHT_X]: AxisConfig(deadband=0.15),
        controller_axis_mapping[ControllerAxisNames.RIGHT_Y]: AxisConfig(deadband=0.15),
        controller_axis_mapping[ControllerAxisNames.LEFT_TRIGGER]: AxisConfig(),
        controller_axis_mapping[ControllerAxisNames.RIGHT_TRIGGER]: AxisConfig()
    }
    button_configs: dict[ControllerButtonNames, ButtonConfig] = {
        ControllerButtonNames.A.value: ButtonConfig(index=0),
        ControllerButtonNames.B.value: ButtonConfig(index=1),
        ControllerButtonNames.X.value: ButtonConfig(index=2),
        ControllerButtonNames.Y.value: ButtonConfig(index=3),
        ControllerButtonNames.START.value: ButtonConfig(index=6),
        ControllerButtonNames.SELECT.value: ButtonConfig(index=7),
        ControllerButtonNames.LEFT_BUMPER.value: ButtonConfig(index=4),
        ControllerButtonNames.RIGHT_BUMPER.value: ButtonConfig(index=5),
    }

    controller_config = ControllerConfig(button_configs, axis_configs)

    #Call a lambda to ensure each config object is different and changing one PWM value doesn't affect other motors
    # standard_thruster_config = lambda: ThrusterPWMConfig(pwm_pulse_range=IntRange(min=1100, max=1900), reverse_polarity=False)

    # may need to change these values
    thruster_impulses: dict[str, dict[str, float]] = {
        ThrusterPosition.FRONT_RIGHT: {
            "forwards": .7,
            "right": -.7,
            "up": 0,
            "pitch": 0,
            "roll": 0,
            "yaw": 1,
        },
        ThrusterPosition.FRONT_LEFT: {
            "forwards": .7,
            "right": .7,
            "up": 0,
            "pitch": 0,
            "roll": 0,
            "yaw": -1,
        },
        ThrusterPosition.REAR_RIGHT: {
            "forwards": -.7,
            "right": -.7,
            "up": 0,
            "pitch": 0,
            "roll": 0,
            "yaw": 1,
        },
        ThrusterPosition.REAR_LEFT: {
            "forwards": -.7,
            "right": .7,
            "up": 0,
            "pitch": 0,
            "roll": 0,
            "yaw": -1,
        },
        ThrusterPosition.FRONT_RIGHT_VERTICAL: {
            "forwards": 0,
            "right": -0,
            "up": 0,
            "pitch": 0,
            "roll": 0,
            "yaw": 1,
        },
        ThrusterPosition.FRONT_LEFT_VERTICAL: {
            "forwards": 0,
            "right": 0,
            "up": 0,
            "pitch": 0,
            "roll": 0,
            "yaw": -1,
        },
        ThrusterPosition.REAR_RIGHT_VERTICAL: {
            "forwards": -0,
            "right": -0,
            "up": 0,
            "pitch": 0,
            "roll": 0,
            "yaw": 1,
        },
        ThrusterPosition.REAR_LEFT_VERTICAL: {
            "forwards": -0,
            "right": 0,
            "up": 0,
            "pitch": 0,
            "roll": 0,
            "yaw": -1,
        },
    }

    thruster_configs: dict[str, ThrusterPWMConfig] = {
        ThrusterPosition.FRONT_RIGHT: ThrusterPWMConfig(
            pwm_pulse_range=IntRange(min=1100, max=1900),
            thruster_impulses=thruster_impulses[ThrusterPosition.FRONT_RIGHT]
        ),
        ThrusterPosition.FRONT_LEFT:  ThrusterPWMConfig(
            pwm_pulse_range=IntRange(min=1100, max=1900),
            thruster_impulses=thruster_impulses[ThrusterPosition.FRONT_LEFT]
        ),
        ThrusterPosition.REAR_RIGHT:  ThrusterPWMConfig(
            pwm_pulse_range=IntRange(min=1100, max=1900),
            thruster_impulses=thruster_impulses[ThrusterPosition.REAR_RIGHT]
        ),
        ThrusterPosition.REAR_LEFT:   ThrusterPWMConfig(
            pwm_pulse_range=IntRange(min=1100, max=1900),
            thruster_impulses=thruster_impulses[ThrusterPosition.REAR_LEFT]
        ),
        ThrusterPosition.FRONT_RIGHT_VERTICAL: ThrusterPWMConfig(
            pwm_pulse_range=IntRange(min=1100, max=1900),
            thruster_impulses=thruster_impulses[ThrusterPosition.FRONT_RIGHT_VERTICAL]
        ),
        ThrusterPosition.FRONT_LEFT_VERTICAL:  ThrusterPWMConfig(
            pwm_pulse_range=IntRange(min=1100, max=1900),
            thruster_impulses=thruster_impulses[ThrusterPosition.FRONT_LEFT_VERTICAL]
        ),
        ThrusterPosition.REAR_RIGHT_VERTICAL:  ThrusterPWMConfig(
            pwm_pulse_range=IntRange(min=1100, max=1900),
            thruster_impulses=thruster_impulses[ThrusterPosition.REAR_RIGHT_VERTICAL]
        ),
        ThrusterPosition.REAR_LEFT_VERTICAL:   ThrusterPWMConfig(
            pwm_pulse_range=IntRange(min=1100, max=1900),
            thruster_impulses=thruster_impulses[ThrusterPosition.REAR_LEFT_VERTICAL]
        ),
    }

    def __init__(self) -> None:
        """Initialize an instance of the class."""

        # All the following values except the manual class and intercepts
        # can be either filled or set to None, but they MUST be defined.

        # # Classes to initialize.
        # self.manual_class = manual.Manual  # REQUIRED
        #
        # # Main functions.
        # self.manual_intercepts = self.manual_class.manual_intercepts  # REQUIRED

