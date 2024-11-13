from typing import NamedTuple, Callable
from topside.config.range import RangeConfig


class AxisConfig(NamedTuple):
    """Describes the configuration of an axis on a controller.

    Parameters:
        deadband (float):
            The deadband for the axis.
        input_range (RangeConfig):
            Input range we expect to receive from the input device.
        output_range (RangeConfig):
            The scaler of the input. Output range of the axis, should be in units meaningful to the robot.
    """
    # Range we want to allow from controller input, absolute value is used and then negated if input was negative,
    # It is expressed as a value from 0 to 1, and is scaled to the expected input range during computation
    deadband: float = 0
    # Input range we expect to receive from the input device.
    input_range: RangeConfig = RangeConfig(0, 1)
    # Output range of the axis, should be in units meaningful to the robot
    output_range: RangeConfig = RangeConfig(0, 1)


class InputFunction(NamedTuple):
    func: Callable[[...], object]
    args: list
    kwargs: dict


class ButtonConfig(NamedTuple):
    index: int
    negated: bool = False
    toggled: bool = False

#
# class BindingConfig(NamedTuple):
#     A: ButtonConfig
#     B: ButtonConfig
#     X: ButtonConfig
#     Y: ButtonConfig
#     LEFT_BUMPER: ButtonConfig
#     RIGHT_BUMPER: ButtonConfig
#     SELECT: ButtonConfig
#     START: ButtonConfig
#
#
# class AxesConfig(NamedTuple):
#     LEFT_X: AxisConfig
#     LEFT_Y: AxisConfig
#     RIGHT_X: AxisConfig
#     RIGHT_Y: AxisConfig
#     LEFT_TRIGGER: AxisConfig
#     RIGHT_TRIGGER: AxisConfig


class ControllerConfig(NamedTuple):
    """Mapping of axes and button numbers to specific configurations"""

    buttons: dict[int, ButtonConfig]
    axes: dict[int, AxisConfig]
