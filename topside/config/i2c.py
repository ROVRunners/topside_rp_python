from typing import NamedTuple

class I2CConfig(NamedTuple):
    """Describe a i2c configuration"""
    addr: str
    val: int
    poll_val: str | None = None
