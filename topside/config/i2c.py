from typing import NamedTuple

class I2CConfig(NamedTuple):
    """Describe a i2c configuration"""
    addr: str
    sending_vals: dict[int, str] | None = {}
    received_vals: dict[str, str] | None = None # dict[name, string of concatenated bytes]
    reading_registers: dict[str, tuple[int, int]] | None = None # dict[name of register, tuple[register, number of bytes]]
    poll_val: dict[int, int] | None = None
