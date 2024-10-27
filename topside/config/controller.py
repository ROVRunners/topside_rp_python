from typing import NamedTuple
from topside.config import RangeConfig

class AxisConfig(NamedTuple):
    """
    :deadband: the deadband for the axis.
    Range we want to allow from controller input, absolute value is used and then negated if input was negative
    :index: the index of the axis
    :output_range: the scaler of the input. Output range of the axis, should be in units meaningful to the robot

    """
    # Range we want to allow from controller input, absolute value is used and then negated if input was negative,
    # It is expressed as a value from 0 to 1, and is scaled to the expected input range during computation
    deadband: float = 0
    # Output range of the axis, should be in units meaningful to the robot
    output_range: RangeConfig = RangeConfig(0,1)
    # Input range we expect to recieve from the input device.
    input_range: RangeConfig = RangeConfig(0, 1)


class ButtonConfig(NamedTuple):
    index: int
    negated: bool
    toggled: bool


class BindingConfig(NamedTuple):
    A: ButtonConfig
    B: ButtonConfig
    X: ButtonConfig
    Y: ButtonConfig
    LEFT_BUMPER: ButtonConfig
    RIGHT_BUMPER: ButtonConfig
    SELECT: ButtonConfig
    START: ButtonConfig


class AxesConfig(NamedTuple):
    LEFT_X: AxisConfig
    LEFT_Y: AxisConfig
    RIGHT_X: AxisConfig
    RIGHT_Y: AxisConfig
    LEFT_TRIGGER: AxisConfig
    RIGHT_TRIGGER: AxisConfig


class ControllerConfig(NamedTuple):
    buttons: BindingConfig
    axes: AxisConfig
