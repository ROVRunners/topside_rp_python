import hardware.thruster_pwm as thruster_pwm
import rov_config
from dashboard import Dashboard
from io_systems.io_handler import IO
from kinematics import Kinematics
from imu import IMU
import tkinter as tk

import manual


class ROV:

    def __init__(self, config: rov_config.ROVConfig, io: IO) -> None:
        """Create and initialize the ROV hardware.

        Args:
            config (rov_config.ROVConfig):
                ROV hardware configuration.
            io (IO):
                The IO object.
        """
        self._config = config
        self._io = io
        self._thrusters = {}
        self._kinematics = Kinematics(self._config.kinematics_config)
        self._imu = IMU(self._config.imu_config)

        self.root = tk.Tk()
        self.root.wm_title("ROV monitor")
        self._dash = Dashboard(self.root, self._config.dash_config)

        # Mavlink connection (fully optional)
        self._mavlink_interval_ns = 10_000_000  # 100 Hz
        for msg_id in self._config.mavlink_subscriptions.values():
            self._io.add_mavlink_subscription(msg_id, self._mavlink_interval_ns)

        # Configure thrusters.
        for position, thruster_config in self._config.thruster_configs.items():
            self._thrusters[position] = thruster_pwm.ThrusterPWM(thruster_config)

        self._frame = thruster_pwm.FrameThrusters(self._thrusters)

        # Set the class handling control to manual as default.
        self._control_mode = manual.Manual(self._frame, self._io, self._kinematics, self._imu, self._dash)

    def run(self):
        self._io.update()
        self._control_mode.loop()
        self.root.update()

    def shutdown(self):
        """Shutdown the ROV hardware."""
        # TODO: Implement this method further.
        self._control_mode.shutdown()
        print("ROV shutdown complete.")
