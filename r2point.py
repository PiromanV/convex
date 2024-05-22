from math import sqrt, inf


class R2Point:
    """ Точка (Point) на плоскости (R2) """

    # Конструктор
    def __init__(self, x=None, y=None):
        if x is None:
            x = float(input("x -> "))
        if y is None:
            y = float(input("y -> "))
        self.x, self.y = x, y

    # Площадь треугольника
    @staticmethod
    def area(a, b, c):
        return 0.5 * ((a.x - c.x) * (b.y - c.y) - (a.y - c.y) * (b.x - c.x))

    # Лежат ли точки на одной прямой?
    @staticmethod
    def is_triangle(a, b, c):
        return R2Point.area(a, b, c) != 0.0

    # Расстояние до другой точки
    def dist(self, other):
        return sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

    # Лежит ли точка внутри "стандартного" прямоугольника?
    def is_inside(self, a, b):
        return (((a.x <= self.x and self.x <= b.x) or
                 (a.x >= self.x and self.x >= b.x)) and
                ((a.y <= self.y and self.y <= b.y) or
                 (a.y >= self.y and self.y >= b.y)))

    # Освещено ли из данной точки ребро (a,b)?
    def is_light(self, a, b):
        s = R2Point.area(a, b, self)
        return s < 0.0 or (s == 0.0 and not self.is_inside(a, b))

    # Сколько точек пересечения у стороны выпуклой оболочки с заданым прямоугольником?
    def count_points_intersect(self, point, rectangle=None):
        if rectangle is None:
            try:
                from __main__ import rectangle
            except:
                rectangle = [R2Point(0.0, 0.0), R2Point(0.0, 1.0), R2Point(1.0, 1.0), R2Point(1.0, 0.0)]
        a, b, c, d = rectangle[0], rectangle[1], rectangle[2], rectangle[3]
        if self == point:
            return int((self.x == a.x or self.x == c.x) and (a.y <= self.y <= c.y) or
                       (self.y == a.y or self.y == c.y) and (a.x <= self.x <= c.x))
        else:
            sides = [(a, b), (b, c), (c, d), (d, a)]
            cnt = 0
            for p1, p2 in sides:
                if (R2Point.is_triangle(self, p1, p2) and R2Point.is_triangle(point, p1, p2) and
                        R2Point.is_triangle(self, point, p1) and R2Point.is_triangle(self, point, p2)):
                    if (p1.is_light(self, point) != p2.is_light(self, point) and
                            self.is_light(p1, p2) != point.is_light(p1, p2)):
                        cnt += 1
                elif not (R2Point.is_triangle(self, point, p1) or R2Point.is_triangle(self, point, p2)):
                    if (self.is_inside(p1, p2) or point.is_inside(p1, p2) or p1.is_inside(self, point)) and point != self:
                        return inf
                elif (not (R2Point.is_triangle(self, point, p1) and R2Point.is_triangle(self, point, p2)) and
                      (p1.is_inside(self, point) or p2.is_inside(self, point))):
                    cnt += 0.5
        return int(cnt)

    # Совпадает ли точка с другой?
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.x == other.x and self.y == other.y
        return False


if __name__ == "__main__":  # pragma: no cover
    x = R2Point(1.0, 1.0)
    print(type(x), x.__dict__)
    print(x.dist(R2Point(1.0, 0.0)))
    a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 0.0), R2Point(1.0, 1.0)
    print(R2Point.area(a, c, b))
