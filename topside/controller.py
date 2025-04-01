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

Functions:
    combine_triggers(trigger_1: float, trigger_2: float) -> float:
        Combines the values of the two triggers into a single value.
"""
import time

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
        update(joystick: type(pygame.joystick.Joystick)) -> None:
            Update the value of the axis from the controller.
    """

    _index: int
    _deadzone: float
    inverted: bool
    input_range: range_util.Range

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
        self._index: int = index
        self._deadzone: float = deadzone
        self._inverted: bool = inverted

        self._value: float = 0.0

        self._input_range = input_range
        self._output_range = output_range

    @property
    def value(self) -> float:
        return self._value

    @property
    def index(self) -> int:
        return self._index

    @property
    def deadzone(self) -> float:
        return self._deadzone

    @property
    def inverted(self) -> bool:
        return self._inverted

    @property
    def input_range(self) -> range_util.Range:
        return self._input_range

    @property
    def output_range(self) -> range_util.Range:
        return self._output_range

    @deadzone.setter
    def deadzone(self, deadzone: float) -> None:
        self._deadzone = deadzone

    @inverted.setter
    def inverted(self, inverted: bool) -> None:
        self._inverted = inverted

    @input_range.setter
    def input_range(self, input_range: range_util.Range) -> None:
        self._input_range = input_range

    @output_range.setter
    def output_range(self, output_range: range_util.Range) -> None:
        self._output_range = output_range

    def update(self, joystick: type(pygame.joystick.Joystick)) -> None:
        """Get the value of the axis from the controller. Used internally, Do not call this method directly outside
        the Controller class.

        Args:
            joystick (type(pygame.joystick.Joystick)):
                The joystick to get the axis value from.
        """
        # Get the raw value of the axis.
        value = joystick.get_axis(self._index)

        # Invert the value if necessary.
        if self._inverted:
            value = -value

        # Apply the deadzone to the value.
        deadzoned_value = self._apply_deadzone(value, deadzone=self._deadzone, input_range=self._input_range)

        # Scale the value to the output range.
        scaled_value = self._output_range.map(deadzoned_value, self._input_range)

        self._value = scaled_value

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
            The toggled state of the button.
        hold_delay (float):
            The hold delay of the button.
        pressed (bool):
            Whether the button is pressed.
        held (bool):
            Whether the button has been held for a preset amount of time.
        released (bool):
            Whether the button is released.
        just_pressed (bool):
            Whether the button had begun to be pressed during this frame.
        just_released (bool):
            Whether the button had begun to be released during this frame.

    Methods:
        update(joystick: type(pygame.joystick.Joystick)) -> None:
            Update the value of the button from the controller.
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

        self._hold_delay: float = 0.25
        self._pressed: bool = False
        self._held: bool = False
        self._released: bool = False
        self._just_pressed: bool = False
        self._just_released: bool = False

        self._last_pressed_time: float = 0.0

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
        self._pressed = not self._pressed
        self._toggled = not self._toggled

    @property
    def toggled(self) -> bool:
        """Whether the button is toggled."""
        return self._toggled

    @toggled.setter
    def toggled(self, value: bool) -> None:
        """Set whether the button is toggled."""
        self._toggled = value

    @property
    def hold_delay(self) -> float:
        """The period of unbroken time the button must be pressed before it is considered held.

        Returns:
            float: The hold delay of the button in seconds.
        """
        return self._hold_delay

    @hold_delay.setter
    def hold_delay(self, new_hold_delay: float) -> None:
        """Set the hold delay of the button.

        Args:
            new_hold_delay (float):
                The new hold delay of the button.
        """
        self._hold_delay = new_hold_delay

    @property
    def pressed(self) -> bool:
        """Return whether the button is pressed.

        Returns:
            bool: True if the button is pressed, False otherwise.
        """
        return self._pressed

    @pressed.setter
    def pressed(self, value: bool) -> None:
        """Set whether the button is pressed.

        Args:
            value (bool):
                The new value of the button.
        """
        self.update(value)

    @property
    def held(self) -> bool:
        """Return whether the button has been held for a preset amount of time.

        Returns:
            bool: True if the button is held, False otherwise.
        """
        return self._held

    @property
    def released(self) -> bool:
        """Return whether the button is released.

        Returns:
            bool: True if the button is released, False otherwise.
        """
        return self._released

    @property
    def just_pressed(self) -> bool:
        """Return whether the button had begun to be pressed during this frame.

        Returns:
            bool: True if the button was just pressed, False otherwise.
        """
        return self._just_pressed

    @property
    def just_released(self) -> bool:
        """Return whether the button had begun to be released during this frame.

        Returns:
            bool: True if the button was just released, False otherwise.
        """
        return self._just_released

    def update(self, val_source: type(pygame.joystick.Joystick) | bool) -> None:
        """Update the value of the button from the controller. Used internally, Do not call this method directly outside
        the Controller or Hat classes.

        Args:
            val_source (type(pygame.joystick.Joystick) | bool):
                Either the joystick to get the button value from or the value of the button itself if it is a boolean.
        """
        # Get the raw current value of the button.
        if isinstance(val_source, bool):
            state = val_source
        # elif isinstance(val_source, type(pygame.joystick.Joystick)):
        #     state = val_source.get_button(self._index)
        # else:
        #     raise TypeError(f"val_source must be a bool or a {type(pygame.joystick.JoystickType)}, " +
        #     "not {type(val_source)}.")
        else:
            state = val_source.get_button(self._index)

        # If the button is negated, invert the state.
        if self._negated:
            state = not state

        # Update the button states.

        # The button is considered just pressed if it was not pressed in the previous loop but is pressed now. The
        # opposite is true for just released.
        self._just_pressed = state and not self._pressed
        self._just_released = not state and self._pressed

        # Now, update whether the button is pressed, held, or released.
        self._pressed = state
        self._released = not self._pressed

        # The button is considered held if it is pressed and the time since the last press is greater than the hold
        # delay. This is similar to pressing a key on a keyboard and holding it down to get the key repeat.
        self._held = self._pressed and (time.time() - self._last_pressed_time) > self._hold_delay

        # Finally, update the last press time if the button was just pressed so that the hold delay can be calculated
        # correctly.
        if self._just_pressed:
            self.toggle()
            self._last_pressed_time = time.time()

    def toggle(self) -> None:
        """Alternate the toggled value of the button."""
        self._toggled = not self._toggled

    def __call__(self, *args, **kwargs):
        return self._pressed


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
        update(joystick: type(pygame.joystick.Joystick)) -> None:
            Update the value of the hat.
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

        self.buttons = {
            enums.ControllerHatButtonNames.DPAD_LEFT: Button(-1, negated=invert_x),
            enums.ControllerHatButtonNames.DPAD_RIGHT: Button(-1, negated=invert_x),
            enums.ControllerHatButtonNames.DPAD_UP: Button(-1, negated=invert_y),
            enums.ControllerHatButtonNames.DPAD_DOWN: Button(-1, negated=invert_y),
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
        self._invert_x = value

        self.buttons[enums.ControllerHatButtonNames.DPAD_LEFT].negated = value
        self.buttons[enums.ControllerHatButtonNames.DPAD_RIGHT].negated = value

    @property
    def invert_y(self) -> bool:
        """Whether to invert the y value of the hat."""
        return self._invert_y

    @invert_y.setter
    def invert_y(self, value: bool) -> None:
        """Set whether to invert the y value of the hat."""
        self._invert_y = value

        self.buttons[enums.ControllerHatButtonNames.DPAD_LEFT].negated = value
        self.buttons[enums.ControllerHatButtonNames.DPAD_RIGHT].negated = value

    def update(self, joystick: type(pygame.joystick.Joystick)) -> None:
        """Get the value of the hat from the controller.

        Args:
            joystick (type(pygame.joystick.Joystick)):
                The joystick to get the hat value from.
        """
        # Get the raw value of the hat.
        value = joystick.get_hat(self._index)

        self.buttons[enums.ControllerHatButtonNames.DPAD_LEFT].pressed = value[0] == -1
        self.buttons[enums.ControllerHatButtonNames.DPAD_RIGHT].pressed = value[0] == 1
        self.buttons[enums.ControllerHatButtonNames.DPAD_UP].pressed = value[1] == 1
        self.buttons[enums.ControllerHatButtonNames.DPAD_DOWN].pressed = value[1] == -1


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
        joystick (type(pygame.joystick.Joystick)):
            The joystick object to use.

    Methods:
        update() -> None:
            Update the controller state.
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

        self._joystick = None

    @property
    def index(self) -> int:
        """The index of the controller to use."""
        return self._index

    @property
    def joystick(self) -> type(pygame.joystick.Joystick):
        """The joystick object to use."""
        return self._joystick

    def initialize(self) -> None:
        """Initialize the controller."""
        self._joystick = pygame.joystick.Joystick(self._index)
        self._joystick.init()

    def update(self) -> None:
        """Update the values for the various inputs attached to the controller"""
        for btn in self.buttons:
            self.buttons[btn].update(self._joystick)

        for ax in self.axes:
            self.axes[ax].update(self._joystick)

        for hat in self.hats:
            self.hats[hat].update(self._joystick)

    def shutdown(self) -> None:
        """Shutdown the controller."""
        self.joystick.quit()
        pygame.quit()
