"""
Project 1 for HCIRA, Spring '23

Group Members :
Aravind S
Nathan Harris
Shashanka Bhat

Description:
This file contains the dataclasses and initialization
for the template gestures
"""

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.coords = [x,y]

class Unistroke:
    def __init__(self, label, points):
        #label: String
        #args = points: Point
        self.label = label
        self.points = []
        for pt in points:
            self.points.append(pt.coords)

