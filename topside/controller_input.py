import pygame

import enums
import controller as ctrl


class InputHandler:
    """Handles the input from the controllers.

    Properties:
        controllers (dict[enums.ControllerNames, ctrl.Controller]):
            The controllers to use.

    Methods:
        update() -> None:
            Update the Controller input objects.
        shutdown() -> None:
            Shutdown the InputHandler.
    """

    def __init__(self, controllers: dict[enums.ControllerNames, ctrl.Controller]) -> None:
        """Initialize the InputHandler object.

        Args:
            controllers (dict[enums.ControllerNames, ctrl.Controller]):
                The controllers to use.
        """
        self.controllers = controllers

        pygame.init()
        pygame.joystick.init()

        # Initialize the controllers.
        for controller in controllers:
            controllers[controller].initialize()

    def update(self) -> None:
        """Update the Controller input objects."""
        pygame.event.pump()

        for controller in self.controllers:
            self.controllers[controller].update()

    def shutdown(self) -> None:
        for controller in self.controllers:
            self.controllers[controller].shutdown()


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
