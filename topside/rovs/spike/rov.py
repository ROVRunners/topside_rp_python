import topside.config as config
from hardware import ThrusterPWM, FrameThrusters
from typing import Callable
from rovs.spike.manual import Manual
from rovs.spike.rov_config import SpikeConfig, ThrusterPosition


class Spike:
    _config: SpikeConfig

    _thrusters: dict[ThrusterPosition, ThrusterPWM]
    _inputs_map: dict[str, Callable] # Function to call to obtain input of a given name

    def __init__(self, spike_config: SpikeConfig,
                 input_getter: dict[str, Callable[[], any]]):
        """Create and initialize the ROV hardware.
        :param spike_config: Configuration of the ROV
        :param input_getter: Function to call to obtain inputs to ROV"""
        self._config = spike_config
        self._thrusters = {}
        self._inputs_map = input_getter

        for position, tconfig in self._config.thruster_configs.items():
            self._thrusters[position] = ThrusterPWM(tconfig)

        self._frame = FrameThrusters(self._thrusters[ThrusterPosition.FRONT_LEFT],
                                     self._thrusters[ThrusterPosition.FRONT_RIGHT],
                                     self._thrusters[ThrusterPosition.REAR_LEFT],
                                     self._thrusters[ThrusterPosition.REAR_RIGHT])

        self._control_mode = Manual(self._frame)

    def get_inputs(self) -> dict[str, object]:
        output = {}
        for key in self._inputs_map:
            value = self._inputs_map[key]()
            output[key] = value

        return output['controller']

    def run(self):
        self._control_mode.update(self.get_inputs())


