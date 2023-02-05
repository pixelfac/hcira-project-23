class Point:
    def init(self, x, y):
        self.x = x
        self.y = y
        self.coords = [x,y]

class Unistroke:
    def init(self, label, points ):
        #label: String
        #args = points: Point
        self.label = label
        self.points = points