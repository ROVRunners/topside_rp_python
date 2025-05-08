from config.flight_controller import FlightControllerConfig
from io_systems.mavlink_handler import MavlinkHandler
from enums import MavlinkMessageTypes

from utilities.vector import Vector3


class FlightController:

    def __init__(self, flight_controller_config: FlightControllerConfig) -> None:
        """Initialize the FlightController object.

        Args:
            flight_controller_config (FlightControllerConfig):
                The configuration for the flight controller.
        """

        self._flight_controller_config = flight_controller_config

        self._attitude = Vector3(yaw=0, pitch=0, roll=0)  # radians
        self._attitude_speed = Vector3(yaw=0, pitch=0, roll=0)  # rad/s
        self._lateral_accel = Vector3(x=0, y=0, z=0)  # mG
        self._compass = Vector3(x=0, y=0, z=0)  # mGauss

        self._currently_calibrating = False

    @property
    def attitude(self):
        return self._attitude

    @property
    def attitude_speed(self):
        return self._attitude_speed

    @property
    def lateral_accel(self):
        return self._lateral_accel

    @property
    def compass(self):
        return self._compass

    @property
    def currently_calibrating(self):
        return self._currently_calibrating

    def initialize_flight_controller(self, mavlink: MavlinkHandler) -> None:
        mavlink.mavlink_commands = self._flight_controller_config.initial_commands

    def update(self, messages: dict[str, dict]) -> None:
        """Update the flight controller with the latest messages.

        Args:
            messages (dict[str, dict]):
                The messages from the mavlink handler.
        """
        if "ATTITUDE" in messages:
            self._attitude = Vector3(
                yaw=messages["ATTITUDE"]["yaw"], pitch=messages["ATTITUDE"]["pitch"], roll=messages["ATTITUDE"]["roll"]
            )
            self._attitude_speed = Vector3(
                yaw=messages["ATTITUDE"]["yawspeed"], pitch=messages["ATTITUDE"]["pitchspeed"], roll=messages["ATTITUDE"]["rollspeed"]
            )

        if "SCALED_IMU" in messages:
            self._lateral_accel = Vector3(
                messages["SCALED_IMU"]["xacc"], messages["SCALED_IMU"]["yacc"], messages["SCALED_IMU"]["zacc"]
            )
            self._compass = Vector3(
                messages["SCALED_IMU"]["xmag"], messages["SCALED_IMU"]["ymag"], messages["SCALED_IMU"]["zmag"]
            )


    def calibrate_gyro(self, mavlink: MavlinkHandler) -> None:
        """Calibrate the gyroscope.

        Args:
            mavlink (MavlinkHandler.mavlink_commands):
                The mavlink commands property.
        """
        if not self._currently_calibrating:
            mavlink.add_command(int(MavlinkMessageTypes.MAV_CMD_DO_SET_MODE.value), (0, 0, 0, 0, 0, 0, 0))
            # mavlink.mavlink_commands[MavlinkMessageTypes.MAV_CMD_PREFLIGHT_CALIBRATION] = (1, 0, 0, 0, 0, 0, 0)
            mavlink.add_command(int(MavlinkMessageTypes.MAV_CMD_PREFLIGHT_CALIBRATION.value), (1, 0, 0, 0, 0, 0, 0))

    def calibrate_accelerometer(self, mavlink: MavlinkHandler) -> None:
        """Calibrate the accelerometer.

        Args:
            mavlink (MavlinkHandler.mavlink_commands):
                The mavlink commands property.
        """
        if not self._currently_calibrating:
            # mavlink.mavlink_commands[int(MavlinkMessageTypes.MAV_CMD_PREFLIGHT_CALIBRATION.value)] = (0, 0, 0, 0, 1, 0, 0)
            mavlink.add_command(int(MavlinkMessageTypes.MAV_CMD_PREFLIGHT_CALIBRATION.value), (0, 0, 0, 0, 1, 0, 0))

    def calibrate_compass(self, mavlink: MavlinkHandler) -> None:
        """Calibrate the compass.

        Args:
            mavlink (MavlinkHandler.mavlink_commands):
                The mavlink commands property.
        """
        if not self._currently_calibrating:
            # mavlink.mavlink_commands[int(MavlinkMessageTypes.MAV_CMD_PREFLIGHT_CALIBRATION.value)] = (0, 1, 0, 0, 0, 0, 0)
            mavlink.add_command(int(MavlinkMessageTypes.MAV_CMD_PREFLIGHT_CALIBRATION.value), (0, 1, 0, 0, 0, 0, 0))
