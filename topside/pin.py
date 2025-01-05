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
        return self._id == self._id and self._mode == self._mode and self._val == self._val and self._freq == self._freq

    def __ne__(self, other):
        return not self.__eq__(other)