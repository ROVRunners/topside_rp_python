import pygame

import enums
import config.controller as ctrl


class InputHandler:
    """Handles the input from the controllers.

    Properties:
        controllers (dict[enums.ControllerNames, ctrl.Controller]):
            The controllers to use.

    Methods:
        get_inputs() -> dict[enums.ControllerButtonNames | enums.ControllerAxisNames, float]:
            Get the inputs from the controllers.
        get_toggled_inputs() -> dict[enums.ControllerHatButtonNames | enums.ControllerButtonNames, bool]:
            Get the toggled state of the buttons on the controllers.
        get_controller(controller: enums.ControllerNames) -> ctrl.Controller:
            Get the controller object.
    """

    def __init__(self, controllers: dict[enums.ControllerNames, ctrl.Controller]) -> None:
        """Initialize the InputHandler object.

        Args:
            controllers (dict[enums.ControllerNames, ctrl.Controller]):
                The controllers to use.
        """
        self.controllers = controllers

        self._toggled_inputs: dict[enums.ControllerNames, dict[enums.ControllerHatButtonNames |
                                                               enums.ControllerButtonNames, bool]] = {}

    def get_inputs(self) -> dict[enums.ControllerNames, dict[enums.ControllerButtonNames |
                                                             enums.ControllerAxisNames |
                                                             enums.ControllerHatButtonNames, float]]:
        """Get the inputs from the controllers.

        Returns:
            dict[enums.ControllerNames, dict[enums.ControllerButtonNames | enums.ControllerAxisNames, float]]:
                The inputs from the controllers.
        """
        pygame.event.pump()

        inputs: dict[enums.ControllerNames, dict[enums.ControllerButtonNames |
                                                 enums.ControllerAxisNames |
                                                 enums.ControllerHatButtonNames, float]] = {}

        for controller in self.controllers:
            inputs[controller] = self.controllers[controller].get_inputs()

        self._update_toggled_inputs()

        return inputs

    def get_toggled_inputs(self) -> dict[enums.ControllerNames, dict[enums.ControllerHatButtonNames |
                                                                     enums.ControllerButtonNames, bool]]:
        """Get the toggled state of the buttons on the controllers.

        Returns:
            dict[enums.ControllerNames, dict[enums.ControllerHatButtonNames | enums.ControllerButtonNames, bool]]:
                The toggled state of the buttons on the controllers.
        """
        return self._toggled_inputs

    def _update_toggled_inputs(self) -> None:
        """Update the toggled state of the buttons on the controller and store the values."""
        for controller in self.controllers:
            self.controllers[controller].update_toggles()
            self._toggled_inputs[controller] = self.controllers[controller].get_toggled_inputs()

    def get_controller(self, controller: enums.ControllerNames) -> ctrl.Controller:
        """Get the controller object.

        Args:
            controller (enums.ControllerNames):
                The controller to get.

        Returns:
            ctrl.Controller: The controller object.
        """
        return self.controllers[controller]


def combine_triggers(positive_trigger: float, negative_trigger: float) -> float:
    """Combines the values of the two triggers into a single value.

    Args:
        positive_trigger (float):
            The value of the positive trigger.
        negative_trigger (float):
            The value of the negative trigger.

    Returns:
        float: The combined value of the triggers.
    """
    # Normalize the triggers to a 0-1 range.
    positive_trigger = (positive_trigger + 1) / 2
    negative_trigger = (negative_trigger + 1) / 2

    return positive_trigger - negative_trigger
