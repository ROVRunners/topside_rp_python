from config.pin import PinConfig

class Pin:

    def __init__(self, config: PinConfig):

        self._config = config

        self._index = self._config.index
        self._mode = self._config.mode
        self._val = self._config.val
        self._freq = self._config.freq

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        self._index = value

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