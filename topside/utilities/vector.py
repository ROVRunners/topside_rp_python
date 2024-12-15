import math


class Vector3:
    def __init__(self, x: float, y: float, z: float) -> None:
        """Initialize the Vector3 object.

        Args:
            x (float):
                The x component of the vector.
            y (float):
                The y component of the vector.
            z (float):
                The z component of the vector.
        """
        self.x = x
        self.y = y
        self.z = z

    @property
    def magnitude(self) -> float:
        """The overall hypotenuse of the vector."""
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __add__(self, other) -> 'Vector3':
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other) -> 'Vector3':
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    # def __mul__(self, other) -> 'Vector3':
    #     return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)


class Vector2:
    def __init__(self, x: float, y: float) -> None:
        """Initialize the Vector2 object.

        Args:
            x (float):
                The x component of the vector.
            y (float):
            The y component of the vector.
        """
        self.x = x
        self.y = y

    @property
    def magnitude(self) -> float:
        """The overall hypotenuse of the vector."""
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __add__(self, other) -> 'Vector2':
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other) -> 'Vector2':
        return Vector2(self.x - other.x, self.y - other.y)
