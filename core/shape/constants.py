from typing import Iterable, Tuple, List, Union


class ShapeType:
    Rect = 'rect'
    Circle = 'circle'
    SemiCircle = 'semi_circle'
    Line = 'line'
    Point = 'point'
    Hexagon = 'hexagon'


Vector2DType = Union[tuple[int, int], list[int, int]]
DotsContainerType = Iterable[Vector2DType]
