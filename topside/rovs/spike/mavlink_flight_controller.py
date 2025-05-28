from config.flight_controller import FlightControllerConfig
from io_systems.mavlink_handler import MavlinkHandler
from enums import MavlinkMessageTypes
from wpimath.geometry import Quaternion

from utilities.vector import Vector3
from utilities.math_help.shared import wrap_angle


class FlightController:

    def __init__(self, flight_controller_config: FlightControllerConfig) -> None:
        """Initialize the FlightController object.

        Args:
            flight_controller_config (FlightControllerConfig):
                The configuration for the flight controller.
        """

        self._flight_controller_config = flight_controller_config


        self._attitude_quat = Quaternion(0, 0, 0, 0)
        self._attitude = Vector3(yaw=0, pitch=0, roll=0)  # radians
        self._attitude_speed = Vector3(yaw=0, pitch=0, roll=0)  # rad/s
        self._lateral_accel = Vector3(x=0, y=0, z=0)  # mG
        self._compass = Vector3(x=0, y=0, z=0)  # mGauss

        self._currently_calibrating = False


    #TODO: fix this so it is irrespective of the order that the quaternion is in
    @property
    def attitude(self) -> Vector3:
        attitude = []
        quat = self._attitude_quat.normalize().toRotationVector()
        for q in quat:
            attitude.append(q)
        return Vector3(yaw=attitude[0], pitch=attitude[1], roll=attitude[2])

    @property
    def attitude_speed(self):
        return self._attitude_speed

    @property
    def attitude_quat(self) -> Quaternion:
        return self._attitude_quat

    @property
    def attitude_quat_speed(self):
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
            att = messages["ATTITUDE"]
            self._attitude = Vector3(
                yaw=wrap_angle(att["yaw"]), pitch=wrap_angle(att["pitch"]),
                roll=wrap_angle(att["roll"])
            )
            self._attitude_speed = Vector3(
                yaw=att["yawspeed"], pitch=att["pitchspeed"], roll=att["rollspeed"]
            )

        if "ATTITUDE_QUATERNION" in messages:
            attq = messages["ATTITUDE_QUATERNION"]
            self._attitude_quat = Quaternion(
                w=attq["q1"], x=attq["q2"], y=attq["q3"], z=attq["q4"]
            )
            self._attitude_speed = Vector3(
                roll=attq["rollspeed"], yaw=attq["yawspeed"], pitch=attq["pitchspeed"]
            )

        if "SCALED_IMU" in messages:
            s_i = messages["SCALED_IMU"]
            self._lateral_accel = Vector3(
                s_i["xacc"], s_i["yacc"], s_i["zacc"]
            )
            self._compass = Vector3(
                s_i["xmag"], s_i["ymag"], s_i["zmag"]
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
