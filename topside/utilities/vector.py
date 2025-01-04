import math


class Vector3:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0,
                 yaw: float = 0, pitch: float = 0, roll: float = 0) -> None:
        """Initialize the Vector3 object.

        Args:
            x (float, optional):
                The x component of the vector.
                Defaults to 0.
            y (float, optional):
                The y component of the vector.
                Defaults to 0.
            z (float, optional):
                The z component of the vector.
                Defaults to 0.
            yaw (float, optional):
                The alternative yaw of the vector. Replaces x and is simply a renaming.
                Defaults to 0.
            pitch (float, optional):
                The alternative pitch of the vector. Replaces y and is simply a renaming.
                Defaults to 0.
            roll (float, optional):
                The alternative roll of the vector. Replaces z and is simply a renaming.
                Defaults to 0.
        """
        self.x = x if yaw == 0 else yaw
        self.y = y if pitch == 0 else pitch
        self.z = z if roll == 0 else roll

    @property
    def yaw(self) -> float:
        """The yaw of the vector."""
        return self.x

    @property
    def pitch(self) -> float:
        """The pitch of the vector."""
        return self.y

    @property
    def roll(self) -> float:
        """The roll of the vector."""
        return self.z

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
