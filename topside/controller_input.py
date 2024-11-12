"""Gets input from a controller and maps it to the controls in the config file."""

# pylint: disable=wildcard-import, unused-import, unused-wildcard-import

import pygame
from typing import Callable, NamedTuple

from utilities.personal_functions import *

from config import ControllerConfig, InputFunction
#
# from surface_main import MainSystem


def combine_triggers(trigger_1: float, trigger_2: float) -> float:
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

    return trigger_2 - trigger_1


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

    _config: ControllerConfig

    # , main_system: MainSystem, config: ControllerConfig
    def __init__(self, config: ControllerConfig, rov_dir: str):
        self._config = config

        pygame.init()
        pygame.joystick.init()

        # self.main_system = main_system
        # self.config = config
        self.rov_dir = rov_dir

        self.control_map = {}
        # self.deadzone = 0.1


        if pygame.joystick.get_count() != 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            self._get_control_map()
        else:
            # TODO Replace error()
            print("Warning! No controller detected!")

    def get_inputs(self) -> dict[str, float]:
        """Retrieves the inputs from the controller.

        Returns:
            dict: The inputs from the controller as float amplitude values (buttons are 1/0).
        """
        pygame.event.pump()


        inputs: dict = self._get_buttons() | self._get_joysticks() | self._get_hat()

        return inputs

    def get_controller_commands(self) -> dict[str, float]:
        """Get the commands from the controller.

        Returns:
            dict[str, float]: The commands from the controller and their emphasis.
        """
        commands = {}
        controller_inputs = self.get_inputs()

        print("Control map: " + str(self.control_map))

        # Sorts through all buttons attached to listed commands.
        for control in self.control_map:
            for button in self.control_map[control]:

                # Set the default value in case something screws up.
                commands[control] = 0

                # If the button is pressed, and it's more than the current value, update the value.
                if controller_inputs[button]:
                    commands[control] = (controller_inputs[button] if abs(controller_inputs[button])
                                         >= abs(commands[control]) else commands[control])

        return commands

    def _get_buttons(self) -> dict[str, float]:
        """Returns a dictionary containing the current state of the buttons on the controller.

        Returns:
            dict[str, float]: A dictionary mapping the button names to their states
                which are formatted as 0 (off) or 1 (on).
        """
        values = {
            "A": self._button(0),
            "B": self._button(1),
            "X": self._button(2),
            "Y": self._button(3),
            "LEFT_BUMPER": self._button(4),
            "RIGHT_BUMPER": self._button(5),
            "SELECT": self._button(6),
            "START": self._button(7),
        }

        return values

    def _get_joysticks(self) -> dict[str, float]:
        """Returns a dictionary containing the values of various joystick axes.

        Returns:
            dict: The values of the joystick and trigger axes ("Chop chop!").
        """
        values = {
            "LEFT_X": self._axis(0),
            "LEFT_Y": -self._axis(1),
            "RIGHT_X": self._axis(2),
            "RIGHT_Y": -self._axis(3),
            "TRIGGERS": combine_triggers(self._axis(4), self._axis(5)),
        }

        return values

    def _get_hat(self) -> dict[str, float]:
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

    def _button(self, number: int) -> float:
        """Returns the state of the specified button on the joystick.

        Args:
            number (int):
                The button number to check.

        Returns:
            float: 1 if the button is pressed, 0 otherwise.
        """
        return 1 if self.joystick.get_button(number) else 0

    def _axis(self, number: int) -> float:
        """Returns the value of the specified axis on the joystick after applying a deadzone.

        Args:
            number (int):
                The axis number to check.

        Returns:
            float: The value of the axis.
        """
        axis_config = self._config.axes[number]
        return self._apply_deadzone(self.joystick.get_axis(number), axis_config.deadband)

    @classmethod
    def _apply_deadzone(value: float, deadzone: float) -> float:
        """Applies a deadzone to the input value.

        Args:
            value (float):
                The input value to apply the deadzone to.

        Returns:
            float: The input value with the deadzone applied.
        """
        if abs(value) < deadzone:
            return 0

        return value

    def _get_control_map(self) -> dict:
        """Get the controls and map them to the keys in the file.

        Returns:
            dict: The controls and their keys.
        """

        # Get the control config file.
        path = os.path.join(self.rov_dir, "config-controls.fangr")  # Funny Absolute Notation for Gamepad Readings

        # Extract data from the file.
        with open(path, "r", encoding="UTF-8") as file:
            file_lines = file.readlines()[:]
            file.close()

        self.control_map = {}

        # Turn the data into a dictionary, stopping at the first #.
        for line in file_lines:
            print(line.strip())

            if line.startswith("#"):
                print("Returning: " + str(self.control_map))
                return
            elif line == "\n":
                continue

            # Remove comments and whitespace.
            line = line.split("#")[0].strip()

            # Split the line into the control and button.
            control = line.split("=")

            button = control[1].strip().upper()
            ctrl = control[0].strip().upper()

            # Add the control to the dictionary.
            if ctrl not in self.control_map:
                self.control_map[ctrl] = []

            self.control_map[ctrl].append(button)


if __name__ == "__main__":
    # Test the controller code
    controller = Controller("rovs/spike")

    while True:
        inputs = controller.get_controller_commands()

        print(inputs)

        time.sleep(0.1)
