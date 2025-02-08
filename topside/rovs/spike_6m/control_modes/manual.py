import json
import os.path
from typing import Callable

from hardware.thruster_pwm import FrameThrusters
from enums import Directions, ControllerAxisNames, ControllerButtonNames, ThrusterPositions
import kinematics as kms
from controller_input import combine_triggers
from io_systems.io_handler import IO
from dashboard import Dashboard

from utilities.vector import Vector3

from rovs.generic_objects.generic_control_mode import ControlMode


class Manual(ControlMode):
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
        return self.inputs

    @inputs.setter
    def inputs(self, value):
        self.inputs = value

    def loop(self):
        """Update thrust values, send commands, and more based on the inputs."""
        inputs = self._io.controllers
        subscriptions = self._io.subscriptions

        controller = inputs[enums.ControllerNames.PRIMARY_DRIVER]

        # Get the depth data from the subscriptions if it exists.
        if "ROV/sensor_data/depth" in subscriptions:
            depth = subscriptions["ROV/sensor_data/depth"]
        else:
            depth = 0

        # self._dash.update_images({
        #     "topview": gyro_yaw,
        #     "frontview": gyro_roll,
        #     "sideview": gyro_pitch
        # })

        # Convert the triggers to a single value.
        right_trigger = controller.axes[ControllerAxisNames.RIGHT_TRIGGER]
        left_trigger = controller.axes[ControllerAxisNames.LEFT_TRIGGER]
        vertical = combine_triggers(left_trigger.value, right_trigger.value)

        self._kinematics.update_target_position(
            Vector3(
                controller.axes[ControllerAxisNames.RIGHT_X].value,
                controller.axes[ControllerAxisNames.RIGHT_Y].value,
                0,
            ),
            vertical,
        )

        # TODO: add sensor data to pids below
        # Get the PWM values for the thrusters based on the controller inputs.
        pwm_values: dict[ThrusterPositions, int] = self._frame.get_pwm_values(
            {
                Directions.FORWARDS: controller.axes[ControllerAxisNames.LEFT_Y].value,
                Directions.RIGHT: controller.axes[ControllerAxisNames.LEFT_X].value,
                Directions.UP: self._kinematics.depth_pid(depth),
                Directions.YAW: self._kinematics.yaw_pid(gyro_yaw),
                Directions.PITCH: self._kinematics.pitch_pid(gyro_pitch),
                Directions.ROLL: self._kinematics.roll_pid(gyro_roll),
            },
        )

        # Theoretically stop the ROV from moving if the B button is toggled. TODO: Fix.
        stop = controller.buttons[ControllerButtonNames.B].toggled

        # Update the PID values if the X button is pressed.
        if controller.buttons[ControllerButtonNames.X].just_pressed:
            self._update_pid_values(self._rov_directory + "/assets/pid_config.json")

        # TODO: Add a keybind or several keybinds to change control modes.
        # self._set_control_mode(enums.ControlModes.MANUAL)

        # Publish the PWM values to the MQTT broker.
        for thruster, pwm in pwm_values.items():
            self._io.gpio_handler.pins[thruster].val = pwm

        self._io.rov_comms.publish_commands({
            "stop": stop,
        })

    def _update_pid_values(self, file_path: str) -> None:
        """Update the PID values based on the file contents.

        Args:
            file_path (str):
                The path to the pid config file.
        """
        with open(file_path, "r") as file:
            file_contents = json.load(file)

        self._kinematics.yaw_pid.Kd = file_contents["yaw"]["D"]
        self._kinematics.yaw_pid.Kp = file_contents["yaw"]["P"]
        self._kinematics.yaw_pid.Ki = file_contents["yaw"]["I"]

        self._kinematics.pitch_pid.Kd = file_contents["pitch"]["D"]
        self._kinematics.pitch_pid.Kp = file_contents["pitch"]["P"]
        self._kinematics.pitch_pid.Ki = file_contents["pitch"]["I"]

        self._kinematics.roll_pid.Kd = file_contents["roll"]["D"]
        self._kinematics.roll_pid.Kp = file_contents["roll"]["P"]
        self._kinematics.roll_pid.Ki = file_contents["roll"]["I"]

        self._kinematics.depth_pid.Kd = file_contents["depth"]["D"]
        self._kinematics.depth_pid.Kp = file_contents["depth"]["P"]
        self._kinematics.depth_pid.Ki = file_contents["depth"]["I"]

    def shutdown(self):
        """Shutdown the ROV."""
        # TODO: Add any shutdown logic here.
        pass
