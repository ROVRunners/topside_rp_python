from config.pid import PIDConfig
from typing import NamedTuple

class KinematicsConfig(NamedTuple):
    """The config class for kinematics"""
    depth_pid: PIDConfig
    # orientation pids
    pitch_pid: PIDConfig
    roll_pid: PIDConfig
    yaw_pid: PIDConfig
