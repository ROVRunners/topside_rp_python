from typing import Callable

import hardware.thruster_pwm as thruster_pwm
import rov_config
from surface_main import IO

import manual


class ROV:

    def __init__(self, rov_config: rov_config.ROVConfig, io: IO) -> None:
        """Create and initialize the ROV hardware.

        Args:
            main_system ('surface_main.MainSystem'):
                The MainSystem object.
        """
        self._config = rov_config
        self._io = io
        self._thrusters = {}

        # Configure thrusters.
        for position, thruster_config in self._config.thruster_configs.items():
            self._thrusters[position] = thruster_pwm.ThrusterPWM(thruster_config)

        self._frame = thruster_pwm.FrameThrusters(self._thrusters)

        # Set the class handling control to manual as default.
        self._control_mode = manual.Manual(self._frame, self._io)

    def run(self):
        self._io.update_inputs()
        self._control_mode.loop()

    def shutdown(self):
        """Shutdown the ROV hardware."""
        # TODO: Implement this method further.
        self._control_mode.shutdown()
        print("ROV shutdown complete.")
