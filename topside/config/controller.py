"""Configuration classes for controller inputs.

Classes:
    Axis:
        Handles an axis for the controller.
    Button:
        Describes the configuration of a button on a controller.
    Hat:
        Handles a hat for the controller.
    Controller:
        Mapping of axes and button numbers to specific configurations.
    InputHandler:
        Handles the input from the controllers.

Functions:
    combine_triggers(trigger_1: float, trigger_2: float) -> float:
        Combines the values of the two triggers into a single value.
"""
import pygame

import enums
import utilities.range_util as range_util


class Axis:
    """Handles an axis for the controller.

    Properties:
        index (int):
            The index of the axis on the controller.
        deadzone (float):
            The deadzone for the axis.
        inverted (bool):
            Whether the axis is inverted.
        input_range (range_util.Range):
            The expected range of the input.
        output_range (range_util.Range):
            The output range to map the input to.

    Methods:
        get_value(joystick: pygame.joystick.Joystick) -> float:
            Get the value of the axis from the controller.
    """
    index: int
    deadzone: float = 0.0
    inverted: bool = False

    # Range we want to allow from controller input, absolute value is used and then negated if input was negative,
    # It is expressed as a value from 0 to 1, and is scaled to the expected input range during computation.

    # Input range we expect to receive from the input device.
    input_range: range_util.Range = range_util.Range(-1, 1)
    # Output range of the axis, should be in units meaningful to the robot
    output_range: range_util.Range = range_util.Range(-1, 1)

    def __init__(self, index: int, deadzone: float = 0.0, inverted: bool = False,
                 input_range: range_util.Range = range_util.Range(-1, 1),
                 output_range: range_util.Range = range_util.Range(-1, 1)) -> None:
        """Initialize the AxisConfig object.

        Args:
            index (int):
                The index of the axis on the controller.
            deadzone (float):
                The deadzone for the axis.
            inverted (bool):
                Whether the axis is inverted.
            input_range (range.Range):
                The expected range of the input.
            output_range (range.Range):
                The output range to map the input to.
        """
        self.index = index
        self.deadzone = deadzone
        self.inverted = inverted

        self.input_range = input_range
        self.output_range = output_range

    def get_value(self, joystick: pygame.joystick.Joystick) -> float:
        """Get the value of the axis from the controller.

        Args:
            joystick (pygame.joystick.Joystick):
                The joystick to get the axis value from.

        Returns:
            float: The value of the axis.
        """
        # Get the raw value of the axis.
        value = joystick.get_axis(self.index)

        # Invert the value if necessary.
        if self.inverted:
            value = -value

        # Apply the deadzone to the value.
        deadzoned_value = self._apply_deadzone(value, deadzone=self.deadzone, input_range=self.input_range)

        # Scale the value to the output range.
        scaled_value = self.output_range.map(deadzoned_value, self.input_range)

        return scaled_value

    @classmethod
    def _apply_deadzone(cls, value: float, deadzone: float, input_range: range_util.Range) -> float:
        """Applies a deadzone to the input value.

        Args:
            value (float):
                The input value to apply the deadzone to.
            deadzone (float):
                The deadzone to apply to the value.
            input_range (range.Range):
                The range of the input value.

        Returns:
            float: The input value with the deadzone applied.
        """
        # Normalize the abs val of the input value. If the value is negative, that means it's below the deadzone cutoff.
        input_range = range_util.Range(deadzone, input_range.max_value)
        input_norm = input_range.normalize(abs(value))

        # Check if the input is above the deadzone cutoff.
        if input_norm > 0:
            # If the input is above the deadzone cutoff, return the value.
            return value

        # Otherwise, if the input is below the deadzone cutoff, return 0.
        return 0


class Button:
    """Describes the configuration of a button on a controller.

    Properties:
        index (int):
            The index of the button on the controller.
        negated (bool):
            Whether the button value is negated.
        toggled (bool):
            The initial toggled state of the button.

    Methods:
        get_value(joystick: pygame.joystick.Joystick) -> float:
            Get the value of the button from the controller.
        toggle() -> None:
            Alternate the toggled value of the button.
    """

    def __init__(self, index: int, negated: bool = False, toggled: bool = False) -> None:
        """Initialize the ButtonConfig object.

        Args:
            index (int):
                The index of the button on the controller.
            negated (bool):
                Whether the button value is negated.
            toggled (bool):
                The initial toggled state of the button.
        """
        self._index = index
        self._negated = negated
        self._toggled = toggled

        # The previous value of the button. Used to determine if the button was just toggled.
        self._prev_value = False

    @property
    def index(self) -> int:
        """The index of the button on the controller."""
        return self._index

    @property
    def negated(self) -> bool:
        """Whether the button value is negated."""
        return self._negated

    @negated.setter
    def negated(self, value: bool) -> None:
        """Set whether the button value is negated."""
        self._negated = value
        self._prev_value = not self._prev_value
        self._toggled = not self._toggled

    @property
    def toggled(self) -> bool:
        """Whether the button is toggled."""
        return self._toggled

    def get_value(self, joystick: pygame.joystick.Joystick) -> float:
        """Get the value of the button from the controller.

        Args:
            joystick (pygame.joystick.Joystick):
                The joystick to get the button value from.

        Returns:
            float: The value of the button.
        """
        # Get the raw value of the button.
        value = joystick.get_button(self._index)

        # Negate the value if necessary.
        if self._negated:
            value = not value

        # Toggle the value if necessary.
        if value and not self._prev_value:
            self._toggled = not self._toggled

        # Update the previous value.
        self._prev_value = value

        return value

    def toggle(self) -> None:
        """Alternate the toggled value of the button."""
        self._toggled = not self._toggled


class Hat:
    """Handles a hat for the controller.

    Properties:
        index (int):
            The index of the hat on the controller.
        invert_x (bool):
            Whether to invert the x value of the hat.
        invert_y (bool):
            Whether to invert the y value of the hat.

    Methods:
        toggle_button(button: enums.ControllerHatButtonNames) -> None:
            Toggle the value of a button on the hat.
        get_toggled_button(button: enums.ControllerHatButtonNames) -> bool:
            Get the toggled state of a button on the hat.
        get_values(joystick: pygame.joystick.Joystick) -> dict[enums.ControllerHatButtonNames, float]:
            Get the value of the hat from the controller.
        get_toggled_values() -> dict[enums.ControllerHatButtonNames, bool]:
            Get the toggled state of the hat buttons. update_toggles() must be called first to have accurate data.
        update_toggles(joystick: pygame.joystick.Joystick) -> None:
            Update the toggled state of the hat buttons.
    """

    def __init__(self, index: int, invert_x: bool = False, invert_y: bool = False) -> None:
        """Initialize the Hat object.

        Args:
            index (int):
                The index of the hat on the controller.
            invert_x (bool):
                Whether to invert the x value of the hat.
            invert_y (bool):
                Whether to invert the y value of the hat.
        """
        self._index: int = index
        self._invert_x: bool = invert_x
        self._invert_y: bool = invert_y

        self._prev_x: float = 0.0
        self._prev_y: float = 0.0

        self._DPAD_LEFT = enums.ControllerHatButtonNames.DPAD_LEFT
        self._DPAD_RIGHT = enums.ControllerHatButtonNames.DPAD_RIGHT
        self._DPAD_UP = enums.ControllerHatButtonNames.DPAD_UP
        self._DPAD_DOWN = enums.ControllerHatButtonNames.DPAD_DOWN

        self._toggled_buttons: dict[enums.ControllerHatButtonNames, bool] = {
            self._DPAD_LEFT: False,
            self._DPAD_RIGHT: False,
            self._DPAD_UP: False,
            self._DPAD_DOWN: False,
        }

    @property
    def index(self) -> int:
        """The index of the hat on the controller."""
        return self._index

    @property
    def invert_x(self) -> bool:
        """Whether to invert the x value of the hat."""
        return self._invert_x

    @invert_x.setter
    def invert_x(self, value: bool) -> None:
        """Set whether to invert the x value of the hat."""
        # If the value is unchanged, do nothing.
        if value == self._invert_x:
            return

        self._invert_x = value

        # Toggle the x values if one or the other is toggled (but not both).
        if self._toggled_buttons[self._DPAD_LEFT] != self._toggled_buttons[self._DPAD_RIGHT]:
            self._toggled_buttons[self._DPAD_LEFT] = not self._toggled_buttons[self._DPAD_LEFT]
            self._toggled_buttons[self._DPAD_RIGHT] = not self._toggled_buttons[self._DPAD_RIGHT]

    @property
    def invert_y(self) -> bool:
        """Whether to invert the y value of the hat."""
        return self._invert_y

    @invert_y.setter
    def invert_y(self, value: bool) -> None:
        """Set whether to invert the y value of the hat."""
        # If the value is unchanged, do nothing.
        if value == self._invert_y:
            return

        self._invert_y = value

        # Toggle the y values if one or the other is toggled (but not both).
        if self._toggled_buttons[self._DPAD_UP] != self._toggled_buttons[self._DPAD_DOWN]:
            self._toggled_buttons[self._DPAD_UP] = not self._toggled_buttons[self._DPAD_UP]
            self._toggled_buttons[self._DPAD_DOWN] = not self._toggled_buttons[self._DPAD_DOWN]

    def toggle_button(self, button: enums.ControllerHatButtonNames) -> None:
        """Toggle the value of a button on the hat.

        Args:
            button (enums.ControllerHatButtonNames):
                The button to toggle.
        """
        self._toggled_buttons[button] = not self._toggled_buttons[button]

    def get_toggled_button(self, button: enums.ControllerHatButtonNames) -> bool:
        """Get the toggled state of a button on the hat.

        Args:
            button (enums.ControllerHatButtonNames):
                The button to get the toggled state of.

        Returns:
            bool: The toggled state of the button.
        """
        return self._toggled_buttons[button]

    def get_values(self, joystick: pygame.joystick.Joystick) -> dict[enums.ControllerHatButtonNames, float]:
        """Get the value of the hat from the controller.

        Args:
            joystick (pygame.joystick.Joystick):
                The joystick to get the hat value from.

        Returns:
            tuple[int, int]: The value of the hat.
        """
        # Get the raw value of the hat.
        value = joystick.get_hat(self._index)

        # Invert the value if necessary.
        if self._invert_x:
            value = (value[0] * -1, value[1])
        if self._invert_y:
            value = (value[0], value[1] * -1)

        # Shorten the names of the button names.
        names = enums.ControllerHatButtonNames

        # Return the values of the hat buttons in float format.
        return {
            names.DPAD_LEFT: 1.0 if value[0] == -1 else 0.0,
            names.DPAD_RIGHT: 1.0 if value[0] == 1 else 0.0,
            names.DPAD_UP: 1.0 if value[1] == -1 else 0.0,
            names.DPAD_DOWN: 1.0 if value[1] == 1 else 0.0,
        }

    def get_toggled_values(self) -> dict[enums.ControllerHatButtonNames, bool]:
        """Get the toggled state of the hat buttons. update_toggles() must be called first to have accurate data.

        Returns:
            dict[enums.ControllerHatButtonNames, bool]: The toggled state of the hat buttons.
        """
        # Shorten the names of the button names.
        names = enums.ControllerHatButtonNames

        # Return the values of the hat buttons in float format.
        return {
            names.DPAD_LEFT: self._toggled_buttons[names.DPAD_LEFT],
            names.DPAD_RIGHT: self._toggled_buttons[names.DPAD_RIGHT],
            names.DPAD_UP: self._toggled_buttons[names.DPAD_UP],
            names.DPAD_DOWN: self._toggled_buttons[names.DPAD_DOWN],
        }

    def update_toggles(self, joystick: pygame.joystick.Joystick) -> None:
        """Update the toggled state of the hat buttons."""
        # Get the raw value of the hat.
        value = joystick.get_hat(self._index)

        # Invert the value if necessary.
        if self._invert_x:
            value = (value[0] * -1, value[1])
        if self._invert_y:
            value = (value[0], value[1] * -1)

        # Toggle the value if necessary.
        if value[0] == -1 and self._prev_x != -1:
            self.toggle_button(self._DPAD_LEFT)
        elif value[0] == 1 and self._prev_x != 1:
            self.toggle_button(self._DPAD_RIGHT)
        if value[1] == -1 and self._prev_y != -1:
            self.toggle_button(self._DPAD_UP)
        elif value[1] == 1 and self._prev_y != 1:
            self.toggle_button(self._DPAD_DOWN)


class Controller:
    """Mapping of axes and button numbers to specific configurations.

    Properties:
        buttons (dict[enums.ControllerButtonNames, Button]):
            Mapping of button numbers to Button objects.
        axes (dict[enums.ControllerAxisNames, Axis]):
            Mapping of axis numbers to Axis objects.
        hats (dict[enums.ControllerHatNames, Hat]):
            Mapping of hat numbers to Hat objects.
        index (int):
            The index of the controller to use.
        joystick (pygame.joystick.Joystick):
            The joystick object to use.

    Methods:
        get_inputs() -> dict[enums.ControllerButtonNames | enums.ControllerAxisNames |
                             enums.ControllerHatButtonNames, float]:
            Retrieves the inputs from the controller.
        get_toggled_inputs() -> dict[enums.ControllerHatButtonNames | enums.ControllerButtonNames, bool]:
            Get the toggled state of the buttons on the controller.
        get_button(button: enums.ControllerButtonNames) -> Button:
            Get the value of a button on the controller.
        get_axis(axis: enums.ControllerAxisNames) -> Axis:
            Get the value of an axis on the controller.
        get_hat(hat: enums.ControllerHatNames) -> Hat:
            Get the value of the hat on the controller.
        update_toggles() -> None:
            Update the toggled state of the hat buttons.
    """

    def __init__(self, index: int, buttons: dict[enums.ControllerButtonNames, Button],
                 axes: dict[enums.ControllerAxisNames, Axis], hats: dict[enums.ControllerHatNames, Hat]) -> None:
        """Initialize the ControllerConfig object.

        Args:
            index (int):
                The index of the controller to use.
            buttons (dict[enums.ControllerButtonNames, ButtonConfig]):
                Mapping of button numbers to ButtonConfig objects.
            axes (dict[enums.ControllerAxisNames, AxisConfig]):
                Mapping of axis numbers to AxisConfig objects.
            hats (dict[enums.ControllerHatNames, Hat]):
                Mapping of hat numbers to Hat objects.
        """
        self.buttons = buttons
        self.axes = axes
        self.hats = hats
        self._index = index

        pygame.init()
        pygame.joystick.init()

        # Wait for a controller to be connected.
        while pygame.joystick.get_count() < self._index:
            print("Warning! Not enough controllers detected!")
            input("Please connect a controller and press enter.")

        self._joystick = pygame.joystick.Joystick(self._index)
        self._joystick.init()

    @property
    def index(self) -> int:
        """The index of the controller to use."""
        return self._index

    @property
    def joystick(self) -> pygame.joystick.Joystick:
        """The joystick object to use."""
        return self._joystick

    def get_inputs(self) -> dict[enums.ControllerButtonNames | enums.ControllerAxisNames |
                                 enums.ControllerHatButtonNames, float]:
        """Retrieves the inputs from the controller.

        Returns:
            dict: The inputs from the controller as float amplitude values (buttons are 1.0/0.0).
        """
        # Merge all the inputs into a single dictionary.
        inputs: dict[enums.ControllerButtonNames | enums.ControllerAxisNames |
                     enums.ControllerHatButtonNames, float] = (
                self._get_button_values() | self._get_axis_values() | self._get_hat_values()
        )

        return inputs

    def get_toggled_inputs(self) -> dict[enums.ControllerHatButtonNames | enums.ControllerButtonNames, bool]:
        """Get the toggled state of the buttons on the controller.

        Returns:
            dict[enums.ControllerHatButtonNames | enums.ControllerButtonNames, bool]: The toggled state of the buttons.
        """
        values: dict[enums.ControllerHatButtonNames | enums.ControllerButtonNames, bool] = {}

        values.update(self._get_toggled_button_values())
        values.update(self._get_toggled_hat_values())

        return values

    def _get_button_values(self) -> dict[enums.ControllerButtonNames, float]:
        """Returns a dictionary containing the current state of the buttons on the controller.

        Returns:
            dict[str, float]: A dictionary mapping the button names to their states
                which are formatted as 0.0 (off) or 1.0 (on).
        """
        values: dict[enums.ControllerButtonNames, float] = {}

        for button in self.buttons:
            values[button] = self.buttons[button].get_value(self._joystick)

        return values

    def _get_toggled_button_values(self) -> dict[enums.ControllerButtonNames, bool]:
        """Returns a dictionary containing the toggled state of the buttons on the controller.

        Returns:
            dict[enums.ControllerButtonNames, bool]: A dictionary mapping the button names to their toggled states.
        """
        values: dict[enums.ControllerButtonNames, bool] = {}

        for button in self.buttons:
            values[button] = self.buttons[button].toggled

        return values

    def _get_axis_values(self) -> dict[enums.ControllerAxisNames, float]:
        """Returns a dictionary containing the values of various joystick axes.

        Returns:
            dict[enums.ControllerAxisNames, float]: The values of the joystick and trigger axes.
        """
        values: dict[enums.ControllerAxisNames, float] = {}

        for axis in self.axes:
            values[axis] = self.axes[axis].get_value(self._joystick)

        return values

    def _get_hat_values(self) -> dict[enums.ControllerHatButtonNames, float]:
        """Returns a dictionary containing the values of the hat buttons.

        Returns:
            dict[enums.ControllerHatButtonNames, float]: The values of the hat buttons in 1.0/0.0 format.
        """
        values: dict[enums.ControllerHatButtonNames, float] = {}

        for hat in self.hats:
            values.update(self.hats[hat].get_values(self._joystick))

        return values

    def _get_toggled_hat_values(self) -> dict[enums.ControllerHatButtonNames, bool]:
        """Returns a dictionary containing the toggled state of the hat buttons.

        Returns:
            dict[enums.ControllerHatButtonNames, bool]: The toggled state of the hat buttons.
        """
        values: dict[enums.ControllerHatButtonNames, bool] = {}

        for hat in self.hats:
            values.update(self.hats[hat].get_toggled_values())

        return values

    def get_button(self, button: enums.ControllerButtonNames) -> Button:
        """Get the value of a button on the controller.

        Args:
            button (enums.ControllerButtonNames):
                The button to get the value of.

        Returns:
            Button: The named button object.
        """
        return self.buttons[button]

    def get_axis(self, axis: enums.ControllerAxisNames) -> Axis:
        """Get the value of an axis on the controller.

        Args:
            axis (enums.ControllerAxisNames):
                The axis to get the value of.

        Returns:
            Axis: The named axis object.
        """
        return self.axes[axis]

    def get_hat(self, hat: enums.ControllerHatNames) -> Hat:
        """Get the value of the hat on the controller.

        Args:
            hat (enums.ControllerHatNames):
                The hat to get the value of.

        Returns:
            Hat: The named hat object.
        """
        return self.hats[hat]

    def update_toggles(self) -> None:
        """Update the toggled state of the hat buttons."""
        for hat in self.hats:
            self.hats[hat].update_toggles(self._joystick)
