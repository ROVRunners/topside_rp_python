import tkinter as tk

from hardware.thruster_pwm import ThrusterPWM, FrameThrusters
from io_systems.io_handler import IO

import rov_config
from dashboard import Dashboard
from enums import ThrusterPositions, ControlModes
from kinematics import Kinematics
from imu import IMU

from control_modes import *

from rovs.generic_objects.generic_rov import GenericROV


class ROV(GenericROV):

    def __init__(self, config: rov_config.ROVConfig, io: IO) -> None:
        """Create and initialize the ROV hardware.

        Args:
            config (rov_config.ROVConfig):
                ROV hardware configuration.
            io (IO):
                The IO object.
        """
        super().__init__(config, io)

        # ROV hardware.
        self._thrusters: dict[ThrusterPositions, ThrusterPWM] = {}
        self._kinematics: Kinematics = Kinematics(self._config.kinematics_config)
        self._imu: IMU = IMU(self._config.imu_config)

        # Tkinter GUI.
        self.root: tk.Tk = tk.Tk()
        self.root.wm_title("ROV monitor")
        self._dash: Dashboard = Dashboard(self.root, self._config.dash_config)

        # Mavlink connection.
        self._mavlink_interval_ns: int = int(1_000_000_000 / 100)  # 100 Hz

        self._io.rov_comms.publish_mavlink_data_request(
            {val: self._mavlink_interval_ns for val in self._config.mavlink_subscriptions.values()}
        )

        # Configure thrusters.
        for position, thruster_config in self._config.thruster_configs.items():
            self._thrusters[position] = ThrusterPWM(thruster_config)

        self._frame = FrameThrusters(self._thrusters)

        # Set up control modes.
        self._control_mode_dict = {
            ControlModes.MANUAL: Manual(
                self._frame, self._io, self._kinematics, self.set_control_mode, self._dash
            ),
        }

        self._control_mode = self._control_mode_dict[ControlModes.MANUAL]

    def set_control_mode(self, control_mode: ControlModes) -> None:
        """Set the current control mode of the ROV.

        Args:
            control_mode (ControlModes):
                The control mode to set.
        """
        self._control_mode = self._control_mode_dict[control_mode]

    def run(self) -> None:
        """Update the io system and loop the control mode."""
        self._io.update()
        self._control_mode.loop()
        self.root.update()

    def shutdown(self) -> None:
        """Shutdown the ROV hardware."""
        # TODO: Implement this method further.
        self._control_mode.shutdown()
        print("ROV shutdown complete.")
