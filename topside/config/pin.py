from typing import NamedTuple

class PinConfig(NamedTuple):
    """Describe a pin configuration"""
    index: int
    mode: str
    val: float
    freq: int | None = None
