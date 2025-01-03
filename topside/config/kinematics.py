from config.pid import PIDConfig
from typing import NamedTuple

class KinematicsConfig(NamedTuple):
    """The config class for kinematics"""
    # planar velocity PIDs
    x_vel_pid: PIDConfig
    y_vel_pid: PIDConfig

    depth_pid: PIDConfig

    # orientation pids
    pitch_pid: PIDConfig
    roll_pid: PIDConfig
    yaw_pid: PIDConfig
