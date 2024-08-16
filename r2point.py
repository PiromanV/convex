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

    # Коллениарны ли 2 отрезка?
    @staticmethod
    def is_colleniars(p1, q1, p2, q2):
        return (p1.x - q1.x == 0) and (p2.x - q2.x == 0) or\
           (p1.y - q1.y == 0) and (p2.y - q2.y == 0)

    # Сколько точек пересечения у стороны выпуклой оболочки с заданым прямоугольником?
    def count_points_intersect(self, point, rectangle=None):
        if rectangle is None:
            try:
                from __main__ import rectangle
            except:
                rectangle = [
                    R2Point(0.0, 0.0),
                    R2Point(0.0, 1.0),
                    R2Point(1.0, 1.0),
                    R2Point(1.0, 0.0)
                    ]
        a, b, c, d = rectangle[0], rectangle[1], rectangle[2], rectangle[3]
        is_inf = False
        intersections = int(self in rectangle) + int(point in rectangle)

        for p, q in (a, b), (b, c), (c, d), (d, a):
            p_on_segment = not R2Point.is_triangle(p, self, point) and p.is_inside(self, point)
            q_on_segment = not R2Point.is_triangle(q, self, point) and q.is_inside(self, point)
            self_on_side = not R2Point.is_triangle(self, p, q) and self.is_inside(p, q)
            point_on_side = not R2Point.is_triangle(point, p, q) and point.is_inside(p, q)

            lights = [
                    self.is_light(p, q),
                    point.is_light(p, q),
                    p.is_light(self, point),
                    q.is_light(self, point)
                ]

            if self == point:
                if self.is_inside(p, q):
                    return 1, False
            elif R2Point.is_colleniars(self, point, p, q):
                if self_on_side or point_on_side or p_on_segment or q_on_segment:
                    is_inf = True
            elif self_on_side and (self not in (p, q)) or\
                    point_on_side and (point not in (p, q)):
                intersections += 1
            elif p_on_segment and (p not in (self, point)) or\
                    q_on_segment and (q not in (self, point)):
                intersections += 0.5
            elif (lights[0] ^ lights[1]) and (lights[2] ^ lights[3]) and\
                not (self in (p, q) or point in (p, q)):
                intersections += 1

        return intersections * (not is_inf), is_inf

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
