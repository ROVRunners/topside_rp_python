"""This file contains the configuration for the Spike ROV."""
import socket

import config.typed_range as typed_range
import enums
import controller as controller
import config.thruster as thruster
from config.pin import PinConfig
from pin import Pin
from i2c import I2C
from config.i2c import I2CConfig
from config.kinematics import KinematicsConfig
from config.pid import PIDConfig
from config.imu import IMUConfig


class ROVConfig:
    """Class for the ROV configuration."""

    def __init__(self) -> None:
        """Initialize an instance of the class."""

        # The ports used to communicate with the ROV. The comms port is for the MQTT broker, while the video port is
        # for the video stream(s).
        self.comms_port = 1883
        self.video_port = 5600

        # TODO: This is where you change the IP. It needs to be the local IP for remote stuff to connect.
        #  We need to make it so it sets itself automatically or can be set by the user.
        # Test auto-IP getter:
        hostname = socket.gethostname()
        ip_addr = socket.gethostbyname(hostname)

        self.host_ip = ip_addr
        # self.host_ip = "192.168.1.142"

        # Put specific settings for each axis/button here. I recommend using a second set of dictionaries for a second
        # controller, if you plan on using one.
        self.axes: dict[enums.ControllerAxisNames, controller.Axis] = {
            enums.ControllerAxisNames.LEFT_X: controller.Axis(index=0, deadzone=0.15),
            enums.ControllerAxisNames.LEFT_Y: controller.Axis(index=1, deadzone=0.15),
            enums.ControllerAxisNames.RIGHT_X: controller.Axis(index=2, deadzone=0.15),
            enums.ControllerAxisNames.RIGHT_Y: controller.Axis(index=3, deadzone=0.15),
            enums.ControllerAxisNames.LEFT_TRIGGER: controller.Axis(index=4),
            enums.ControllerAxisNames.RIGHT_TRIGGER: controller.Axis(index=5),
        }
        self.buttons: dict[enums.ControllerButtonNames, controller.Button] = {
            enums.ControllerButtonNames.A: controller.Button(index=0),
            enums.ControllerButtonNames.B: controller.Button(index=1),
            enums.ControllerButtonNames.X: controller.Button(index=2),
            enums.ControllerButtonNames.Y: controller.Button(index=3),
            enums.ControllerButtonNames.START: controller.Button(index=6),
            enums.ControllerButtonNames.SELECT: controller.Button(index=7),
            enums.ControllerButtonNames.LEFT_BUMPER: controller.Button(index=4),
            enums.ControllerButtonNames.RIGHT_BUMPER: controller.Button(index=5),
        }

        self.hats: dict[enums.ControllerHatNames, controller.Hat] = {
            enums.ControllerHatNames.DPAD: controller.Hat(index=0),
        }

        self.controllers: dict[enums.ControllerNames, controller.Controller] = {
            enums.ControllerNames.PRIMARY_DRIVER: controller.Controller(0, self.buttons, self.axes, self.hats),
        }

        # Definitions of the forces applied by the thrusters.
        self.thruster_impulses: dict[enums.ThrusterPositions, dict[enums.Directions, float]] = {
            enums.ThrusterPositions.FRONT_RIGHT: {
                enums.Directions.FORWARDS: 1,
                enums.Directions.RIGHT: -1,
                enums.Directions.UP: 0,
                enums.Directions.YAW: 1,
                enums.Directions.PITCH: 0,
                enums.Directions.ROLL: 0,
            },
            enums.ThrusterPositions.FRONT_LEFT: {
                enums.Directions.FORWARDS: 1,
                enums.Directions.RIGHT: 1,
                enums.Directions.UP: 0,
                enums.Directions.YAW: -1,
                enums.Directions.PITCH: 0,
                enums.Directions.ROLL: 0,
            },
            enums.ThrusterPositions.REAR_RIGHT: {
                enums.Directions.FORWARDS: -1,
                enums.Directions.RIGHT: -1,
                enums.Directions.UP: 0,
                enums.Directions.YAW: 1,
                enums.Directions.PITCH: 0,
                enums.Directions.ROLL: 0,
            },
            enums.ThrusterPositions.REAR_LEFT: {
                enums.Directions.FORWARDS: -1,
                enums.Directions.RIGHT: 1,
                enums.Directions.UP: 0,
                enums.Directions.YAW: -1,
                enums.Directions.PITCH: 0,
                enums.Directions.ROLL: 0,
            },
            enums.ThrusterPositions.FRONT_RIGHT_VERTICAL: {
                enums.Directions.FORWARDS: 0,
                enums.Directions.RIGHT: 0,
                enums.Directions.UP: 1,
                enums.Directions.YAW: 0,
                enums.Directions.PITCH: 1,
                enums.Directions.ROLL: -1,
            },
            enums.ThrusterPositions.FRONT_LEFT_VERTICAL: {
                enums.Directions.FORWARDS: 0,
                enums.Directions.RIGHT: 0,
                enums.Directions.UP: 1,
                enums.Directions.YAW: 0,
                enums.Directions.PITCH: 1,
                enums.Directions.ROLL: 1,
            },
            enums.ThrusterPositions.REAR_RIGHT_VERTICAL: {
                enums.Directions.FORWARDS: 0,
                enums.Directions.RIGHT: 0,
                enums.Directions.UP: 1,
                enums.Directions.YAW: 0,
                enums.Directions.PITCH: -1,
                enums.Directions.ROLL: -1,
            },
            enums.ThrusterPositions.REAR_LEFT_VERTICAL: {
                enums.Directions.FORWARDS: 0,
                enums.Directions.RIGHT: 0,
                enums.Directions.UP: 1,
                enums.Directions.YAW: 0,
                enums.Directions.PITCH: -1,
                enums.Directions.ROLL: 1,
            },
        }

        self.kinematics_config = KinematicsConfig(
            yaw_pid=PIDConfig(p= 0, i=0, d=0),
            pitch_pid=PIDConfig(p= 0, i=0, d=0),
            roll_pid=PIDConfig(p= 0, i=0, d=0),
            depth_pid=PIDConfig(p= 0, i=0, d=0),
        )

        self.thruster_configs: dict[enums.ThrusterPositions, thruster.ThrusterPWMConfig] = {

            position: thruster.ThrusterPWMConfig(
                pwm_pulse_range=typed_range.IntRange(min=1100, max=1900),
                thruster_impulses=self.thruster_impulses[position]
            ) for position in self.thruster_impulses.keys()
        }

        self.pins: dict[str, Pin] = {
            enums.ThrusterPositions.FRONT_RIGHT: Pin(PinConfig(id= 27, mode="PWMus", val=1500, freq=50)),
            enums.ThrusterPositions.FRONT_LEFT: Pin(PinConfig(id=5, mode="PWMus", val=1500, freq=50)),
            enums.ThrusterPositions.REAR_RIGHT: Pin(PinConfig(id=6, mode="PWMus", val=1500, freq=50)),
            enums.ThrusterPositions.REAR_LEFT: Pin(PinConfig(id=13, mode="PWMus", val=1500, freq=50)),
            enums.ThrusterPositions.FRONT_RIGHT_VERTICAL: Pin(PinConfig(id=19, mode="PWMus", val=1500, freq=50)),
            enums.ThrusterPositions.FRONT_LEFT_VERTICAL: Pin(PinConfig(id=26, mode="PWMus", val=1500, freq=50)), #pins for following motors are placeholders
            enums.ThrusterPositions.REAR_RIGHT_VERTICAL: Pin(PinConfig(id=23, mode="PWMus", val=1500, freq=50)),
            enums.ThrusterPositions.REAR_LEFT_VERTICAL: Pin(PinConfig(id=4, mode="PWMus", val=1500, freq=50)),

        }
        self.i2cs: dict[str, I2C] = {
            "imu": I2C(I2CConfig(addr=0x6A, reading_registers={"gyro": (0x22, 6), "accel": (0x28, 6)}),)
        }

        self.imu_config = IMUConfig(
            gyro_init_register = 0x10,
            accel_init_register = 0x11,
            gyro_init_value = 0x50,
            accel_init_value = 0x50,
            gyro_name = "gyro",
            accel_name = "accel"
        )


