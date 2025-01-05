from typing import overload

from config.pin import PinConfig

class Pin:

    def __init__(self, config: PinConfig):

        self._config = config

        self._id = self._config.id
        self._mode = self._config.mode
        self._val = self._config.val
        self._freq = self._config.freq

    @property
    def index(self):
        return self._id

    @index.setter
    def index(self, value):
        self._id = value

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        self._mode = value

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, value):
        self._val = value

    @property
    def freq(self):
        return self._freq

    @freq.setter
    def freq(self, value):
        self._freq = value

    def __eq__(self, other):
        return self._id == other._id and self._mode == other._mode and self._val == other._val and self._freq == other._freq

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __deepcopy__(self, meta):
        return Pin(PinConfig(
            id=self._id,
            mode=self._mode,
            val=self._val,
            freq=self._freq,
            ))