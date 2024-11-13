# import topside.config as config
from hardware import ThrusterPWM, FrameThrusters
from typing import Callable
from rovs.spike.manual import Manual
from rovs.spike.rov_config import SpikeConfig, ThrusterPositions


class Spike:
    _config: SpikeConfig

    _thrusters: dict[ThrusterPositions, ThrusterPWM]
    _inputs_map: dict[str, Callable]  # Function to call to obtain input of a given name.

    def __init__(self, spike_config: SpikeConfig,
                 input_getter: dict[str, Callable[[], any]]):
        """Create and initialize the ROV hardware.

        Args:
            spike_config (SpikeConfig):
                Configuration of the ROV.
            input_getter (dict[str, dict[str, Callable[[], any]]):
                Dictionary of callables used to get the inputs.
        """
        self._config = spike_config
        self._thrusters = {}
        self._inputs_map = input_getter

        # Configure thrusters.
        for position, thruster_config in self._config.thruster_configs.items():
            self._thrusters[position] = ThrusterPWM(thruster_config)

        self._frame = FrameThrusters(self._thrusters)

        # Set the class handling control to manual as default.
        self._control_mode = Manual(self._frame)

    def get_inputs(self) -> dict[str, dict[str, object]]:
        """Get the inputs from the controller and otherwise.

        Returns:
            dict[str, object]: The inputs matched to the references to the functions which return the inputs.
                (It's Eric's fault)
        """
        input_functions = {}
        for key in self._inputs_map:
            value = self._inputs_map[key]()
            input_functions[key] = value

        return input_functions

    def run(self):
        self._control_mode.update(self.get_inputs())
