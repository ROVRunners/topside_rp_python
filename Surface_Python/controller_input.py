"""Gets input from a controller and maps it to the controls in the config file."""
# pylint: disable=wildcard-import, unused-import, unused-wildcard-import
import os
import pygame

from utilities.personal_functions import *
from config import ControllerConfig


class Controller:
    """Class for handling controller input.
    
    Functions:
    
    get_inputs() -> dict[str, float]:
        Retrieves the inputs from the controller.

    get_buttons() -> dict[str, float]:
        Returns a dictionary containing the current state of the buttons on the controller.

    get_joysticks() -> dict[str, float]:
        Returns a dictionary containing the values of various joystick axes.

    get_hat() -> dict[str, float]:
        Get the values of the D-Pad on the controller.

    button(number: int) -> float:
        Returns the state of the specified button on the joystick.

    axis(number: int) -> float:
        Returns the value of the specified axis on the joystick after applying a deadzone.

    combine_triggers(trigger_1: float, trigger_2: float) -> float:
        Combines the values of the two triggers into a single value.

    apply_deadzone(value: float) -> float:
        Applies a deadzone to the input value.

    get_controls() -> dict:
        Get the controls and map them to the keys in the file.
        """

    def __init__(self, config: ControllerConfig):
        pygame.init()
        pygame.joystick.init()

        self.config = config
        self.control_map = {}

        if not pygame.joystick.get_count() == 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            self.get_controls()
        else:
            error("Warning! No controller detected!")

    def get_inputs(self) -> dict[str, float]:
        """Retrieves the inputs from the controller.

        Returns:
            dict: The inputs from the controller as float amplitude values (buttons are 1/0).
        """
        pygame.event.pump()
        inputs = self.get_buttons() | self.get_joysticks() | self.get_hat()

        return inputs

    def get_buttons(self) -> dict[str, float]:
        """Returns a dictionary containing the current state of the buttons on the controller.

        Returns:
            dict[str, float]: A dictionary mapping the button names to their states
                which are formatted as 0 (off) or 1 (on).
        """
        values = {
            "A": self.button(0),
            "B": self.button(1),
            "X": self.button(2),
            "Y": self.button(3),
            "LEFT_BUMPER": self.button(4),
            "RIGHT_BUMPER": self.button(5),
            "SELECT": self.button(6),
            "START": self.button(7),
        }

        return values

    def get_joysticks(self) -> dict[str, float]:
        """Returns a dictionary containing the values of various joystick axes.

        Returns:
            dict: The values of the joystick and trigger axes ("Chop chop!").
        """
        values = {
            "LEFT_X": self.axis(0),
            "LEFT_Y": self.axis(1),
            "RIGHT_X": self.axis(2),
            "RIGHT_Y": self.axis(3),
            "TRIGGERS": self.combine_triggers(self.axis(4), self.axis(5)),
        }

        return values

    def get_hat(self) -> dict[str, float]:
        """Get the values of the D-Pad on the controller.
            
        Returns:
            dict: The values of the D-Pad buttons in 1/0 format.
        """
        coords = self.joystick.get_hat(0)
        values = {
            "DPAD_UP": coords[1] == 1,
            "DPAD_DOWN": coords[1] == -1,
            "DPAD_LEFT": coords[0] == -1,
            "DPAD_RIGHT": coords[0] == 1,
        }

        return values

    def button(self, number: int) -> float:
        """Returns the state of the specified button on the joystick.

        Args:
            number (int):
                The button number to check.

        Returns:
            float: 1 if the button is pressed, 0 otherwise.
        """
        return 1 if self.joystick.get_button(number) else 0

    def axis(self, number: int) -> float:
        """Returns the value of the specified axis on the joystick after applying a deadzone.

        Args:
            number (int):
                The axis number to check.

        Returns:
            float: The value of the axis.
        """
        return self.apply_deadzone(self.joystick.get_axis(number))

    def combine_triggers(self, trigger_1: float, trigger_2: float) -> float:
        """Combines the values of the two triggers into a single value.

        Args:
            trigger_1 (float):
                The value of the first trigger.
            trigger_2 (float):
                The value of the second trigger.

        Returns:
            float: The combined value of the triggers.
        """
        trigger_1 = (trigger_1 + 1) / 2
        trigger_2 = (trigger_2 + 1) / 2

        return trigger_1 - trigger_2

    def apply_deadzone(self, value: float) -> float:
        """Applies a deadzone to the input value.

        Args:
            value (float):
                The input value to apply the deadzone to.

        Returns:
            float: The input value with the deadzone applied.
        """
        if abs(value) < self.deadzone:
            return 0

        return value

    def get_controls(self) -> dict:
        """Get the controls and map them to the keys in the file.

        Returns:
            dict: The controls and their keys.
        """

        # Get the control config file.
        path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(path, "config")
        path = os.path.join(path, "config-controls.fangr") # Funny Absolute Notation for Gamepad Readings

        # Extract data from the file.
        file = open(path, "r", encoding="UTF-8")
        file_lines = file.readlines()[:]
        file.close()

        control_map = {}

        # Turn the data into a dictionary, stopping at the first #.
        for line in file_lines:

            if line.startswith("#"):
                return control_map
            elif line == "\n":
                continue

            # Remove comments and whitespace.
            line = line.split("#")[0].strip()

            control = line.split("=")

            button = control[1].strip().upper()
            ctrl = control[0].strip().upper()

            if ctrl not in control_map:
                control_map[ctrl] = []

            control_map[ctrl].append(button)

        self.control_map = control_map

