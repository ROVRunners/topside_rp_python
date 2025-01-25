from typing import NamedTuple

class I2CConfig(NamedTuple):
    """Describe a i2c configuration"""
    addr: str
    sending_vals: dict[int, str] | None = None
    received_vals: dict[int, str] | None = None
    poll_val: str | None = None
