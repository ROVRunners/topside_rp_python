from config.i2c import I2CConfig


class I2C:

    def __init__(self, config: I2CConfig):
        self._config = config

        self._addr = self._config.addr
        self._poll_val = self._config.poll_val
        self._sending_vals = self._config.sending_vals

        self._received_vals = self._config.received_vals
        self._reading_registers = self._config.reading_registers

    @property
    def addr(self):
        return self._addr

    @addr.setter
    def addr(self, value):
        self._addr = value

    @property
    def poll_val(self):
        return self._poll_val

    @poll_val.setter
    def poll_val(self, value):
        self._poll_val = value

    @property
    def received_vals(self):
        return self._received_vals

    @received_vals.setter
    def received_vals(self, received_value):
        self._received_vals = received_value

    @property
    def sending_vals(self):
        return self._sending_vals

    @sending_vals.setter
    def sending_vals(self, sending_value):
        self._sending_vals = sending_value

    @property
    def reading_registers(self):
        return self._reading_registers

    @reading_registers.setter
    def reading_registers(self, reading_registers):
        self._reading_registers = reading_registers

    def __eq__(self, other):
        return (
            self._addr == other.addr and self._poll_val == other.poll_val and
            self._sending_vals == other.sending_vals, self._received_vals == other.received_vals,
            self._reading_registers == other.reading_registers
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __deepcopy__(self, meta):
        return I2C(I2CConfig(
            addr=self._addr,
            poll_val=self._poll_val,
            sending_vals=self.sending_vals,
            received_vals=self.received_vals,
            reading_registers=self.reading_registers,
        ))