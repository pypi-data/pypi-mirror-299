from typing import Dict, Tuple
from turtle import Turtle

from math import inf, sqrt
from pyturtle.shapes.shape import Shape
from pyturtle.shapes.point import Point2D


class Line(Shape):
    def __init__(self, start, end, num_coordinates: int = 2):
        super().__init__(num_coordinates)
        if not isinstance(start, Point2D):
            self.start = Point2D(*start)
        else:
            self.start = start
        if not isinstance(end, Point2D):
            self.end = Point2D(*end)
        else:
            self.end = end

        self._set_properties()
        self.set_coordinates()

    def _set_properties(self):
        self._set_slope()
        self._set_intercept()
        self._set_length()

    def get_properties(self):
        return [self.slope, self.intercept, self.length]

    def _set_slope(self):
        """
        returns slope of a line
        """
        if not (self.end.x - self.start.x) == 0:
            self.slope = (self.end.y - self.start.y) / (self.end.x - self.start.x)
        else:
            self.slope = inf

    def get_slope(self):
        return self.slope

    def _set_intercept(self):
        """
        returns the intercept of the line
        y = mx+b
        """
        self.intercept = self.start.y - self.slope * self.start.x

    def get_intercept(self):
        return self.intercept

    def _set_length(self):
        """Calculate the length of the line segment."""
        self.length = sqrt(
            (self.end.x - self.start.x) ** 2 + (self.end.y - self.start.y) ** 2
        )

    def get_length(self):
        return self.length

    def set_coordinates(self):
        """Set the coordinates for the line based on num_coordinates."""
        if self.num_coordinates <= 2:
            self.coordinates = [self.start, self.end]  # At least one point
        else:
            step_x = (self.end.x - self.start.x) / (self.num_coordinates - 1)
            step_y = (self.end.y - self.start.y) / (self.num_coordinates - 1)

            self.coordinates = [
                Point2D(self.start.x + step_x * i, self.start.y + step_y * i)
                for i in range(self.num_coordinates)
            ]

    def change_end(self, end: Tuple[float, float]):
        """
        change the end point of the line while
        keeping start point the same.
        """
        self.end = Point2D(*end)
        self._set_properties()
        self.set_coordinates()

    def swap_start_end(self):
        """
        changes the start of the line to the previous end of the line.
        """
        temp = self.end
        self.end = self.start
        self.start = temp
        self._set_properties()
        self.set_coordinates()

    def translate_x(self, x):
        self.start.x += x
        self.end.x += x
        # update coordinates
        self._set_properties()
        self.set_coordinates()

    def translate_y(self, y):
        self.start.y += y
        self.end.y += y
        # update coordinates
        self._set_properties()
        self.set_coordinates()

    def translate_xy(self, x, y):
        self.start.x += x
        self.start.y += y
        self.end.x += x
        self.start.x += y
        self._set_properties()
        self.set_coordinates()

    def rotate(self):
        pass

    def get_slice(self):
        pass

    def get_random_slice(self):
        pass


class HorizontalLine(Line):
    def __init__(self, start: Tuple[float, float], length: float, num_coordinates=2):
        end = (start[0] + length, start[1])  # End point extends to the right
        super().__init__(start=start, end=end, num_coordinates=num_coordinates)

    def set_coordinates(self):
        """Set the coordinates for the horizontal line based on num_coordinates."""
        if self.num_coordinates <= 2:
            self.coordinates = [self.start, self.end]  # At least one point
            return

        step_x = self.get_length() / (self.num_coordinates - 1)
        self.coordinates = [
            Point2D(self.start.x + step_x * i, self.start.y)  # y remains constant
            for i in range(self.num_coordinates)
        ]


class VerticalLine(Line):
    def __init__(self, start: Tuple, length: float, num_coordinates=2):
        end = (0, start[1] + length)  # End point extends upward
        super().__init__(start=start, end=end, num_coordinates=num_coordinates)

    def set_coordinates(self):
        """Set the coordinates for the vertical line based on num_coordinates."""
        if self.num_coordinates <= 2:
            self.coordinates = [self.start, self.end]  # At least one point
            return

        step_y = (self.end.y - self.start.y) / (self.num_coordinates - 1)
        self.coordinates = [
            Point2D(self.start.x, self.start.y + step_y * i)  # x remains constant
            for i in range(self.num_coordinates)
        ]


class HorizontalLineStack:
    """
    going to try and implement this object using concepts from
    a linked list
    """

    def __init__(self):
        self.lines = []

    def is_empty(self):
        return self.lines == []

    def add(self, start, length, num_coordinates):
        new_line = HorizontalLine(start, length, num_coordinates)
        self.lines.append(new_line)

    def draw(self):
        for line in self.lines:
            line.draw()

    def clear(self):
        self.lines = []

    def get_lines(self):
        return self.lines

    def pop_line(self):
        return self.lines.pop()


class VerticalLineStack:
    """
    going to try and implement this object using concepts from
    a linked list
    """

    def __init__(self):
        self.lines = []

    def is_empty(self):
        return self.lines == []

    def add(self, start, length, num_coordinates):
        new_line = VerticalLine(start, length, num_coordinates)
        self.lines.append(new_line)

    def draw(self, turtle_instance):
        for line in self.lines:
            line.draw(turtle_instance)

    def clear(self):
        self.lines = []

    def get_lines(self):
        return self.lines

    def pop_line(self):
        return self.lines.pop()


if __name__ == "__main__":
    Line()
