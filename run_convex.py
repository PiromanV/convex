#!/usr/bin/env -S python3 -B
from r2point import R2Point
from convex import Void

f = Void()
try:
    a = R2Point()
    c = R2Point()
    rectangle = [R2Point(min(a.x, c.x), min(a.y, c.y)),
                 R2Point(min(a.x, c.x), max(a.y, c.y)),
                 R2Point(max(a.x, c.x), max(a.y, c.y)),
                 R2Point(max(a.x, c.x), min(a.y, c.y))]
    while True:
        f = f.add(R2Point())
        print(f"S = {f.area()}, P = {f.perimeter()}, N = {f.intersections()}\n")
        print()
except (EOFError, KeyboardInterrupt):
    print("\nStop")
