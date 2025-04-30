import math
import os.path
from copy import copy
from typing import Callable

from hardware.thruster_pwm import FrameThrusters
from enums import Directions, ControllerAxisNames, ControllerButtonNames, ThrusterPositions
import kinematics as kms
from mavlink_flight_controller import FlightController
from controller_input import combine_triggers
from io_systems.io_handler import IO
from dashboard import Dashboard
import enums

from utilities.vector import Vector3
# import utilities.cursor as cursor

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

    @property
    def inputs(self):
        return self.inputs

    @inputs.setter
    def inputs(self, value):
        self.inputs = value

    def loop(self):
        """Update thrust values, send commands, and more based on the inputs."""
        # Get the controller inputs, subscriptions, and i2c data and put them into local variables.
        inputs = self._io.controllers
        subscriptions = self._io.subscriptions
        # i2c = self._io.i2c_handler.i2cs

        controller = inputs[enums.ControllerNames.PRIMARY_DRIVER]

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

        # Get the depth data from the subscriptions if it exists.
        if "ROV/custom/depth_sensor/depth" in subscriptions:
            depth = subscriptions["ROV/custom/depth_sensor/depth"]
        else:
            depth = 0

        self._dash.get_entry("depth", None).set_value(f"Depth: {depth}")

        self._dash.update_images({
            "topview": gyro_orientation.yaw * 180 / math.pi,
            "frontview": gyro_orientation.roll * 180 / math.pi,
            "sideview": gyro_orientation.pitch * 180 / math.pi,
        })

        # print("(manual.py) gyro_orientation [degrees]:", gyro_orientation * 180 / math.pi)

        # Convert the triggers to a single value.
        right_trigger = controller.axes[ControllerAxisNames.RIGHT_TRIGGER]
        left_trigger = controller.axes[ControllerAxisNames.LEFT_TRIGGER]
        vertical = combine_triggers(right_trigger.value, left_trigger.value)

        # Convert the back buttons to a single value indicating desired roll thrust.
        right_bumper = controller.buttons[ControllerButtonNames.RIGHT_BUMPER]
        left_bumper = controller.buttons[ControllerButtonNames.LEFT_BUMPER]
        roll = combine_triggers(float(left_bumper.pressed), float(right_bumper.pressed))

        # print(controller.axes[ControllerAxisNames.LEFT_X].value)

        # # Update the target position of the ROV based on the controller inputs for the PID controllers.
        # self._kinematics.update_target_position(
        #     Vector3(
        #         controller.axes[ControllerAxisNames.RIGHT_X].value,
        #         controller.axes[ControllerAxisNames.RIGHT_Y].value,
        #         0,
        #     ),
        #     vertical,
        # )

        # # Get the mixed directions based on the controller inputs, gyro data, and PID outputs.
        # overall_thruster_impulses: dict[Directions, float] = self._kinematics.mix_directions(
        #     heading=Vector3(yaw=0, pitch=0, roll=0),
        #     lateral_target=Vector3(
        #         controller.axes[ControllerAxisNames.LEFT_X].value,
        #         controller.axes[ControllerAxisNames.LEFT_Y].value,
        #         vertical,
        #     ),
        #     rotational_target=Vector3(  # Set to zero because we are using PIDs for this. (No :P)
        #         yaw=controller.axes[ControllerAxisNames.RIGHT_X].value,
        #         pitch=controller.axes[ControllerAxisNames.RIGHT_Y].value,
        #         roll=0,
        #     ),
        #     pid_impulses={
        #         # Directions.YAW: self._kinematics.yaw_pid(gyro_orientation.yaw),
        #         # Directions.PITCH: self._kinematics.pitch_pid(gyro_orientation.pitch),
        #         # Directions.ROLL: self._kinematics.roll_pid(gyro_orientation.roll),
        #         # Directions.UP: self._kinematics.depth_pid(depth),
        #     },
        # )

        overall_thruster_impulses: dict[Directions, float] = {
            Directions.FORWARDS: controller.axes[ControllerAxisNames.LEFT_Y].value,
            Directions.RIGHT: controller.axes[ControllerAxisNames.LEFT_X].value,
            Directions.UP: vertical,
            Directions.YAW: controller.axes[ControllerAxisNames.RIGHT_X].value,
            Directions.PITCH: controller.axes[ControllerAxisNames.RIGHT_Y].value,
            Directions.ROLL: roll,
        } 

        # cursor.clear_screen()
        # cursor.set_pos(0, 0)
        # print("Overall thruster impulses:")
        # for pos in Directions:
        #     print(pos, overall_thruster_impulses[pos])

        # Get the PWM values for the thrusters based on the controller inputs.
        pwm_values: dict[ThrusterPositions, int] = self._frame.get_pwm_values(
            overall_thruster_impulses
        )



        # print("Torques:")
        # for pos in ThrusterPositions:
        #     print(pos, self._frame.thrusters[pos].torques)
        # Theoretically stop the ROV from moving if the B button is toggled. TODO: Fix.
        stop = controller.buttons[ControllerButtonNames.B].toggled

        # # Calibrate the gyro if the Y button is pressed.
        # if controller.buttons[ControllerButtonNames.Y].just_pressed:
        #     self._flight_controller.calibrate_gyro()

        # # Update the PID values if the X button is pressed.
        # if controller.buttons[ControllerButtonNames.X].just_pressed:
        #     self._update_pid_values(self._rov_directory + "/assets/pid_config.json")

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

    # def _update_pid_values(self, file_path: str) -> None:
    #     """Update the PID values based on the file contents.

    #     Args:
    #         file_path (str):
    #             The path to the pid config file.
    #     """
    #     with open(file_path, "r") as file:
    #         file_contents = json.load(file)

    #     self._kinematics.yaw_pid.Kd = file_contents["yaw"]["P"]
    #     self._kinematics.yaw_pid.Kp = file_contents["yaw"]["I"]
    #     self._kinematics.yaw_pid.Ki = file_contents["yaw"]["D"]

    #     self._kinematics.pitch_pid.Kd = file_contents["pitch"]["P"]
    #     self._kinematics.pitch_pid.Kp = file_contents["pitch"]["I"]
    #     self._kinematics.pitch_pid.Ki = file_contents["pitch"]["D"]

    #     self._kinematics.roll_pid.Kd = file_contents["roll"]["P"]
    #     self._kinematics.roll_pid.Kp = file_contents["roll"]["I"]
    #     self._kinematics.roll_pid.Ki = file_contents["roll"]["D"]

    #     self._kinematics.depth_pid.Kd = file_contents["depth"]["P"]
    #     self._kinematics.depth_pid.Kp = file_contents["depth"]["I"]
    #     self._kinematics.depth_pid.Ki = file_contents["depth"]["D"]

    def shutdown(self):
        """Shutdown the ROV."""
        # TODO: Add any shutdown logic here.
        pass
