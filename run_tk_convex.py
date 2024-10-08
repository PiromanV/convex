#!/usr/bin/env -S python3 -B
from tk_drawer import TkDrawer
from r2point import R2Point
from convex import Void, Point, Segment, Polygon


def void_draw(self, tk):
    pass


def point_draw(self, tk):
    tk.draw_point(self.p)


def segment_draw(self, tk):
    tk.draw_line(self.p, self.q)


def polygon_draw(self, tk):
    for n in range(self.points.size()):
        tk.draw_line(self.points.last(), self.points.first())
        self.points.push_last(self.points.pop_first())


setattr(Void, 'draw', void_draw)
setattr(Point, 'draw', point_draw)
setattr(Segment, 'draw', segment_draw)
setattr(Polygon, 'draw', polygon_draw)


tk = TkDrawer()
f = Void()
tk.clean()

try:
    a = R2Point()
    c = R2Point()
    rectangle = [R2Point(min(a.x, c.x), min(a.y, c.y)),
                 R2Point(min(a.x, c.x), max(a.y, c.y)),
                 R2Point(max(a.x, c.x), max(a.y, c.y)),
                 R2Point(max(a.x, c.x), min(a.y, c.y))]
    rectangle_polygon = Polygon(rectangle[0], rectangle[1], rectangle[2])
    rectangle_polygon.add(rectangle[3])
    rectangle_polygon.draw(tk)
    while True:
        f = f.add(R2Point())
        tk.clean()
        rectangle_polygon.draw(tk)
        f.draw(tk)
        print(
                f"S = {f.area()},",
                f"P = {f.perimeter()},",
                f"N = {f.intersections()}\n"
            )
except (EOFError, KeyboardInterrupt):
    print("\nStop")
    tk.close()
