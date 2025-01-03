from typing import Callable

import hardware.thruster_pwm as thruster_pwm
import rov_config
from surface_main import IO
from kinematics import Kinematics

import manual


class ROV:

    def __init__(self, rov_config: rov_config.ROVConfig, io: IO) -> None:
        """Create and initialize the ROV hardware.

        Args:
            rov_config (rov_config.ROVConfig):
                ROV hardware configuration.
            io (IO):
                The IO object.
        """
        self._config = rov_config
        self._io = io
        self._thrusters = {}
        self._kinematics = Kinematics(self._config.kinematics_config)

        # Configure thrusters.
        for position, thruster_config in self._config.thruster_configs.items():
            self._thrusters[position] = thruster_pwm.ThrusterPWM(thruster_config)

        self._frame = thruster_pwm.FrameThrusters(self._thrusters)

        # Set the class handling control to manual as default.
        self._control_mode = manual.Manual(self._frame, self._io, self._kinematics)

    def run(self):
        self._io.update()
        self._control_mode.loop()

    def shutdown(self):
        """Shutdown the ROV hardware."""
        # TODO: Implement this method further.
        self._control_mode.shutdown()
        print("ROV shutdown complete.")
