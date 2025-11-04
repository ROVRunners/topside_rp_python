class Range:
    """A class representing a range of float values.

    Properties:
        min_val (float):
            The minimum float value of the range.
        max_val (float):
            The maximum float value of the range.
        range (float):
            The range of the values.

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

    def __init__(self, min_value: float, max_value: float) -> None:
        """Initializes the range with a minimum and maximum value.

        Args:
            min_value (float):
                The minimum value of the range.
            max_value (float):
                The maximum value of the range.
        """
        self._min_val = min_value
        self._max_val = max_value
        self._range = max_value - min_value

    def normalize(self, val: float) -> float:
        """Places the value on a 0-1 range between the class's min and max values, inclusive.

        Args:
            val (float):
                The value to normalize.

        Returns:
            float: The normalized value.
        """
        val = self.clip(val)

        return (val - self.min_value) / (self.max_value - self.min_value)

    @property
    def min_value(self) -> float:
        """The minimum float value of the range."""
        return self._min_val

    @property
    def max_value(self) -> float:
        """The maximum float value of the range."""
        return self._max_val

    @min_value.setter
    def min_value(self, val: float) -> None:
        """Sets the minimum value of the range."""
        self._min_val = val
        self._range = self._max_val - val

    @max_value.setter
    def max_value(self, val: float) -> None:
        """Sets the maximum value of the range."""
        self._max_val = val
        self._range = val - self._min_val

    @property
    def range(self) -> float:
        """The calculated distance between the min and max values."""
        return self._range

    def contains(self, val: float) -> bool:
        """Checks if the value is within the range.

        Args:
            val (float):
                The value to test.
        Returns:
            bool: True if the value is within the range.
        """
        return self.min_value <= val <= self.max_value

    def clip(self, val: float) -> float:
        """Clips the value to the range. If the value is less than the minimum, the minimum is returned. If the value
        is greater than the maximum, the maximum is returned.

        Args:
            val (float):
                The value to compare.
        Returns:
            float: The nearest value within the range.
        """
        if val < self.min_value:
            return self.min_value

        return val if val <= self.max_value else self.max_value

    def interpolate(self, scalar: float) -> float:
        """Interpolates a value from 0-1 between the min and max values of the range. In other words, it returns a value
        between the min and max values based on the scalar.

        Args:
            scalar (float):
                A scalar representing the distance between min/max.

        Returns:
            float: The value, ex: 0.5 is the midpoint between min/max.
        """
        return (self._range * scalar) + self.min_value

    def map(self, val: float, old_range: "Range") -> float:
        """Maps the value from a different range to this range.

        Args:
            val (float):
                The value to map.
            old_range (Range):
                The range to map from.

        Returns:
            float: The value mapped to this range.
        """
        return self.interpolate(old_range.normalize(val))
