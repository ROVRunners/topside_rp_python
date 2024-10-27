import manual
import enum
from topside.config import AxisConfig, ThrusterConfig, IntRange

class AxisNames(enum.StrEnum):
    LEFT_X = enum.auto(),
    LEFT_Y = enum.auto(),
    RIGHT_X = enum.auto(),
    RIGHT_Y = enum.auto(),
    LEFT_TRIGGER = enum.auto(),
    RIGHT_TRIGGER = enum.auto()

class ROVConfig:
    """Class for the ROV configuration."""

    "Put specific settings for each axis here"
    axis_configs: dict[str, AxisConfig] = {
        AxisNames.LEFT_X.value: AxisConfig(),
        AxisNames.LEFT_Y.value: AxisConfig(),
        AxisNames.RIGHT_X.value: AxisConfig(),
        AxisNames.RIGHT_Y.value: AxisConfig(),
        AxisNames.LEFT_TRIGGER.value: AxisConfig(),
        AxisNames.RIGHT_TRIGGER.value: AxisConfig(),
    }

    #Call a lambda to ensure each config object is different and changing one PWM value doesn't affect other motors
    standard_thruster_config = lambda: ThrusterConfig(pwm_pulse_range=IntRange(min=7000, max=11000), reverse_polarity=False)
    
    thruster_configs: dict[str, ThrusterConfig] = {
        "FRONT_LEFT":  standard_thruster_config(),
        "FRONT_RIGHT": standard_thruster_config(),
        "BACK_LEFT":   standard_thruster_config(),
        "BACK_RIGHT":  standard_thruster_config(),
    }

    def __init__(self) -> None:
        """Initialize an instance of the class."""

        # All the following values except the manual class and intercepts
        # can be either filled or set to None, but they MUST be defined.

        # Classes to initialize.
        self.manual_class = manual.Manual  # REQUIRED

        # Main functions.
        self.manual_intercepts = self.manual_class.manual_intercepts  # REQUIRED

