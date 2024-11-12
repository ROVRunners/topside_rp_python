from typing import NamedTuple

class RangeConfig(NamedTuple):
    """Describes a range of values"""
    min: float
    max: float


class OptionalRange(NamedTuple):
    """Describes a range of values.  Either min or max can be None"""
    min: float | None
    max: float | None


class IntRange(NamedTuple):
    """Describes a range of values"""
    min: int
    max: int


class OptionalIntRange(NamedTuple):
    """Describes a range of values.  Either min or max can be None"""
    min: float | None
    max: float | None