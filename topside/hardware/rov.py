import os.path
import sys

import hardware.thruster_pwm as thruster_pwm
import surface_main

# Import the ROV

# Get the current parent file
current_path = os.path.dirname(os.path.abspath(__file__))
# TODO: Make this dynamic based on a file
rov_path = os.path.join(current_path, "..\\rovs\\spike")
# Add the folder to the import path.
sys.path.append(rov_path)

import manual


class ROV:

    def __init__(self, main_system: 'surface_main.MainSystem') -> None:
        """Create and initialize the ROV hardware.

        Args:
            main_system ('surface_main.MainSystem'):
                The MainSystem object.
        """
        self._main_system = main_system
        self._config = self._main_system.rov_config

        self._thrusters = {}

        # Configure thrusters.
        for position, thruster_config in self._config.thruster_configs.items():
            self._thrusters[position] = thruster_pwm.ThrusterPWM(thruster_config)

        self._frame = thruster_pwm.FrameThrusters(self._thrusters)

        # Set the class handling control to manual as default.
        self._control_mode = manual.Manual(self._frame, self._main_system)

    def run(self):
        self._control_mode.loop()

    def shutdown(self):
        """Shutdown the ROV hardware."""
        # TODO: Implement this method further.
        self._control_mode.shutdown()
        print("ROV shutdown complete.")
