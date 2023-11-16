class Vector2:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y
        self.offset = self.Offset()

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        elif isinstance(other, tuple):
            return Vector2(self.x + other[0], self.y + other[1])
        else:
            return NotImplemented

    def set_pos(self, _tuple: tuple[int, int]) -> None:
        self.x = _tuple[0]
        self.y = _tuple[1]

    def set_offset(self, _tuple: tuple[int, int]) -> None:
        self.offset.x = _tuple[0]
        self.offset.y = _tuple[1]

    def get_tuple(self) -> tuple[int, int]:
        return self.x, self.y

    def get_tuplef(self) -> tuple[float, float]:
        return float(self.x), float(self.y)

    def get_offset_tuple(self) -> tuple[int, int]:
        return self.offset.x, self.offset.y

    def get_offset_tuplef(self) -> tuple[float, float]:
        return float(self.offset.x), float(self.offset.y)

    class Offset:
        def __init__(self):
            self.x = 0
            self.y = 0
