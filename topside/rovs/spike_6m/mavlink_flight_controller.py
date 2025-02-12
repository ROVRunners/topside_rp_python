from config.flight_controller import FlightControllerConfig
from io_systems.mavlink_handler import MavlinkHandler
from enums import MavlinkMessageTypes
from utilities.vector import Vector3


class FlightController():

    def __init__(self, FlightControllerConfig):

        self._flight_controller_config = FlightControllerConfig

        self._attitude = Vector3(yaw=0, pitch=0, roll=0)  # radians
        self._attitude_speed = Vector3(yaw=0, pitch=0, roll=0)  # rad/s

        self._lateral_accel = Vector3(x=0, y=0, z=0)  # mG

        self._compass = Vector3(x=0, y=0, z=0)  # mgauss

        self._currently_calibrating = False

    def initialize_flight_controller(self, mavlink: MavlinkHandler.mavlink_commands):
        mavlink.mavlink_commands = self._flight_controller_config.initial_commands

    def update(self, messages: dict[str, dict]):
        self._attitude = messages["ATTITUDE"]["yaw"], messages["ATTITUDE"]["pitch"], messages["ATTITUDE"]["roll"]
        self._attitude_speed = messages["ATTITUDE"]["yawspeed"], messages["ATTITUDE"]["pitchspeed"], messages["ATTITUDE"]["rollspeed"]

        self._lateral_accel = messages["SCALED_IMU"]["xacc"], messages["SCALED_IMU"]["yacc"], messages["SCALED_IMU"]["zacc"]
        self._compass = messages["SCALED_IMU"]["xmag"], messages["SCALED_IMU"]["ymag"],messages["SCALED_IMU"]["zmag"]

    def calibrate_gyro(self, mavlink: MavlinkHandler.mavlink_commands):
        if not self._currently_calibrating:
            mavlink.mavlink_commands[MavlinkMessageTypes.MAV_CMD_PREFLIGHT_CALIBRATION] = (1,0,0,0,0,0,0)

    def calibrate_accelerometer(self, mavlink: MavlinkHandler.mavlink_commands):
        if not self._currently_calibrating:
            mavlink.mavlink_commands[MavlinkMessageTypes.MAV_CMD_PREFLIGHT_CALIBRATION] = (0,0,0,0,1,0,0)

    def calibrate_compass(self, mavlink: MavlinkHandler.mavlink_commands):
        if not self._currently_calibrating:
            mavlink.mavlink_commands[MavlinkMessageTypes.MAV_CMD_PREFLIGHT_CALIBRATION] = (0,1,0,0,0,0,0)

