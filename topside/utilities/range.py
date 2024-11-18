class Range:
    """A class representing a range of float values.

    Properties:
        min_val (float):
            The minimum float value of the range.
        max_val (float):
            The maximum float value of the range.

    Methods:
        normalize(val: float) -> float:
            Places the value on a 0-1 range between the class's min and max values, inclusive.
        contains(val: float) -> bool:
            Checks if the value is within the range.
        clip(val: float) -> float:
            Clips the value to the range. If the value is less than the minimum, the minimum is returned. If the value
            is greater than the maximum, the maximum is returned.
        interpolate(scalar: float) -> float:
            Interpolates a value from 0-1 between the min and max values of the range.
    """

    def __init__(self, min_val: float, max_val: float) -> None:
        """Initializes the range with a minimum and maximum value.

        Args:
            min_val (float):
                The minimum value of the range.
            max_val (float):
                The maximum value of the range.
        """
        self._min_val = min_val
        self._max_val = max_val
        self._range = max_val - min_val

    def normalize(self, val: float) -> float:
        """Places the value on a 0-1 range between the class's min and max values, inclusive.

        Args:
            val (float):
                The value to normalize.

        Returns:
            float: The normalized value.
        """
        val = self.clip(val)

        return (val - self.min_val) / (self.max_val - self._min_val)

    @property
    def min_val(self) -> float:
        """The minimum float value of the range."""
        return self._min_val

    @property
    def max_val(self) -> float:
        """The maximum float value of the range."""
        return self._max_val

    @min_val.setter
    def min_val(self, val: float) -> None:
        """Sets the minimum value of the range."""
        self._min_val = val
        self._range = self._max_val - val

    @max_val.setter
    def max_val(self, val: float) -> None:
        """Sets the maximum value of the range."""
        self._max_val = val
        self._range = val - self._min_val

    def contains(self, val: float) -> bool:
        """Checks if the value is within the range.

        Args:
            val (float):
                The value to test.
        Returns:
            bool: True if the value is within the range.
        """
        return self._min_val <= val <= self._max_val

    def clip(self, val: float) -> float:
        """Clips the value to the range. If the value is less than the minimum, the minimum is returned. If the value
        is greater than the maximum, the maximum is returned.

        Args:
            val (float):
                The value to compare.
        Returns:
            float: The nearest value within the range.
        """
        if val < self._min_val:
            return self._min_val

        return val if val <= self._max_val else self._max_val

    def interpolate(self, scalar: float) -> float:
        """Interpolates a value from 0-1 between the min and max values of the range.

        Args:
            scalar (float):
                A scalar representing the distance between min/max.

        Returns:
            float: The value, ex: 0.5 is the midpoint between min/max.
        """
        return (self._range * scalar) + self._min_val
