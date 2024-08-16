from deq import Deq
from math import inf
from r2point import R2Point


class Figure:
    """ Абстрактная фигура """

    def perimeter(self):
        return 0.0

    def intersections(self):
        return 0

    def area(self):
        return 0.0


class Void(Figure):
    """ "Hульугольник" """

    def add(self, p):
        return Point(p)


class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p):
        self.p = p
        self._intersections, self.inf_intersections = R2Point.count_points_intersect(p, p)

    def intersections(self):
        return self._intersections

    def add(self, q):
        return self if self.p == q else Segment(self.p, q)


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q):
        self.p, self.q = p, q
        self._intersections, self.inf_intersections = R2Point.count_points_intersect(p, q)

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            return Polygon(self.p, self.q, r)
        elif r.is_inside(self.p, self.q):
            return self
        elif self.p.is_inside(r, self.q):
            return Segment(r, self.q)
        else:
            return Segment(self.p, r)

    def intersections(self):
        return inf if self.inf_intersections else self._intersections


class Polygon(Figure):
    """ Многоугольник """

    def __init__(self, a, b, c):
        self.points = Deq()
        self.points.push_first(b)
        if b.is_light(a, c):
            self.points.push_first(a)
            self.points.push_last(c)
        else:
            self.points.push_last(a)
            self.points.push_first(c)
        self._perimeter = a.dist(b) + b.dist(c) + c.dist(a)
        self._area = abs(R2Point.area(a, b, c))
        self._intersections, self.inf_intersections = 0, 0
        for (p, q) in [(a, b), (b, c), (a, c)]:
            self.change_intersections(p, q)

    def change_intersections(self, p, q, sub=0):
        if sub:
            intersect_info = R2Point.count_points_intersect(p, q)
            self.inf_intersections -= intersect_info[1]
            self._intersections -= intersect_info[0]
        else:
            intersect_info = R2Point.count_points_intersect(p, q)
            self.inf_intersections += intersect_info[1]
            self._intersections += intersect_info[0]

    def intersections(self):
        return inf if self.inf_intersections else self._intersections

    def perimeter(self):
        return self._perimeter

    def area(self):
        return self._area

    # добавление новой точки
    def add(self, t):

        # поиск освещённого ребра
        for n in range(self.points.size()):
            if t.is_light(self.points.last(), self.points.first()):
                break
            self.points.push_last(self.points.pop_first())

        # хотя бы одно освещённое ребро есть
        if t.is_light(self.points.last(), self.points.first()):

            # учёт удаления ребра, соединяющего конец и начало дека
            self._perimeter -= self.points.first().dist(self.points.last())
            self._area += abs(R2Point.area(t,
                                           self.points.last(),
                                           self.points.first()))
            self.change_intersections(self.points.last(), self.points.first(), 1)

            # удаление освещённых рёбер из начала дека
            p = self.points.pop_first()
            while t.is_light(p, self.points.first()):
                self._perimeter -= p.dist(self.points.first())
                self._area += abs(R2Point.area(t, p, self.points.first()))
                self.change_intersections(p, self.points.first(), 1)
                p = self.points.pop_first()
            self.points.push_first(p)

            # удаление освещённых рёбер из конца дека
            p = self.points.pop_last()
            while t.is_light(self.points.last(), p):
                self._perimeter -= p.dist(self.points.last())
                self._area += abs(R2Point.area(t, p, self.points.last()))
                self.change_intersections(self.points.last(), p, 1)
                p = self.points.pop_last()
            self.points.push_last(p)

            # добавление двух новых рёбер
            self._perimeter += (t.dist(self.points.first()) +
                                t.dist(self.points.last()))
            try:
                from __main__ import rectangle
            except:
                rectangle = [
                    R2Point(0.0, 0.0),
                    R2Point(0.0, 1.0),
                    R2Point(1.0, 1.0),
                    R2Point(1.0, 0.0)
                ]
            self._intersections -= (self.points.first() in rectangle) + (self.points.last() in rectangle)
            self.change_intersections(self.points.first(), t)
            self.change_intersections(self.points.last(), t)
            self.points.push_first(t)

        return self


if __name__ == "__main__":  # pragma: no cover
    f = Void()
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(1.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 1.0))
    print(type(f), f.__dict__)
