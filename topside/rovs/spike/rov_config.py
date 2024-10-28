import manual
import enum
from topside.config import AxisConfig, ThrusterPWMConfig, IntRange

class ControllerAxisNames(enum.IntEnum):
    LEFT_X = enum.auto(),
    LEFT_Y = enum.auto(),
    RIGHT_X = enum.auto(),
    RIGHT_Y = enum.auto(),
    TRIGGERS = enum.auto()

class ThrusterPosition(enum.StrEnum):
    """The thrusters and associated names available to this ROV"""
    FRONT_LEFT = "FRONT_LEFT",
    FRONT_RIGHT = "FRONT_RIGHT",
    BACK_LEFT = "BACK_LEFT",
    BACK_RIGHT = "BACK_RIGHT",

class SpikeConfig:
    """Class for the ROV configuration."""

    controller_axis_mapping: dict[ControllerAxisNames, int] =
    {
        ControllerAxisNames.LEFT_X.value: 0,
        ControllerAxisNames.LEFT_Y.value: 1,
        ControllerAxisNames.RIGHT_X.value: 2,
        ControllerAxisNames.RIGHT_Y.value: 3,
        AxisNames.LEFT_TRIGGER.value: AxisConfig(),
        AxisNames.RIGHT_TRIGGER.value: AxisConfig(),
    }

    "Put specific settings for each axis here"
    axis_configs: dict[ControllerAxisNames, AxisConfig] = {
        ControllerAxisNames.LEFT_X.value: AxisConfig(),
        ControllerAxisNames.LEFT_Y.value: AxisConfig(),
        ControllerAxisNames.RIGHT_X.value: AxisConfig(),
        ControllerAxisNames.RIGHT_Y.value: AxisConfig(),
        ControllerAxisNames.LEFT_TRIGGER.value: AxisConfig(),
        ControllerAxisNames.RIGHT_TRIGGER.value: AxisConfig(),
    }

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

