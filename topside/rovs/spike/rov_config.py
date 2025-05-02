"""This file contains the configuration for the Spike ROV."""
import os.path
import socket

import config.typed_range as typed_range
import enums
import controller
from hardware.pin import Pin
from hardware.i2c import I2C

import config.thruster as thruster
from config.pin import PinConfig
# from config.i2c import I2CConfig
from config.kinematics import KinematicsConfig
from config.pid import PIDConfig
from config.imu import IMUConfig
from config.dashboard import *
from config.flight_controller import FlightControllerConfig

from utilities.vector import Vector3


class ROVConfig:
    """Class for the ROV configuration."""

    def __init__(self) -> None:
        """Initialize an instance of the class."""

        # The ports used to communicate with the ROV. The comms port is for the MQTT broker, while the video port is
        # for the video stream(s).
        self.comms_port = 1883
        self.video_port = 5600

        self.rov_dir = os.path.dirname(os.path.realpath(__file__))

        # TODO: This is where you change the IP. It needs to be the local IP for remote stuff to connect.
        #  We need to make it so it sets itself automatically or can be set by the user, but if it breaks,
        #  here is where you can manually set it.
        # Test auto-IP getter:
        hostname = socket.gethostname()
        ip_addr = socket.gethostbyname(hostname)

        self.host_ip = ip_addr
        # self.host_ip = "192.168.2.3"

        ### CONTROLLERS ###

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

        ### THRUSTERS ###

        self.thruster_positions: dict[enums.ThrusterPositions, Vector3] = {
            enums.ThrusterPositions.FRONT_LEFT: Vector3(-1, 1, 0),
            enums.ThrusterPositions.FRONT_RIGHT: Vector3(1, 1, 0),
            enums.ThrusterPositions.REAR_LEFT: Vector3(-1, -1, 0),
            enums.ThrusterPositions.REAR_RIGHT: Vector3(1, -1, 0),
            enums.ThrusterPositions.FRONT_LEFT_VERTICAL: Vector3(-1, 1, 0),
            enums.ThrusterPositions.FRONT_RIGHT_VERTICAL: Vector3(1, 1, 0),
            enums.ThrusterPositions.REAR_LEFT_VERTICAL: Vector3(-1, -1, 0),
            enums.ThrusterPositions.REAR_RIGHT_VERTICAL: Vector3(1, -1, 0),
        }

        self.thruster_orientations: dict[enums.ThrusterPositions, Vector3] = {
            enums.ThrusterPositions.FRONT_LEFT: Vector3(
                # Left rotation is positive in all of the following cases.
                yaw=-45,  # Set by viewing the ROV from the top, looking down. 0 degrees is the front of the ROV.
                pitch=0,  # Set by viewing the ROV from its left side. 0 degrees is vertical up.
                roll=90  # Set by viewing the ROV from its rear. 0 degrees is vertical up.
            ),
            enums.ThrusterPositions.FRONT_RIGHT: Vector3(yaw=45, pitch=0, roll=-90),
            enums.ThrusterPositions.REAR_LEFT: Vector3(yaw=-135, pitch=0, roll=90),
            enums.ThrusterPositions.REAR_RIGHT: Vector3(yaw=135, pitch=0, roll=-90),
            enums.ThrusterPositions.FRONT_LEFT_VERTICAL: Vector3(yaw=45, pitch=90, roll=0),
            enums.ThrusterPositions.FRONT_RIGHT_VERTICAL: Vector3(yaw=-45, pitch=90, roll=0),
            enums.ThrusterPositions.REAR_LEFT_VERTICAL: Vector3(yaw=135, pitch=90, roll=0),
            enums.ThrusterPositions.REAR_RIGHT_VERTICAL: Vector3(yaw=-135, pitch=90, roll=0),
        }

        # # TODO: Insert the correct thruster impulses here when the ROV is re-assembled.
        # # Used to set the thrust of each thruster in the case that some thrusters are more powerful than others.
        # self.thruster_thrusts: dict[enums.ThrusterPositions, float] = {
        #     enums.ThrusterPositions.FRONT_LEFT: 1,
        #     enums.ThrusterPositions.FRONT_RIGHT: 1,
        #     enums.ThrusterPositions.REAR_LEFT: 1,
        #     enums.ThrusterPositions.REAR_RIGHT: -1,
        #     enums.ThrusterPositions.FRONT_LEFT_VERTICAL: 1,
        #     enums.ThrusterPositions.FRONT_RIGHT_VERTICAL: 1,
        #     enums.ThrusterPositions.REAR_LEFT_VERTICAL: 1,
        #     enums.ThrusterPositions.REAR_RIGHT_VERTICAL: -1,
        # }

        # TODO: Insert the correct thruster impulses here when the ROV is re-assembled.
        # Used to set the thrust of each thruster in the case that some thrusters are more powerful than others.
        self.thruster_thrusts: dict[enums.ThrusterPositions, float] = {
            enums.ThrusterPositions.FRONT_LEFT: -1,
            enums.ThrusterPositions.FRONT_RIGHT: 1,
            enums.ThrusterPositions.REAR_LEFT: 1,
            enums.ThrusterPositions.REAR_RIGHT: 1,
            enums.ThrusterPositions.FRONT_LEFT_VERTICAL: 1,
            enums.ThrusterPositions.FRONT_RIGHT_VERTICAL: 1,
            enums.ThrusterPositions.REAR_LEFT_VERTICAL: 1,
            enums.ThrusterPositions.REAR_RIGHT_VERTICAL: -1,
        }

        self.thruster_configs: dict[enums.ThrusterPositions, thruster.ThrusterConfig] = {

            position: thruster.ThrusterConfig(
                name=position,
                pwm_pulse_range=typed_range.IntRange(min=1100, max=1900),
                thruster_position=self.thruster_positions[position],
                thruster_orientation=self.thruster_orientations[position],
                thrust=self.thruster_thrusts[position],
            ) for position in self.thruster_positions.keys()
        }

        ### PIDs ###

        self.kinematics_config = KinematicsConfig(
            yaw_pid=PIDConfig(p=0.5, i=0, d=0),
            pitch_pid=PIDConfig(p=0.5, i=0, d=0),
            roll_pid=PIDConfig(p=0.5, i=0, d=0),
            depth_pid=PIDConfig(p=0.5, i=0, d=0),
        )

        self.pid_value_file = f"{self.rov_dir}/assets/pid_values.json"

        ### PI I/O ###

        self.pins: dict[str, Pin] = {
            enums.ThrusterPositions.FRONT_LEFT: Pin(PinConfig(id=17, mode="PWMus", val=1500, freq=50)),
            enums.ThrusterPositions.FRONT_RIGHT: Pin(PinConfig(id=22, mode="PWMus", val=1500, freq=50)),
            enums.ThrusterPositions.REAR_LEFT: Pin(PinConfig(id=5, mode="PWMus", val=1500, freq=50)),
            enums.ThrusterPositions.REAR_RIGHT: Pin(PinConfig(id=6, mode="PWMus", val=1500, freq=50)),
            enums.ThrusterPositions.FRONT_LEFT_VERTICAL: Pin(PinConfig(id=26, mode="PWMus", val=1500, freq=50)),
            enums.ThrusterPositions.FRONT_RIGHT_VERTICAL: Pin(PinConfig(id=19, mode="PWMus", val=1500, freq=50)),
            enums.ThrusterPositions.REAR_LEFT_VERTICAL: Pin(PinConfig(id=27, mode="PWMus", val=1500, freq=50)),
            enums.ThrusterPositions.REAR_RIGHT_VERTICAL: Pin(PinConfig(id=13, mode="PWMus", val=1500, freq=50)),

        }

        self.i2cs: dict[str, I2C] = {
            # "imu": I2C(I2CConfig(addr=0x6A, reading_registers={"gyro": (0x28, 6), "accel": (0x22, 6)}),)
        }

        self.imu_config = IMUConfig(
            gyro_init_register=0x11,
            accel_init_register=0x10,
            gyro_init_value=0x40,
            accel_init_value=0x40,
            gyro_name="gyro",
            accel_name="accel",
            gyro_conversion_factor=1.0,
            accel_conversion_factor=1.0
        )

        self.mavlink_interval = 10_000  # 10ms

        self.mavlink_subscriptions: dict[str, int] = {
            "heartbeat": 0,
            "sys_status": 1,
            "scaled_imu": 26,
            "attitude": 30,
            "local_position_ned": 32,
        }

        # initial_commands = [
        #     (enums.MavlinkMessageTypes.MAV_CMD_PREFLIGHT_CALIBRATION: (1, 0, 0, 0, 0, 0, 0)),
        #     (enums.MavlinkMessageTypes.MAV_CMD_PREFLIGHT_CALIBRATION: (0, 0, 0, 0, 0, 0, 0)),
        # ]

        self.flight_controller_config: FlightControllerConfig = FlightControllerConfig(initial_commands={})

        ### DASHBOARD ###

        self.dash_config = DashboardConfig(
            labels=(
                LabelConfig("Height", 2, 2, "Height"),
                LabelConfig("FPS", 3, 2, "FPS"),
                LabelConfig("Quality", 4, 2, "Quality"),
                # LabelConfig("Depth", 5, 1, "Depth: "),
            ),
            scales=(
                ScaleConfig("Height", 2, 3, 50, 300, 150, cspan=2),
                ScaleConfig("FPS", 3, 3, 1, 30, 15, cspan=2),
                ScaleConfig("Quality", 4, 3, 1, 100, 75, cspan=2)
            ),
            images=(
                ImageConfig("topview", 1, 2, 125, 125, f"{self.rov_dir}/assets/topview.png", cspan=2),
                ImageConfig("sideview", 1, 4, 125, 125, f"{self.rov_dir}/assets/sideview.png", cspan=2),
                ImageConfig("frontview", 1, 6, 125, 125, f"{self.rov_dir}/assets/frontview.png", cspan=2)
            )
        )
