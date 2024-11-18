from typing import Callable

# import topside.config as config
# from hardware import ThrusterPWM, FrameThrusters
import hardware.thruster_pwm as thruster_pwm
import mqtt_handler
import rovs.spike.rov_config as rov_config
import rovs.spike.manual as manual
import rovs.spike.enums as enums
# from rovs.spike.manual import Manual
# from rovs.spike.rov_config import SpikeConfig, ThrusterPositions


class ROV:
    _config: rov_config.ROVConfig

    _thrusters: dict[enums.ThrusterPositions, thruster_pwm.ThrusterPWM]
    _inputs_getter_map: dict[str, Callable[[], any]]  # Function to call to obtain input of a given name.

    def __init__(self, spike_config: rov_config.ROVConfig,
                 input_getter: dict[str, Callable[[], any]], rov_connection: mqtt_handler.ROVConnection) -> None:
        """Create and initialize the ROV hardware.

        Args:
            spike_config (SpikeConfig):
                Configuration of the ROV.
            input_getter (dict[str, dict[str, Callable[[], any]]):
                Dictionary of callables used to get the inputs.
        """
        self._config = spike_config
        self._thrusters = {}
        self._inputs_getter_map = input_getter

        # Configure thrusters.
        for position, thruster_config in self._config.thruster_configs.items():
            self._thrusters[position] = thruster_pwm.ThrusterPWM(thruster_config)

        self._frame = thruster_pwm.FrameThrusters(self._thrusters)

        # Set the class handling control to manual as default.
        self._control_mode = manual.Manual(self._frame, rov_connection)

        # Used to flag a desired shutdown of the ROV.
        self.continue_running = True

    def get_inputs(self) -> dict[str, dict[enums.ControllerButtonNames | enums.ControllerAxisNames, object]]:
        """Get the inputs from the controller and otherwise.

        Returns:
            dict[str, dict[enums.ControllerButtonNames | enums.ControllerAxisNames, object]]: The inputs matched to the
                references to the functions which return the inputs. (It's Eric's fault)
        """
        input_functions = {}

        # Gets inputs from the controller, sensors, and otherwise by calling the functions in the input_getter_map and
        # stores the results in a dictionary of dictionaries categorized by input type (e.g. "controller"), then by
        # input name (e.g. "enums.ControllerAxisNames.LEFT_X").
        for input_type in self._inputs_getter_map:
            value = self._inputs_getter_map[input_type]()
            input_functions[input_type] = value

        return input_functions

    def run(self):
        self._control_mode.update(self.get_inputs())

    def shutdown(self):
        """Shutdown the ROV hardware."""
        # TODO: Implement this method further.
        self._control_mode.shutdown()
        print("ROV shutdown complete.")
