from typing import Iterable, Union

__all__ = 'ShapeType', 'Vector2DType', 'DotsContainerType'


class ShapeType:
    Rect = 'rect'
    Circle = 'circle'
    SemiCircle = 'semi_circle'
    Line = 'line'
    Point = 'point'
    Hexagon = 'hexagon'


Vector2DType = Union[tuple[int, int], list[int, int]]
DotsContainerType = Iterable[Vector2DType]
