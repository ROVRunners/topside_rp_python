"""
"""

import hardware.thruster_pwm as thruster_pwm
import enums
import kinematics as kms
import controller_input
from topside.io_handler import IO
from utilities.vector import Vector3


class Manual:
    """The manual control class for the ROV.
    takes an inputs and maps and sends outputs to the rov connection
    """

    def __init__(self, frame: thruster_pwm.FrameThrusters, io: IO, kinematics: kms.Kinematics) -> None:
        """Initialize the Manual object.

        Args:
            frame (thruster_pwm.FrameThrusters):
                The objects of the thrusters mounted to the frame.
            io (IO):
                The IO (input output) object.
            kinematics (kinematics.Kinematics):
                The Kinematics object housing the PIDs.
        """
        self._frame = frame
        self._io = io
        self._kinematics = kinematics

        # Set up the objects
        # self._rov_connection: mqtt_handler.ROVConnection = self._main_system.rov_connection
        # self._input_handler: controller_input.InputHandler = self._main_system.input_handler

        # self.sensor_data = {}
        # self.terminal_data = {}

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
        print(controller.axes[enums.ControllerAxisNames.LEFT_X].value)

        print(controller.axes[enums.ControllerAxisNames.RIGHT_X].value)

        subscriptions = self._io.subscriptions

        # Get the gyro data from the subscriptions if it exists.
        if "ROV/sensor_data/gyro" in subscriptions:
            gyro_yaw = subscriptions["ROV/sensor_data/gyro/yaw"]
            gyro_pitch = subscriptions["ROV/sensor_data/gyro/pitch"]
            gyro_roll = subscriptions["ROV/sensor_data/gyro/roll"]
        else:
            gyro_yaw = 0
            gyro_pitch = 0
            gyro_roll = 0

        # Get the accelerometer data from the subscriptions if it exists.
        if "ROV/sensor_data/accel" in subscriptions:
            accel_x = subscriptions["ROV/sensor_data/accel/x"]
            accel_y = subscriptions["ROV/sensor_data/accel/y"]
            accel_z = subscriptions["ROV/sensor_data/accel/z"]
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

        # Convert the triggers to a single value.
        right_trigger = controller.axes[enums.ControllerAxisNames.RIGHT_TRIGGER]
        left_trigger = controller.axes[enums.ControllerAxisNames.LEFT_TRIGGER]
        vertical = controller_input.combine_triggers(left_trigger.value, right_trigger.value)

        # TODO: Add any other input processing software like a PID here. Also, a PID should probably be
        #  implemented in a separate class due to it being generally applicable to all ROVs.
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
