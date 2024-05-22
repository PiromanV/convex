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
        self._intersections = R2Point.count_points_intersect(p, p)

    def intersections(self):
        return self._intersections

    def add(self, q):
        return self if self.p == q else Segment(self.p, q)


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q):
        self.p, self.q = p, q
        if R2Point.count_points_intersect(p, q) is inf:
            self._inf_intersections = 1
            self._intersections = 2
        else:
            self._inf_intersections = 0
            self._intersections = R2Point.count_points_intersect(p, q)

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def intersections(self):
        if self._inf_intersections:
            return inf
        else:
            return self._intersections

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            return Polygon(self.p, self.q, r)
        elif r.is_inside(self.p, self.q):
            return self
        elif self.p.is_inside(r, self.q):
            return Segment(r, self.q)
        else:
            return Segment(self.p, r)


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
        self._inf_intersections = 0
        self._intersections = 0
        if R2Point.count_points_intersect(a, b) is inf:
            self._inf_intersections += 1
            self._inf_intersections += 1
        if R2Point.count_points_intersect(b, c) is inf:
            self._inf_intersections += 1
            self._inf_intersections += 1
        if R2Point.count_points_intersect(c, a) is inf:
            self._inf_intersections += 1
            self._inf_intersections += 1
        if not self._inf_intersections:
            self._intersections = (R2Point.count_points_intersect(a, b) +
                                   R2Point.count_points_intersect(b, c) +
                                   R2Point.count_points_intersect(c, a))
        self._perimeter = a.dist(b) + b.dist(c) + c.dist(a)
        self._area = abs(R2Point.area(a, b, c))

    def perimeter(self):
        return self._perimeter

    def intersections(self):
        if self._inf_intersections:
            return inf
        else:
            return self._intersections

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
            if R2Point.count_points_intersect(self.points.first(), self.points.last()) is inf:
                self._inf_intersections -= 1
            else:
                self._intersections -= R2Point.count_points_intersect(self.points.first(), self.points.last())
            self._perimeter -= self.points.first().dist(self.points.last())
            self._area += abs(R2Point.area(t,
                                           self.points.last(),
                                           self.points.first()))

            # удаление освещённых рёбер из начала дека
            p = self.points.pop_first()
            while t.is_light(p, self.points.first()):
                if R2Point.count_points_intersect(self.points.first(), p) is inf:
                    self._inf_intersections -= 1
                    self._intersections -= 1
                else:
                    self._intersections -= R2Point.count_points_intersect(self.points.first(), p)
                self._perimeter -= p.dist(self.points.first())
                self._area += abs(R2Point.area(t, p, self.points.first()))
                p = self.points.pop_first()
            self.points.push_first(p)

            # удаление освещённых рёбер из конца дека
            p = self.points.pop_last()
            while t.is_light(self.points.last(), p):
                if R2Point.count_points_intersect(p, self.points.last()) is inf:
                    self._inf_intersections -= 1
                    self._intersections -= 1
                else:
                    self._intersections -= R2Point.count_points_intersect(p, self.points.last())
                self._perimeter -= p.dist(self.points.last())
                self._area += abs(R2Point.area(t, p, self.points.last()))
                p = self.points.pop_last()
            self.points.push_last(p)

            # добавление двух новых рёбер
            if R2Point.count_points_intersect(self.points.first(), t) is inf:
                self._inf_intersections += 1
                self._intersections += 1
            if R2Point.count_points_intersect(t, self.points.last()) is inf:
                self._inf_intersections += 1
                self._intersections += 1
            if (R2Point.count_points_intersect(t, self.points.last()) is not inf and
                    R2Point.count_points_intersect(self.points.first(), t) is not inf):
                self._intersections += (R2Point.count_points_intersect(self.points.first(), t) +
                                        R2Point.count_points_intersect(t, self.points.last()))
            self._perimeter += (t.dist(self.points.first()) +
                                t.dist(self.points.last()))
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
