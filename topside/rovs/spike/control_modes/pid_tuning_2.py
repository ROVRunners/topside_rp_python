import json
import math
import os.path
from copy import copy
from typing import Callable

from hardware.thruster_pwm import FrameThrusters
from enums import Directions, ControllerAxisNames, ControllerButtonNames, ThrusterPositions, ControllerNames, ControllerHatNames, ControllerHatButtonNames
import kinematics as kms
from controller_input import combine_triggers
from io_systems.io_handler import IO
from dashboard import Dashboard
from mavlink_flight_controller import FlightController

from utilities.vector import Vector3

from rovs.generic_objects.generic_control_mode import ControlMode


class PIDTuning2(ControlMode):
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

    def __init__(self, frame: FrameThrusters, io: IO, kinematics: kms.Kinematics, flight_controller: FlightController,
                 dash: Dashboard, set_control_mode: Callable) -> None:
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
            flight_controller (FlightController):
                The flight controller object.
            dash (Dashboard):
                The Tkinter Dashboard object.
            set_control_mode (Callable):
                The function to set the control mode.
        """
        super().__init__(frame, io, kinematics, set_control_mode, dash)

        self._flight_controller = flight_controller

        self._rov_directory = os.path.dirname(os.path.dirname(__file__))

        self._inputs = self._io.controllers
        self._controller = self._inputs[ControllerNames.PRIMARY_DRIVER]

        self._controller.buttons[ControllerButtonNames.B].toggled = True

        # The trim values for the rotational velocity inputs used to compensate for drift.
        self._omega_trim = Vector3(yaw=0, pitch=0, roll=0)

    @property
    def inputs(self):
        return self.inputs

    @inputs.setter
    def inputs(self, value):
        self.inputs = value

    def loop(self):
        """Update thrust values, send commands, and more based on the inputs."""
        # Get the controller inputs, subscriptions, and i2c data and put them into local variables.
        subscriptions = self._io.subscriptions
        # i2c = self._io.i2c_handler.i2cs

        # mavlink = subscriptions["mavlink"]
        mavlink = {}
        for key, val in subscriptions.items():
            path = key.split("/")
            if path[1] == "mavlink":
                mavlink[path[2]] = val

        # Get the gyro data from the subscriptions if it exists.
        # if "imu" in i2c:
        #     self._imu.update(i2c["imu"])
        #     gyro_yaw = self._imu.yaw
        #     gyro_pitch = self._imu.pitch
        #     gyro_roll = self._imu.roll
        # else:
        #     gyro_yaw = 0
        #     gyro_pitch = 0
        #     gyro_roll = 0

        self._flight_controller.update(mavlink)

        gyro_orientation: Vector3 = copy(self._flight_controller.attitude)
        gyro_omega: Vector3 = copy(self._flight_controller.attitude_speed)

        # Get the depth data from the subscriptions if it exists.
        if "ROV/custom/depth_sensor/depth" in subscriptions:
            depth = subscriptions["ROV/custom/depth_sensor/depth"]
        else:
            depth = 0

        # self._dash.get_entry("Depth", None).set_value(f"Depth: {depth}")

        self._dash.update_images({
            "topview": 360 - gyro_orientation.yaw * 180 / math.pi,
            "frontview": 360 - gyro_orientation.roll * 180 / math.pi,
            "sideview": 360 - gyro_orientation.pitch * 180 / math.pi,
        })

        # Convert the triggers to a single value.
        right_trigger = self._controller.axes[ControllerAxisNames.RIGHT_TRIGGER]
        left_trigger = self._controller.axes[ControllerAxisNames.LEFT_TRIGGER]
        vertical_speed = combine_triggers(left_trigger.value, right_trigger.value)

        # Convert the back buttons to a single value indicating desired roll thrust.
        right_bumper = self._controller.buttons[ControllerButtonNames.RIGHT_BUMPER]
        left_bumper = self._controller.buttons[ControllerButtonNames.LEFT_BUMPER]
        roll_speed = 2*combine_triggers(float(left_bumper.pressed), float(right_bumper.pressed))

        # Get the values from the controller hat (D-Pad) to adjust the trim values.
        if self._controller.hats[ControllerHatNames.DPAD].buttons[ControllerHatButtonNames.DPAD_UP].held:
            self._omega_trim.pitch += 0.01
        if self._controller.hats[ControllerHatNames.DPAD].buttons[ControllerHatButtonNames.DPAD_DOWN].held:
            self._omega_trim.pitch -= 0.01
        if self._controller.hats[ControllerHatNames.DPAD].buttons[ControllerHatButtonNames.DPAD_LEFT].held:
            self._omega_trim.roll += 0.01
        if self._controller.hats[ControllerHatNames.DPAD].buttons[ControllerHatButtonNames.DPAD_RIGHT].held:
            self._omega_trim.roll -= 0.01

        # Update the target position of the ROV based on the controller inputs for the PID controllers.
        self._kinematics.update_target_position(
            Vector3(
                yaw=0,  # Doing this manually
                pitch=self._controller.axes[ControllerAxisNames.RIGHT_Y].value,
                roll=roll_speed,
            ),
            vertical_speed,
        )

        # Get the mixed directions based on the controller inputs, gyro data, and PID outputs.
        overall_thruster_impulses: dict[Directions, float] = self._kinematics.mix_directions(
            heading=gyro_orientation,
            lateral_target=Vector3(
                self._controller.axes[ControllerAxisNames.LEFT_X].value,
                self._controller.axes[ControllerAxisNames.LEFT_Y].value,
                0,  # Set to zero because we are using PIDs for this.
            ),
            rotational_target=Vector3(  # Set to zero because we are using PIDs for this.
                yaw=self._controller.axes[ControllerAxisNames.RIGHT_X].value,
                pitch=0,
                roll=0,
            ),
            pid_impulses={
                # Directions.YAW: self._kinematics.yaw_pid(gyro_orientation.yaw + self._omega_trim.yaw),
                Directions.PITCH: self._kinematics.pitch_pid(-gyro_omega.pitch + self._omega_trim.pitch),
                Directions.ROLL: self._kinematics.roll_pid(-gyro_omega.roll + self._omega_trim.roll),
                Directions.UP: self._kinematics.depth_pid(depth),
            },
        )

        # Get the PWM values for the thrusters based on the controller inputs.
        pwm_values: dict[ThrusterPositions, int] = self._frame.get_pwm_values(
            overall_thruster_impulses
        )

        # Theoretically stop the ROV from moving if the B button is toggled.
        stop = self._controller.buttons[ControllerButtonNames.B].toggled

        # # Calibrate the gyro if the Y button is pressed.
        # if controller.buttons[ControllerButtonNames.Y].just_pressed:
        #     self._flight_controller.calibrate_gyro()

        # Update the PID values if the X button is pressed.
        if self._controller.buttons[ControllerButtonNames.X].just_pressed:
            self._update_pid_values(self._rov_directory + "/assets/pid_config.json")

        # TODO: Add a keybind or several keybinds to change control modes.
        # self._set_control_mode(enums.ControlModes.MANUAL)

        # Publish the PWM values to the MQTT broker.
        for thruster, pwm in pwm_values.items():
            # If the stop button is toggled, set the PWM to 1500, stopping the thrusters. This is useful for testing and
            # emergency situations where the thrusters are above water.
            if stop:
                pwm = 1500

            # Set the PWM value for the thruster.
            self._io.gpio_handler.pins[thruster].val = pwm

        # self._io.rov_comms.publish_commands({
        #     "stop": stop,
        # })

    def _update_pid_values(self, file_path: str) -> None:
        """Update the PID values based on the file contents.

        Args:
            file_path (str):
                The path to the pid config file.
        """
        with open(file_path, "r") as file:
            file_contents = json.load(file)

        self._kinematics.yaw_pid.Kd = file_contents["yaw"]["P"]
        self._kinematics.yaw_pid.Kp = file_contents["yaw"]["I"]
        self._kinematics.yaw_pid.Ki = file_contents["yaw"]["D"]

        self._kinematics.pitch_pid.Kd = file_contents["pitch"]["P"]
        self._kinematics.pitch_pid.Kp = file_contents["pitch"]["I"]
        self._kinematics.pitch_pid.Ki = file_contents["pitch"]["D"]

        self._kinematics.roll_pid.Kd = file_contents["roll"]["P"]
        self._kinematics.roll_pid.Kp = file_contents["roll"]["I"]
        self._kinematics.roll_pid.Ki = file_contents["roll"]["D"]

        self._kinematics.depth_pid.Kd = file_contents["depth"]["P"]
        self._kinematics.depth_pid.Kp = file_contents["depth"]["I"]
        self._kinematics.depth_pid.Ki = file_contents["depth"]["D"]

    def shutdown(self):
        """Shutdown the ROV."""
        # TODO: Add any shutdown logic here.
        pass
