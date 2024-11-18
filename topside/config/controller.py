"""Configuration classes for controller inputs.

Classes:
    AxisConfig:
        Describes the configuration of an axis on a controller.
    ButtonConfig:
        Describes the configuration of a button on a controller.
    ControllerConfig:
        Mapping of axes and button numbers to specific configurations.
    InputFunction:
        Describes a function and the arguments to be called with it.
"""

from typing import NamedTuple, Callable

# from topside.config.typed_range import RangeConfig
import config.typed_range as typed_range
import rovs.spike.enums as enums


class AxisConfig(NamedTuple):
    """Describes the configuration of an axis on a controller.

    Implements:
        NamedTuple

    Attributes:
        index (int):
            The index of the axis on the controller.
        deadband (float):
            The deadband for the axis.
        inverted (bool):
            Whether the axis is inverted.
        input_range (RangeConfig):
            Input range we expect to receive from the input device.
        output_range (RangeConfig):
            The scaler of the input. Output range of the axis, should be in units meaningful to the robot.
    """
    index: int
    deadband: float = 0
    inverted: bool = False

    # Range we want to allow from controller input, absolute value is used and then negated if input was negative,
    # It is expressed as a value from 0 to 1, and is scaled to the expected input range during computation.

    # Input range we expect to receive from the input device.
    input_range: typed_range.RangeConfig = typed_range.RangeConfig(-1, 1)
    # Output range of the axis, should be in units meaningful to the robot
    output_range: typed_range.RangeConfig = typed_range.RangeConfig(0, 1)


class InputFunction(NamedTuple):
    """Describes a function and the arguments to be called with it.

    Implements:
        NamedTuple

    Attributes:
        func (Callable[[...], object]):
            The function to be called.
        args (list):
            The arguments to be passed to the function.
        kwargs (dict):
            The keyword arguments to be passed to the function.
    """
    func: Callable[[...], object]
    args: list
    kwargs: dict


class ButtonConfig(NamedTuple):
    """Describes the configuration of a button on a controller.

    Implements:
        NamedTuple

    Attributes:
        index (int):
            The index of the button on the controller.
        negated (bool):
            Whether the button is negated.
        toggled (bool):
            Whether the button is toggled.
    """
    index: int
    negated: bool = False
    toggled: bool = False


class ControllerConfig(NamedTuple):
    """Mapping of axes and button numbers to specific configurations.

    Implements:
        NamedTuple

    Attributes:
        buttons (dict[enums.ControllerButtonNames, ButtonConfig]):
            Mapping of button numbers to ButtonConfig objects.
        axes (dict[enums.ControllerAxisNames, AxisConfig]):
            Mapping of axis numbers to AxisConfig objects.
    """
    buttons: dict[enums.ControllerButtonNames, ButtonConfig]
    axes: dict[enums.ControllerAxisNames, AxisConfig]
