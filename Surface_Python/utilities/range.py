class Range:

    def normalize(self, val: float) -> float:
        """A 0-1 range between a min and max value, inclusive"""
        val = self.clip(val)
        return (val - self.min_val) / (self.max_val - self._min_val)

    @property
    def min_val(self) -> float:
        return self._min_val

    @property
    def max_val(self) -> float:
        return self._max_val

    def contains(self, val: float) -> bool:
        """
        :param val: value to test
        :return: True if the value is within the range
        """
        return self._min_val <= val <= self._max_val

    def clip(self, val: float) -> float:
        """
        :param val: value to compare
        :return: nearest value within the range
        """
        if val < self._min_val:
            return self._min_val

        return val if val <= self._max_val else self._max_val

    def interpolate(self, scalar: float) -> float:
        """
        :param scalar: A scalar representing the distance between min/max
        :return: The value, ex: 0.5 is the midpoint between min/max
        """
        return (self._range * scalar) + self._min_val

    def __init__(self, min_val: float, max_val: float):
        self._min_val = min_val
        self._max_val = max_val
        self._range = max_val - min_val