import rov_config
import simple_pid

from config.kinematics import KinematicsConfig

from utilities.vector import Vector3
import numpy as np


class Kinematics:
    """
    The kinematics class for the ROV. holds the depth, orientation, and velocity PIDs.
    Set Target position + velocity and get the thruster pwms.
     Determines the current position + velocity from sensor inputs
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
        self.depth_pid = simple_pid.PID(self._config.depth_pid.p, self._config.depth_pid.i, self._config.depth_pid.d, output_limits=self._config.depth_pid.output)

        # Orientation PIDs.
        self.pitch_pid = simple_pid.PID(self._config.pitch_pid.p, self._config.pitch_pid.i, self._config.pitch_pid.d, output_limits=self._config.pitch_pid.output)
        self.roll_pid = simple_pid.PID(self._config.roll_pid.p, self._config.roll_pid.i, self._config.roll_pid.d, output_limits=self._config.roll_pid.output)
        self.yaw_pid = simple_pid.PID(self._config.yaw_pid.p, self._config.yaw_pid.i, self._config.yaw_pid.d, output_limits=self._config.yaw_pid.output)

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

    def update_target_position(self, heading: Vector3, depth: float):
        self.target_heading = heading
        self.target_depth = depth

        self.pitch_pid.setpoint = self.target_heading.pitch
        self.roll_pid.setpoint = self.target_heading.roll
        self.yaw_pid.setpoint = self.target_heading.yaw

        self.depth_pid.setpoint = self.target_depth

