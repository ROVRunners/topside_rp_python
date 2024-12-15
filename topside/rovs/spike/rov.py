import os.path
import sys
from typing import Callable

import hardware.thruster_pwm as thruster_pwm
import rov_config

# Import the ROV

# Get the current parent file
current_path = os.path.dirname(os.path.abspath(__file__))
# TODO: Make this dynamic based on a file
rov_path = os.path.join(current_path, "..\\rovs\\spike")
# Add the folder to the import path.
sys.path.append(rov_path)

import manual


class ROV:

    def __init__(self, rov_config: rov_config.ROVConfig, input_getter: dict[str, Callable[[], any]],
                 output_map: dict[str, Callable]) -> None:
        """Create and initialize the ROV hardware.

        Args:
            main_system ('surface_main.MainSystem'):
                The MainSystem object.
        """
        self._config = rov_config
        self._inputs_getter_map = input_getter
        self._thrusters = {}

        # Configure thrusters.
        for position, thruster_config in self._config.thruster_configs.items():
            self._thrusters[position] = thruster_pwm.ThrusterPWM(thruster_config)

        self._frame = thruster_pwm.FrameThrusters(self._thrusters)

        # Set the class handling control to manual as default.
        self._control_mode = manual.Manual(self._frame)

    def run(self):
        self._control_mode.loop()

    def shutdown(self):
        """Shutdown the ROV hardware."""
        # TODO: Implement this method further.
        self._control_mode.shutdown()
        print("ROV shutdown complete.")
