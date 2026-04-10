"""This file contains the configuration for the Spike ROV."""
import os.path
import socket

import config.typed_range as typed_range
from rovs.cali.enums import ControllerNames, ControllerAxisNames, ControllerButtonNames, ControllerHatNames, ThrusterPositions#, MavlinkMessageTypes
from controller import Axis, Button, Hat, Controller
from hardware.pin import Pin
from hardware.i2c import I2C

from config.thruster import ThrusterConfig
from config.pin import PinConfig
# from config.i2c import I2CConfig
from config.kinematics import KinematicsConfig
from config.pid import PIDConfig
from config.imu import IMUConfig
from config.dashboard import DashboardConfig, ScaleConfig, LabelConfig, ImageConfig
from config.flight_controller import FlightControllerConfig

from utilities.range_util import Range
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

        ### CONTROLLERS ###

        # Put specific settings for each axis/button here. I recommend using a second set of dictionaries for a second
        # controller, if you plan on using one.
        self.axes: dict[ControllerAxisNames, Axis] = {
            ControllerAxisNames.LEFT_X:        Axis(index=0, deadzone=0.15),
            ControllerAxisNames.LEFT_Y:        Axis(index=1, deadzone=0.15),
            ControllerAxisNames.RIGHT_X:       Axis(index=2, deadzone=0.15),
            ControllerAxisNames.RIGHT_Y:       Axis(index=3, deadzone=0.15),
            ControllerAxisNames.LEFT_TRIGGER:  Axis(index=4, output_range=Range(0.0, 1.0)),
            ControllerAxisNames.RIGHT_TRIGGER: Axis(index=5, output_range=Range(0.0, 1.0)),
        }
        self.buttons: dict[ControllerButtonNames, Button] = {
            ControllerButtonNames.A:            Button(index=0),
            ControllerButtonNames.B:            Button(index=1),
            ControllerButtonNames.X:            Button(index=2),
            ControllerButtonNames.Y:            Button(index=3),
            ControllerButtonNames.START:        Button(index=6),
            ControllerButtonNames.SELECT:       Button(index=7),
            ControllerButtonNames.LEFT_BUMPER:  Button(index=4),
            ControllerButtonNames.RIGHT_BUMPER: Button(index=5),
        }

        self.hats: dict[ControllerHatNames, Hat] = {
            ControllerHatNames.DPAD: Hat(index=0),
        }

        self.controllers: dict[ControllerNames, Controller] = {
            ControllerNames.PRIMARY_DRIVER: Controller(0, self.buttons, self.axes, self.hats),
        }

        ### THRUSTERS ###
        # (Measured in cm)
        self.thruster_positions: dict[ThrusterPositions, Vector3] = {
            ThrusterPositions.FRONT_LEFT:     Vector3(-21,  25.5,   0),
            ThrusterPositions.FRONT_RIGHT:    Vector3( 21,  25.5,   0),
            ThrusterPositions.REAR_LEFT:      Vector3(-21, -25.5,   0),
            ThrusterPositions.REAR_RIGHT:     Vector3( 21, -25.5,   0),
            ThrusterPositions.FRONT_VERTICAL: Vector3(  0,  24.75, 11),
            ThrusterPositions.REAR_VERTICAL:  Vector3(  0, -24.75, 11),
        }

        #is this the thrust vector or the motor casing? [Motor casing. Black cone with wire is front]
        self.thruster_orientations: dict[ThrusterPositions, Vector3] = {
            ThrusterPositions.FRONT_LEFT: Vector3(
                # Left rotation is positive in all of the following cases.
                yaw= -30,   # Set by viewing the ROV from the top, looking down. 0 degrees is the front of the ROV.
                pitch=90,   # Set by viewing the ROV from its left side. 0 degrees is vertical up.
                roll=-90,   # Set by viewing the ROV from its rear. 0 degrees is vertical up.
            ),
            ThrusterPositions.FRONT_RIGHT:    Vector3(yaw=  30, pitch= 90, roll=  90),
            ThrusterPositions.REAR_LEFT:      Vector3(yaw=-150, pitch=-90, roll=  90),
            ThrusterPositions.REAR_RIGHT:     Vector3(yaw= 150, pitch=-90, roll= -90),
            ThrusterPositions.FRONT_VERTICAL: Vector3(yaw=   0, pitch=  0, roll= 180),
            ThrusterPositions.REAR_VERTICAL:  Vector3(yaw=   0, pitch=  0, roll=-180),
        }

        # # TODO: Insert the correct thruster impulses here when the ROV is re-assembled.
        # # Used to set the thrust of each thruster in the case that some thrusters are more powerful than others.
        # self.thruster_thrusts: dict[ThrusterPositions, float] = {
        #     ThrusterPositions.FRONT_LEFT: 1,
        #     ThrusterPositions.FRONT_RIGHT: 1,
        #     ThrusterPositions.REAR_LEFT: 1,
        #     ThrusterPositions.REAR_RIGHT: -1,
        #     ThrusterPositions.FRONT_LEFT_VERTICAL: 1,
        #     ThrusterPositions.FRONT_RIGHT_VERTICAL: 1,
        #     ThrusterPositions.REAR_LEFT_VERTICAL: 1,
        #     ThrusterPositions.REAR_RIGHT_VERTICAL: -1,
        # }

        # TODO: Insert the correct thruster impulses here when the ROV is re-assembled.
        # Used to set the thrust of each thruster in the case that some thrusters are more powerful than others.
        self.thruster_thrusts: dict[ThrusterPositions, float] = {
            ThrusterPositions.FRONT_LEFT:     1.0,
            ThrusterPositions.FRONT_RIGHT:    1.0,
            ThrusterPositions.REAR_LEFT:      1.0,
            ThrusterPositions.REAR_RIGHT:     1.0,
            ThrusterPositions.FRONT_VERTICAL: 1.0,
            ThrusterPositions.REAR_VERTICAL:  1.0,
        }

        self.reversed_thrust: dict[ThrusterPositions, bool] = {
            ThrusterPositions.FRONT_LEFT:     False,
            ThrusterPositions.FRONT_RIGHT:    False,
            ThrusterPositions.REAR_LEFT:      False,
            ThrusterPositions.REAR_RIGHT:     False,
            ThrusterPositions.FRONT_VERTICAL: False,
            ThrusterPositions.REAR_VERTICAL:  False,
        }

        self.thruster_configs: dict[ThrusterPositions, ThrusterConfig] = {

            position: ThrusterConfig(
                name                 = position,
                pwm_pulse_range      = typed_range.IntRange(min=1100, max=1900),
                thruster_position    = self.thruster_positions[position],
                thruster_orientation = self.thruster_orientations[position],
                thrust               = self.thruster_thrusts[position],
                reversed_thrust      = self.reversed_thrust[position],
            ) for position in self.thruster_positions.keys()
        }

        ### PIDs ###

        self.kinematics_config = KinematicsConfig(
            yaw_pid   = PIDConfig(p=0.5, i=0, d=0),
            pitch_pid = PIDConfig(p=0.5, i=0, d=0),
            roll_pid  = PIDConfig(p=0.5, i=0, d=0),
            depth_pid = PIDConfig(p=0.5, i=0, d=0),
        )

        self.pid_value_file = f"{self.rov_dir}/assets/pid_values.json"

        ### PI I/O ###

        self.pins: dict[str, Pin] = {
            ThrusterPositions.FRONT_LEFT:     Pin(PinConfig(id=21, mode="PWMus", val=1500, freq=50)),
            ThrusterPositions.FRONT_RIGHT:    Pin(PinConfig(id=20, mode="PWMus", val=1500, freq=50)),
            ThrusterPositions.REAR_LEFT:      Pin(PinConfig(id=26, mode="PWMus", val=1500, freq=50)),
            ThrusterPositions.REAR_RIGHT:     Pin(PinConfig(id=16, mode="PWMus", val=1500, freq=50)),
            ThrusterPositions.FRONT_VERTICAL: Pin(PinConfig(id=19, mode="PWMus", val=1500, freq=50)),
            ThrusterPositions.REAR_VERTICAL:  Pin(PinConfig(id=13, mode="PWMus", val=1500, freq=50)),

        }

        self.i2cs: dict[str, I2C] = {
            # "imu": I2C(I2CConfig(addr=0x6A, reading_registers={"gyro": (0x28, 6), "accel": (0x22, 6)}),),
        }

        self.imu_config = IMUConfig(
            gyro_init_register      = 0x11,
            accel_init_register     = 0x10,
            gyro_init_value         = 0x40,
            accel_init_value        = 0x40,
            gyro_name               = "gyro",
            accel_name              = "accel",
            gyro_conversion_factor  = 1.0,
            accel_conversion_factor = 1.0,
        )

        self.mavlink_interval = 10_000  # 10ms

        self.mavlink_subscriptions: dict[str, int] = {
            "heartbeat":             0,
            "sys_status":            1,
            "scaled_imu":           26,
            "attitude":             30,
            "attitude_quarternion": 31,
            "local_position_ned":   32,
        }

        # initial_commands = [
        #     (MavlinkMessageTypes.MAV_CMD_PREFLIGHT_CALIBRATION: (1, 0, 0, 0, 0, 0, 0)),
        #     (MavlinkMessageTypes.MAV_CMD_PREFLIGHT_CALIBRATION: (0, 0, 0, 0, 0, 0, 0)),
        # ]

        self.flight_controller_config: FlightControllerConfig = FlightControllerConfig(initial_commands={})

        ### DASHBOARD ###

        self.dash_config = DashboardConfig(
            labels=(
                LabelConfig("Height",  2, 2, "Height" ),
                LabelConfig("FPS",     3, 2, "FPS"    ),
                LabelConfig("Quality", 4, 2, "Quality"),
                # LabelConfig("Depth", 5, 1, "Depth: "),
            ),
            scales=(
                ScaleConfig("Height",  2, 3, 50, 300, 150, cspan=2),
                ScaleConfig("FPS",     3, 3,  1,  30,  15, cspan=2),
                ScaleConfig("Quality", 4, 3,  1, 100,  75, cspan=2),
            ),
            images=(
                ImageConfig("topview",   1, 2, 125, 125, f"{self.rov_dir}/assets/topview.png",   cspan=2),
                ImageConfig("sideview",  1, 4, 125, 125, f"{self.rov_dir}/assets/sideview.png",  cspan=2),
                ImageConfig("frontview", 1, 6, 125, 125, f"{self.rov_dir}/assets/frontview.png", cspan=2),
            )
        )
