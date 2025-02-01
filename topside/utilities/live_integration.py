from enum import Enum
import time


class IntegrationTypes(Enum):
    """An enumeration to represent the types of integration."""
    LEFT_HANDED = "LEFT_HANDED"
    RIGHT_HANDED = "RIGHT_HANDED"
    MIDPOINT = "MIDPOINT"
    TRAPEZOIDAL = "TRAPEZOIDAL"
    SIMPSONS = "SIMPSONS"
    GAUSSIAN = "GAUSSIAN"


class Integration:
    """A class to represent an integration object.

    Properties:
        integration_type (IntegrationTypes):
            The type of integration.
        integration_value (float):
            The value of the integration.

    Methods:
        add_entry(value: float | int, instance_time: float | int = time.time()) -> None:
            Add an entry to the integration.
    """

    def __init__(self, integration_type: IntegrationTypes = IntegrationTypes.LEFT_HANDED, initial_value: float = 0.0,
                 initial_time: float = time.time(), internal_time: bool = True) -> None:
        """Initialize the Integration object.

        Args:
            integration_type (IntegrationTypes, optional):
                The type of integration.
                Defaults to IntegrationTypes.LEFT_HANDED.
            initial_value (float, optional):
                The value of the integration.
                Defaults to 0.0.
            initial_time (float, optional):
                The initial time of the integration.
                Defaults to time.time().
            internal_time (bool, optional):
                Whether to use the internal time or require the user to input the time value for each entry.
                Defaults to True.
        """
        self._integration_type: IntegrationTypes = integration_type
        self._initial_value: float = initial_value
        self._initial_time: float = initial_time
        self._internal_time: bool = internal_time

        self._last_value: float = self._initial_value
        self._last_time: float = self._initial_time
        self._sum: float = self._initial_value

    @property
    def integration_type(self) -> IntegrationTypes:
        return self._integration_type

    @property
    def sum(self) -> float:
        return self._sum

    def add_entry(self, value: float | int, instance_time: float | int = time.time()) -> float:
        """Add an entry to the integration.

        Args:
            value (float | int):
                The value of the entry.
            instance_time (float | int, optional):
                The time of the entry.
                Defaults to time.time().
        """
        self._sum += self._calculate_entry(value, instance_time)
        self._last_value = value
        self._last_time = instance_time

        return self._sum

    def reset(self) -> None:
        """Reset the integration."""
        self._last_value = self._initial_value
        self._last_time = self._initial_time
        self._sum = self._initial_value

    def _calculate_entry(self, value: float | int, instance_time: float | int) -> float:
        """Calculate the entry for the integration.

        Args:
            value (float | int):
                The value of the entry.
            instance_time (float | int):
                The time of the entry.

        Returns:
            float:
                The calculated entry.
        """
        match self._integration_type:
            case IntegrationTypes.LEFT_HANDED:
                return self._left_handed(value, instance_time)
            case IntegrationTypes.RIGHT_HANDED:
                return self._right_handed(value, instance_time)
            case IntegrationTypes.MIDPOINT:
                return self._midpoint(value, instance_time)
            case IntegrationTypes.TRAPEZOIDAL:
                return self._trapezoidal(value, instance_time)
            case IntegrationTypes.SIMPSONS:
                return self._simpsons(value, instance_time)
            case IntegrationTypes.GAUSSIAN:
                return self._gaussian(value, instance_time)
            case _:
                raise ValueError(f"Invalid integration type: {self._integration_type}")

    def _left_handed(self, value: float | int, instance_time: float | int) -> float:
        """Calculate the left-handed integration.

        Args:
            value (float | int):
                The value of the entry.
            instance_time (float | int):
                The time of the entry.

        Returns:
            float:
                The calculated entry.
        """
        return self._last_value * (instance_time - self._last_time)

    def _right_handed(self, value: float | int, instance_time: float | int) -> float:
        """Calculate the right-handed integration.

        Args:
            value (float | int):
                The value of the entry.
            instance_time (float | int):
                The time of the entry.

        Returns:
            float:
                The calculated entry.
        """
        return value * (instance_time - self._last_time)

    def _midpoint(self, value: float | int, instance_time: float | int) -> float:
        """Calculate the midpoint integration.

        Args:
            value (float | int):
                The value of the entry.
            instance_time (float | int):
                The time of the entry.

        Returns:
            float:
                The calculated entry.
        """
        return (self._last_value + value) * (instance_time - self._last_time) / 2

    def _trapezoidal(self, value: float | int, instance_time: float | int) -> float:
        """Calculate the trapezoidal integration.

        Args:
            value (float | int):
                The value of the entry.
            instance_time (float | int):
                The time of the entry.

        Returns:
            float:
                The calculated entry.
        """
        return (self._last_value + value) * (instance_time - self._last_time) / 2

    def _simpsons(self, value: float | int, instance_time: float | int) -> float:
        """Calculate the Simpsons integration.

        Args:
            value (float | int):
                The value of the entry.
            instance_time (float | int):
                The time of the entry.

        Returns:
            float:
                The calculated entry.
        """
        return (self._last_value + 4 * value) * (instance_time - self._last_time) / 6

    def _gaussian(self, value: float | int, instance_time: float | int) -> float:
        """Calculate the Gaussian integration. NOT IMPLEMENTED!

        Args:
            value (float | int):
                The value of the entry.
            instance_time (float | int):
                The time of the entry.

        Returns:
            float:
                The calculated entry.
        """
        raise NotImplementedError("Gaussian integration is not yet implemented.")

    def __str__(self) -> str:
        return f"Integration({self._integration_type}, {self._sum})"

    def __call__(self, value: float | int, instance_time: float | int = time.time()) -> float:
        return self.add_entry(value, instance_time)
