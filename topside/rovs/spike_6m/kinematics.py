import math

import simple_pid

from config.kinematics import KinematicsConfig
from rov_config import ROVConfig

from utilities.vector import Vector3


class Kinematics:
    """
    The kinematics class for the ROV. holds the depth, and orientation PIDs.
    Determines the current orientation and depth from sensor inputs.
    """

    depth_pid: simple_pid.PID

    pitch_pid: simple_pid.PID
    roll_pid: simple_pid.PID
    yaw_pid: simple_pid.PID

    def __init__(self, config: KinematicsConfig) -> None:
        """Set up the various PIDs involved in moving the ROV smoothly.

        Args:
            config (KinematicsConfig):
                The PID configuration of the ROV.
        """
        self._config = config

        # Depth position PID.
        self.depth_pid = simple_pid.PID(self._config.depth_pid.p, self._config.depth_pid.i, self._config.depth_pid.d)
        # , output_limits=self._config.depth_pid.output)

        # Orientation PIDs.
        self.pitch_pid = simple_pid.PID(self._config.pitch_pid.p, self._config.pitch_pid.i, self._config.pitch_pid.d,
                                        output_limits=self._config.pitch_pid.output)
        self.roll_pid = simple_pid.PID(self._config.roll_pid.p, self._config.roll_pid.i, self._config.roll_pid.d,
                                       output_limits=self._config.roll_pid.output)
        self.yaw_pid = simple_pid.PID(self._config.yaw_pid.p, self._config.yaw_pid.i, self._config.yaw_pid.d,
                                      output_limits=self._config.yaw_pid.output)

        self.target_heading = Vector3(yaw=0, pitch=0, roll=0)
        self.target_depth = 0

        # self.current_heading = radians (pitch, roll, yaw)
        # self.current_depth = 0 # meters
        #

        # self.target_heading = (0, 0, 0) # radians (pitch, roll, yaw)
        # self.target_depth = 0 # meters

    # def update_position(self, heading: tuple[float, float, float], depth: float):
    #     self.current_heading = heading
    #     self.current_depth = depth
    #
    #     self.pitch_pid(self.current_heading[0])
    #     self.roll_pid(self.current_heading[1])
    #     self.yaw_pid(self.current_heading[2])

    #     self.depth_pid(depth)

    def update_target_position(self, heading: Vector3, depth: float) -> None:
        """Update the target position of the ROV.

        Args:
            heading (Vector3):
                The target heading of the ROV.
            depth (float):
                The target depth of the ROV.
        """
        self.target_heading = heading
        self.target_depth = depth

        self.pitch_pid.setpoint = self.target_heading.pitch
        self.roll_pid.setpoint = self.target_heading.roll
        self.yaw_pid.setpoint = self.target_heading.yaw

        self.depth_pid.setpoint = self.target_depth

    def get_pid_values(self) -> dict[str, dict[str, float]]:
        pass

    def calculate_direction_mixing(self, current_heading: Vector3, target_lateral: Vector3) -> Vector3:
        """Calculate the direction mixing for the ROV.

        Args:
            current_heading (Vector3):
                The current heading of the ROV.
            target_lateral (Vector3):
                The target lateral movement of the ROV.

        Returns:
            Vector3:
                The lateral values to move the ROV in plus the  modulated by the current heading.
        """
        up = self.depth_pid.

        # TODO: Verify that this actually makes sense.
        up_dir: Vector3 = Vector3(
            x=math.sin(current_heading.pitch),  # ROV Forward
            y=math.sin(current_heading.roll),  # ROV Right
            z=math.cos(current_heading.pitch)*math.cos(current_heading.roll),  # ROV Up
        )

        return Vector3(
            x=up_dir.x + target_lateral.x,
            y=up_dir.y + target_lateral.y,
            z=up_dir.z + target_lateral.z,
        )
