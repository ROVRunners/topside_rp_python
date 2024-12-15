import rov_config
from config.kinematics import KinematicsConfig
import numpy as np
import simple_pid

class Kinematics:
    """
    The kinematics class for the ROV. holds the depth, orientation, and velocity PIDs.
    Set Target position + velocity and get the thruster pwms.
     Determines the current position + velocity from sensor inputs
    """
    def __init__(self, config: KinematicsConfig):
        self._config = config

        # planar velocity PIDs
        #TODO add actual pid classes
        self.x_vel_pid = simple_pid.PID(self._config.x_vel_pid.p, self._config.x_vel_pid.i, self._config.x_vel_pid.d)
        self.y_vel_pid = simple_pid.PID(self._config.y_vel_pid.p, self._config.y_vel_pid.i, self._config.y_vel_pid.d)

        self.depth_pid = simple_pid.PID(self._config.depth_pid.p, self._config.depth_pid.i, self._config.depth_pid.d)

        # orientation PIDs
        self.pitch_pid = simple_pid.PID(self._config.pitch_pid.p, self._config.pitch_pid.i, self._config.pitch_pid.d)
        self.roll_pid = simple_pid.PID(self._config.roll_pid.p, self._config.roll_pid.i, self._config.roll_pid.d)
        self.yaw_pid = simple_pid.PID(self._config.yaw_pid.p, self._config.yaw_pid.i, self._config.yaw_pid.d)


        self.current_velocity = (0, 0, 0) # m/s (x, y, z)
        self.current_heading = (0, 0, 0) # radians (pitch, roll, yaw)
        self.current_depth = 0 # meters

        self.target_velocity = (0, 0, 0) # m/s (x, y, z)
        self.target_heading = (0, 0, 0) # radians (pitch, roll, yaw)
        self.target_depth = 0 # meters

    def update_position(self, velocity: tuple[float, float, float], heading: tuple[float, float, float], depth: float):
        self.current_velocity = velocity
        self.current_heading = heading
        self.current_depth = depth

    def update_target_position(self, velocity: tuple[float, float, float], heading: tuple[float, float, float], depth: float):
        self.target_velocity = velocity
        self.target_heading = heading
        self.target_depth = depth

        self.x_vel_pid.setpoint = self.target_velocity[0]
        self.y_vel_pid.setpoint = self.target_velocity[1]

        self.pitch_pid.setpoint = self.target_heading[0]
        self.roll_pid.setpoint = self.target_heading[1]
        self.yaw_pid.setpoint = self.target_heading[2]

        self.depth_pid.setpoint = self.target_depth

