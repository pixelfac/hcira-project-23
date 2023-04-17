"""
Project 2 for HCIRA, Spring '23

Group Members :
Aravind S
Nathan Harris
Shashanka Bhat

Description:
This file contains the dataclasses and initialization
for the template gestures
"""


class Point:
    def __init__(self, x, y, strokeid):
        self.x = x
        self.y = y
        self.strokeId = strokeid
        self.coords = [x, y, strokeid]


class Multistroke:
    def __init__(self, label, points):
        # label: String
        # args = points: Point
        self.label = label
        self.points = []
        for pt in points:
            self.points.append(pt.coords)

