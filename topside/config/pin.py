from typing import NamedTuple

class PinConfig(NamedTuple):
    """Describe a pin configuration"""
    id: int
    mode: str
    val: int
    freq: int | None = None
