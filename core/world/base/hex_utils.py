import math
from typing import List, Type
from abc import abstractmethod


class HexMathAbs:
    ANGLES: List[float]
    DEFAULT_ODD = True

    @classmethod
    def normalize_coordinates(cls, x, y, r, odd=None) -> tuple[int, int]:
        return cls.get_center(*cls.get_indexes_from_coordinates(x, y, r, odd), r, odd)

    @classmethod
    def get_dots_by_xy(cls, x, y, r, dx=0, dy=0, odd=None):
        odd = cls.DEFAULT_ODD if odd is None else odd
        x, y = cls.get_center(x, y, r, odd=odd)
        return cls.get_dots(x, y, r, dx=dx, dy=dy)

    @classmethod
    @abstractmethod
    def get_lt_by_id(cls, x, y, r, dx=0, dy=0, odd=None):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_width(r) -> float:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_height(r) -> float:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def horizontal_spacing(r) -> float:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def vertical_spacing(r) -> float:
        raise NotImplementedError

    @classmethod
    def get_dots(cls, x, y, r, dx=0, dy=0) -> list:
        return [(int(x + dx + r * math.cos(a)), int(y + dy + r * math.sin(a))) for a in cls.ANGLES]

    @classmethod
    @abstractmethod
    def get_center(cls, x, y, r, dx=0, dy=0, odd=None):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_indexes_from_coordinates(x, y, r, odd=None):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_horizontal_size(cls, x, r) -> int:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_vertical_size(cls, y, r) -> int:
        raise NotImplementedError

    @classmethod
    def get_map_size(cls, x, y, r):
        return cls.get_horizontal_size(x, r), cls.get_vertical_size(y, r)


class PointTopHex(HexMathAbs):
    @classmethod
    def get_horizontal_size(cls, x, r) -> int:
        return int(cls.horizontal_spacing(r) * x + cls.get_width(r) / 2) + 1

    @classmethod
    def get_vertical_size(cls, y, r) -> int:
        return int(cls.vertical_spacing(r) * y + cls.get_height(r) * 0.25) + 1

    ANGLES = [math.radians(30 + 60 * i) for i in range(6)]

    @classmethod
    def get_lt_by_id(cls, x, y, r, dx=0, dy=0, odd=None):
        odd = cls.DEFAULT_ODD if odd is None else odd
        dx0, dx1 = (0.5, 0.) if odd else (0., 0.5)
        x += dx0 if y % 2 else dx1
        x0 = x * PointTopHex.horizontal_spacing(r)
        y0 = y * PointTopHex.vertical_spacing(r)

        return int(x0), int(y0)

    @classmethod
    def get_center(cls, x, y, r, dx=0, dy=0, odd=None):
        x0, y0 = cls.get_lt_by_id(x, y, r, dx, dy, odd)
        x0 += PointTopHex.get_width(r) / 2
        y0 += PointTopHex.get_height(r) / 2

        return int(x0), int(y0)

    @staticmethod
    def get_indexes_from_coordinates(x, y, r, odd=None):
        odd = PointTopHex.DEFAULT_ODD if odd is None else odd
        y = y // PointTopHex.vertical_spacing(r)
        if (odd and y % 2) or (not odd and not y % 2):
            x -= PointTopHex.get_width(r) / 2
        x = x // PointTopHex.get_width(r)

        return int(x), int(y)

    @staticmethod
    def get_width(r) -> float:
        return math.sqrt(3) * r

    @staticmethod
    def get_height(r) -> float:
        return r + r

    @staticmethod
    def horizontal_spacing(r) -> float:
        return PointTopHex.get_width(r)

    @staticmethod
    def vertical_spacing(r) -> float:
        return PointTopHex.get_height(r) * 0.75


class FlatTopHex(HexMathAbs):
    @classmethod
    def get_horizontal_size(cls, x, r) -> int:
        return int(cls.horizontal_spacing(r) * x + cls.get_width(r) * 0.25) + 1

    @classmethod
    def get_vertical_size(cls, y, r) -> int:
        return int(cls.vertical_spacing(r) * y + cls.get_height(r) / 2) + 1

    @classmethod
    def get_lt_by_id(cls, x, y, r, dx=0, dy=0, odd=None):
        odd = FlatTopHex.DEFAULT_ODD if odd is None else odd
        x0 = x * FlatTopHex.horizontal_spacing(r)
        dy0, dy1 = (0., 0.5) if odd else (0.5, 0.)
        y0 = (y + (dy0 if x % 2 else dy1)) * FlatTopHex.get_height(r)
        return int(x0), int(y0)

    @classmethod
    def get_center(cls, x, y, r, dx=0, dy=0, odd=None):
        x0, y0 = cls.get_lt_by_id(x, y, r, dx, dy, odd)
        x0 += FlatTopHex.get_width(r) / 2
        y0 += FlatTopHex.get_height(r) / 2
        return int(x0), int(y0)

    @staticmethod
    def get_indexes_from_coordinates(x, y, r, odd=None):
        odd = FlatTopHex.DEFAULT_ODD if odd is None else odd
        x = x // FlatTopHex.horizontal_spacing(r)
        if (odd and x % 2) or (not odd and not x % 2):
            y += FlatTopHex.vertical_spacing(r) / 2

        y = ((y - FlatTopHex.get_height(r) / 2) // FlatTopHex.get_height(r))
        return int(x), int(y)

    ANGLES = [math.radians(60 * i) for i in range(6)]

    @staticmethod
    def get_width(r) -> float:
        return r + r

    @staticmethod
    def get_height(r) -> float:
        return math.sqrt(3) * r

    @staticmethod
    def horizontal_spacing(r) -> float:
        return FlatTopHex.get_width(r) * 0.75

    @staticmethod
    def vertical_spacing(r) -> float:
        return FlatTopHex.get_height(r)


def get_hex_math(flat=True, odd=True) -> Type[PointTopHex | FlatTopHex]:
    (FlatTopHex if flat else PointTopHex).DEFAULT_ODD = odd
    return FlatTopHex if flat else PointTopHex
