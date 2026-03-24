import os.path
from typing import Callable

from hardware.thruster_pwm import FrameThrusters
from enums import Directions, ControllerAxisNames, ControllerButtonNames, ThrusterPositions, ControllerNames
import kinematics as kms
from controller_input import combine_triggers
from io_systems.io_handler import IO
from dashboard import Dashboard

from rovs.generic_objects.generic_control_mode import ControlMode


class PureManual(ControlMode):
    """One of the control modes for the ROV which take in inputs from the controller, sensors, and more to determine
    the thrust values for the thrusters and send other commands to the ROV.

    This is the manual control mode which only takes in pure controller inputs to determine the thrust values for the
    thrusters.

    Methods:
        loop() -> None:
            Update thrust values, send commands, and more based on the inputs.
        shutdown() -> None:
            Shutdown the ROV.
    """

    def __init__(self, frame: FrameThrusters, io: IO, kinematics: kms.Kinematics, set_control_mode: Callable,
                 dash: Dashboard) -> None:
        """Initialize the Manual object.

        Args:
            frame (FrameThrusters):
                The objects of the thrusters mounted to the frame.
            io (IO):
                The IO (input output) object.
            kinematics (kms.Kinematics):
                The Kinematics object housing the PIDs.
            set_control_mode (Callable):
                The function to set the control mode.
            dash (Dashboard):
                The Tkinter Dashboard object.
        """
        super().__init__(frame, io, kinematics, set_control_mode, dash)

        self._rov_directory = os.path.dirname(os.path.dirname(__file__))

    @property
    def inputs(self):
        return self._inputs

    @inputs.setter
    def inputs(self, value):
        self._inputs = value

    def loop(self):
        """Update thrust values, send commands, and more based on the inputs."""
        self._inputs = self._io.controllers
        # subscriptions = self._io.subscriptions

        controller = self._inputs[ControllerNames.PRIMARY_DRIVER]

        # self._dash.update_images({
        #     "topview": gyro_yaw,
        #     "frontview": gyro_roll,
        #     "sideview": gyro_pitch
        # })

        # Convert the triggers to a single value.
        right_trigger = controller.axes[ControllerAxisNames.RIGHT_TRIGGER]
        left_trigger = controller.axes[ControllerAxisNames.LEFT_TRIGGER]
        vertical = combine_triggers(left_trigger.value, right_trigger.value)

        # TODO: add sensor data to pids below
        # Get the PWM values for the thrusters based on the controller inputs.
        self._frame.update_thruster_output(
            {
                Directions.FORWARDS: controller.axes[ControllerAxisNames.LEFT_Y].value,
                Directions.RIGHT: controller.axes[ControllerAxisNames.LEFT_X].value,
                Directions.UP: vertical,
                Directions.YAW: controller.axes[ControllerAxisNames.RIGHT_X].value,
                Directions.PITCH: controller.axes[ControllerAxisNames.RIGHT_Y].value,
                Directions.ROLL: (
                        controller.buttons[ControllerButtonNames.RIGHT_BUMPER].pressed -
                        controller.buttons[ControllerButtonNames.LEFT_BUMPER].pressed
                )
            },
        )

        pwm_values: dict[ThrusterPositions, int] = self._frame.pwm

        # Theoretically stop the ROV from moving if the B button is toggled. TODO: Fix.
        stop = controller.buttons[ControllerButtonNames.B].toggled

        # TODO: Add a keybind or several keybinds to change control modes.
        # self._set_control_mode(enums.ControlModes.MANUAL)

        # Publish the PWM values to the MQTT broker.
        for thruster, pwm in pwm_values.items():
            self._io.gpio_handler.pins[thruster].val = pwm

        self._io.rov_comms.publish_commands({
            "stop": stop,
        })

    def shutdown(self):
        """Shutdown the ROV."""
        # TODO: Add any shutdown logic here.
        pass
