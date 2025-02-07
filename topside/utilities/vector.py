import math


class Vector3:
    """A 3D vector class.

    Properties:
        x (float):
            The x component of the vector.
        y (float):
            The y component of the vector.
        z (float):
            The z component of the vector.
        yaw (float):
            The yaw of the vector.
        pitch (float):
            The pitch of the vector.
        roll (float):
            The roll of the vector.
        magnitude (float):
            The overall hypotenuse of the vector.
    """

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
        if isinstance(other, Vector3):
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        elif isinstance(other, (int, float)):
            return Vector3(self.x + other, self.y + other, self.z + other)
        else:
            raise TypeError(f"Unsupported type for addition: {type(other)}")

    def __sub__(self, other) -> 'Vector3':
        if isinstance(other, Vector3):
            return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
        elif isinstance(other, (int, float)):
            return Vector3(self.x - other, self.y - other, self.z - other)
        else:
            raise TypeError(f"Unsupported type for subtraction: {type(other)}")

    def __mul__(self, other) -> 'Vector3':
        if isinstance(other, Vector3):
            return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)
        elif isinstance(other, (int, float)):
            return Vector3(self.x * other, self.y * other, self.z * other)
        else:
            raise TypeError(f"Unsupported type for multiplication: {type(other)}")

    def __truediv__(self, other) -> 'Vector3':
        if isinstance(other, Vector3):
            return Vector3(self.x / other.x, self.y / other.y, self.z / other.z)
        elif isinstance(other, (int, float)):
            return Vector3(self.x / other, self.y / other, self.z / other)
        else:
            raise TypeError(f"Unsupported type for division: {type(other)}")

    def __floordiv__(self, other) -> 'Vector3':
        if isinstance(other, Vector3):
            return Vector3(self.x // other.x, self.y // other.y, self.z // other.z)
        elif isinstance(other, (int, float)):
            return Vector3(self.x // other, self.y // other, self.z // other)
        else:
            raise TypeError(f"Unsupported type for floor division: {type(other)}")

    def __mod__(self, other) -> 'Vector3':
        if isinstance(other, Vector3):
            return Vector3(self.x % other.x, self.y % other.y, self.z % other.z)
        elif isinstance(other, (int, float)):
            return Vector3(self.x % other, self.y % other, self.z % other)
        else:
            raise TypeError(f"Unsupported type for modulo: {type(other)}")

    def __pow__(self, other) -> 'Vector3':
        if isinstance(other, Vector3):
            return Vector3(self.x ** other.x, self.y ** other.y, self.z ** other.z)
        elif isinstance(other, (int, float)):
            return Vector3(self.x ** other, self.y ** other, self.z ** other)
        else:
            raise TypeError(f"Unsupported type for exponentiation: {type(other)}")

    def __abs__(self) -> 'Vector3':
        return Vector3(abs(self.x), abs(self.y), abs(self.z))

    def __neg__(self) -> 'Vector3':
        return Vector3(-self.x, -self.y, -self.z)

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other) -> bool:
        return not self == other

    def __lt__(self, other) -> bool:
        return self.magnitude < other.magnitude

    def __le__(self, other) -> bool:
        return self.magnitude <= other.magnitude

    def __gt__(self, other) -> bool:
        return self.magnitude > other.magnitude

    def __ge__(self, other) -> bool:
        return self.magnitude >= other.magnitude

    def __str__(self) -> str:
        return f"Vector3({self.x}, {self.y}, {self.z})"

    def __repr__(self) -> str:
        return str(self)


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
