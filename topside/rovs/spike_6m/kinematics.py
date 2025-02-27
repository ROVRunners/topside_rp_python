import math

import simple_pid

import enums
from config.kinematics import KinematicsConfig

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

    @classmethod
    def rotate_target_lateral_movement(cls, ch: Vector3, tl: Vector3) -> Vector3:
        """Calculate the combination of directions the thrusters need to push to move the ROV in the desired direction
        while taking into account the current heading of the ROV. Does not account for rotating the ROV.

        Args:
            ch (Vector3):
                The current heading of the ROV.
            tl (Vector3):
                The target lateral movement of the ROV.

        Returns:
            Vector3:
                The lateral values to move the ROV modulated by the current heading.
        """
        # TODO: Test this.
        translated_lateral = Vector3(
            x=(
                tl.x * math.cos(ch.roll)
                + tl.y * math.sin(ch.roll) * math.sin(ch.pitch)
                + tl.z * math.sin(ch.roll) * math.cos(ch.pitch)
            ),
            y=(
                tl.y * math.cos(ch.pitch)
                - tl.z * math.sin(ch.pitch)
            ),
            z=(
                -tl.x * math.sin(ch.roll)
                + tl.y * math.cos(ch.roll) * math.sin(ch.pitch)
                + tl.z * math.cos(ch.roll) * math.cos(ch.pitch)
            ),
        )

        # # up = self.depth_pid._last_output
        #
        # # TODON'T: Verify that this actually makes sense.
        # up_dir: Vector3 = Vector3(
        #     x=math.sin(current_heading.pitch),  # ROV Forward
        #     y=math.sin(current_heading.roll),  # ROV Right
        #     z=math.cos(current_heading.pitch)*math.cos(current_heading.roll),  # ROV Up
        # )
        #
        # return Vector3(
        #     x=up_dir.x + tl.x,
        #     y=up_dir.y + tl.y,
        #     z=up_dir.z + tl.z,
        # )

        return translated_lateral

    # TODO: Test and work on this to make it more efficient.
    def mix_directions(self, heading: Vector3, lateral_target: Vector3, rotational_target: Vector3,
                       pid_impulses: dict[str, float]) -> dict[str, float]:
        """Mix the thrusters to move the ROV in the desired direction.

        Args:
            heading (Vector3):
                The current heading of the ROV.
            lateral_target (Vector3):
                The target lateral movement of the ROV. Do not include anything PID-controlled.
            rotational_target (Vector3):
                The target rotational movement of the ROV. Do not include anything PID-controlled.
            pid_impulses (dict[str, float]):
                The PID-controlled values for the directions.

        Returns:
            dict[str, float]:
                The output values for the thrusters.
        """
        directional_values: dict[str, float] = {name: 0 for name in enums.Directions}

        lateral: Vector3 = self.rotate_target_lateral_movement(heading, lateral_target)

        directional_values[enums.Directions.FORWARDS] = lateral.x
        directional_values[enums.Directions.RIGHT] = lateral.y
        directional_values[enums.Directions.UP] = lateral.z

        directional_values[enums.Directions.YAW] = rotational_target.yaw
        directional_values[enums.Directions.PITCH] = rotational_target.pitch
        directional_values[enums.Directions.ROLL] = rotational_target.roll

        for direction, value in pid_impulses.items():
            directional_values[direction] += value

        normalized_dir_vals = {}

        thruster_norm = max(
            abs(directional_values[enums.Directions.FORWARDS]),
            abs(directional_values[enums.Directions.RIGHT]),
            abs(directional_values[enums.Directions.UP]),
            abs(directional_values[enums.Directions.YAW]),
            abs(directional_values[enums.Directions.PITCH]),
            abs(directional_values[enums.Directions.ROLL]),
        )

        if thruster_norm > 1:
            for direction, value in directional_values.items():
                normalized_dir_vals[direction] = value / thruster_norm
        else:
            normalized_dir_vals = directional_values

        return normalized_dir_vals
