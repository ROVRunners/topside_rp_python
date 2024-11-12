from . import manual
import enum
from topside.config import AxisConfig, ButtonConfig, ThrusterPWMConfig, IntRange, ControllerConfig

class ControllerAxisNames(enum.IntEnum):
    LEFT_X = enum.auto(),
    LEFT_Y = enum.auto(),
    RIGHT_X = enum.auto(),
    RIGHT_Y = enum.auto(),
    TRIGGERS = enum.auto(),

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
    FRONT_LEFT = "FRONT_LEFT",
    FRONT_RIGHT = "FRONT_RIGHT",
    BACK_LEFT = "BACK_LEFT",
    BACK_RIGHT = "BACK_RIGHT",

class SpikeConfig:
    """Class for the ROV configuration."""

    controller_axis_mapping: dict[ControllerAxisNames, int] = {
        ControllerAxisNames.LEFT_X.value: 0,
        ControllerAxisNames.LEFT_Y.value: 1,
        ControllerAxisNames.RIGHT_X.value: 2,
        ControllerAxisNames.RIGHT_Y.value: 3,
        ControllerAxisNames.TRIGGERS.value: 4 #AxisConfig()
        # AxisNames.RIGHT_TRIGGER.value: AxisConfig()
    }

    "Put specific settings for each axis here"
    axis_configs: dict[ControllerAxisNames, AxisConfig] = {
        ControllerAxisNames.LEFT_X.value: AxisConfig(),
        ControllerAxisNames.LEFT_Y.value: AxisConfig(),
        ControllerAxisNames.RIGHT_X.value: AxisConfig(),
        ControllerAxisNames.RIGHT_Y.value: AxisConfig(),
        ControllerAxisNames.TRIGGERS.value: AxisConfig(),
        # ControllerAxisNames.RIGHT_TRIGGER.value: AxisConfig()
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
    standard_thruster_config = lambda: ThrusterPWMConfig(pwm_pulse_range=IntRange(min=7000, max=11000), reverse_polarity=False)
    
    thruster_configs: dict[str, ThrusterPWMConfig] = {
        ThrusterPosition.FRONT_LEFT:  standard_thruster_config(),
        ThrusterPosition.FRONT_RIGHT: standard_thruster_config(),
        ThrusterPosition.BACK_LEFT:   standard_thruster_config(),
        ThrusterPosition.BACK_RIGHT:  standard_thruster_config(),
    }

    def __init__(self) -> None:
        """Initialize an instance of the class."""

        # All the following values except the manual class and intercepts
        # can be either filled or set to None, but they MUST be defined.

        # Classes to initialize.
        self.manual_class = manual.Manual  # REQUIRED

        # Main functions.
        self.manual_intercepts = self.manual_class.manual_intercepts  # REQUIRED

