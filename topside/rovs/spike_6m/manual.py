"""
"""

from hardware.thruster_pwm import FrameThrusters
import enums
import kinematics as kms
from imu import IMU
import controller_input
from io_systems.io_handler import IO
from utilities.vector import Vector3
from dashboard import Dashboard


class Manual:
    """The manual control class for the ROV.
    takes an inputs and maps and sends outputs to the rov connection
    """

    def __init__(self, frame: FrameThrusters, io: IO, kinematics: kms.Kinematics, imu: IMU, dash: Dashboard) -> None:
        """Initialize the Manual object.

        Args:
            frame (FrameThrusters):
                The objects of the thrusters mounted to the frame.
            io (IO):
                The IO (input output) object.
            kinematics (kms.Kinematics):
                The Kinematics object housing the PIDs.
        """
        self._frame = frame
        self._io = io
        self._kinematics = kinematics
        self._imu = imu
        self._dash = dash

        self._imu.initialize_imu(self._io.i2c_handler.i2cs["imu"])

        # Add whatever you need initialized here.

    @property
    def inputs(self):
        return self.inputs

    @inputs.setter
    def inputs(self, value):
        self.inputs = value

    def loop(self):
        """Update thrust values, send commands, and more based on the inputs."""
        inputs = self._io.controllers

        controller = inputs[enums.ControllerNames.PRIMARY_DRIVER]

        subscriptions = self._io.subscriptions
        i2c = self._io.i2c_handler.i2cs

        # Get the gyro data from the subscriptions if it exists.
        if "imu" in i2c:
            self._imu.update(i2c["imu"])
            gyro_yaw = self._imu.yaw
            gyro_pitch = self._imu.pitch
            gyro_roll = self._imu.roll
            print(gyro_yaw)
        else:
            gyro_yaw = 0
            gyro_pitch = 0
            gyro_roll = 0

        # Get the accelerometer data from the subscriptions if it exists.
        if "imu" in i2c:
            accel_x = self._imu.accel_x
            accel_y = self._imu.accel_y
            accel_z = self._imu.accel_z
        else:
            accel_x = 0
            accel_y = 0
            accel_z = 0

        # Get the depth data from the subscriptions if it exists.
        if "ROV/sensor_data/depth" in subscriptions:
            depth = subscriptions["ROV/sensor_data/depth"]
        else:
            depth = 0

        # Get the leak warning data from the subscriptions if it exists.
        if "ROV/sensor_data/leak" in subscriptions:
            leak = subscriptions["ROV/sensor_data/leak"]
        else:
            leak = 0

        self._dash.update_images({
            "topview": gyro_yaw,
            "frontview": gyro_roll,
            "sideview": gyro_pitch
        })

        # Convert the triggers to a single value.
        right_trigger = controller.axes[enums.ControllerAxisNames.RIGHT_TRIGGER]
        left_trigger = controller.axes[enums.ControllerAxisNames.LEFT_TRIGGER]
        vertical = controller_input.combine_triggers(left_trigger.value, right_trigger.value)

        self._kinematics.update_target_position(
            Vector3(
                controller.axes[enums.ControllerAxisNames.RIGHT_X].value,
                controller.axes[enums.ControllerAxisNames.RIGHT_Y].value,
                0,
            ),
            vertical,
        )

        # TODO: add sensor data to pids below
        # Get the PWM values for the thrusters based on the controller inputs.
        pwm_values: dict[enums.ThrusterPositions, int] = self._frame.get_pwm_values(
            {
                enums.Directions.FORWARDS: controller.axes[enums.ControllerAxisNames.LEFT_Y].value,
                enums.Directions.RIGHT: controller.axes[enums.ControllerAxisNames.LEFT_X].value,
                enums.Directions.UP: self._kinematics.depth_pid(depth),
                enums.Directions.YAW: self._kinematics.yaw_pid(gyro_yaw),
                enums.Directions.PITCH: self._kinematics.pitch_pid(gyro_pitch),
                enums.Directions.ROLL: self._kinematics.roll_pid(gyro_roll),
            },
        )

        # Test to see if button press toggles are working.
        stop = controller.buttons[enums.ControllerButtonNames.B].toggled

        if controller.buttons[enums.ControllerButtonNames.Y].value:
            self._imu.calibrate_gyro()

        # Publish the PWM values to the MQTT broker.
        for thruster, pwm in pwm_values.items():
            self._io.gpio_handler.pins[thruster].val = 1500

        self._io.rov_comms.publish_commands({
            "stop": stop,
        })

    def shutdown(self):
        """Shutdown the ROV."""
        # TODO: Add any shutdown logic here.
        pass
