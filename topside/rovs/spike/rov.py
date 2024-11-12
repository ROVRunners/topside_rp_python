import topside.config as config
from hardware import ThrusterPWM
from typing import Callable

from rovs.spike.rov_config import SpikeConfig, ThrusterPosition

class Spike():
    _config: SpikeConfig

    _thrusters: dict[ThrusterPosition, ThrusterPWM]
    _inputs_map:dict[str, Callable] # Function to call to obtain input of a given name

    def __init__(self, spike_config: SpikeConfig,
                       input_getter: dict[str, Callable[[], any]]):
        """Create and initialize the ROV hardware
        :param spike_config: Configuration of the ROV
        :param input_getter: Function to call to obtain inputs to ROV"""
        self._config = spike_config
        self._thrusters = {}

        for position, tconfig in spike_config.thruster_configs:
            self._thrusters[position] = ThrusterPWM(tconfig)

    def get_inputs(self) -> dict[str, object]:
        output = {}
        for key, input_func in self._inputs_map:
            value = input_func()
            output[key] = value

        return output

    def run(self):
        inputs = self.get_inputs()


