import math
from turtle import Turtle

from pyturtle.shapes.point import Point2D
from pyturtle.shapes.shape import Shape
from pyturtle.shapes.line import Line


class Triangle(Shape):
    def __init__(
        self,
        center=None,
        base_length=None,
        height=None,
        orientation=None,
        vertex1=None,
        vertex2=None,
        vertex3=None,
        num_coordinates=0,
    ):
        self.num_coordinates = num_coordinates // 3  # number of coordinates to retrieve

        if vertex1 is not None and vertex2 is not None and vertex3 is not None:
            # Initialize with three vertices
            self.vertices = [Point2D(*vertex1), Point2D(*vertex2), Point2D(*vertex3)]
            self._set_sides()  # set properties uses set_sides
            self._set_properties()
        elif (
            center is not None
            and base_length is not None
            and height is not None
            and orientation is not None
        ):
            # Initialize using center, base length, height, and orientation
            self.base_length = base_length
            self.height = height
            self.orientation = orientation
            self.center = Point2D(*center)
            self._set_vertices()  # Set the vertices based on other parameters
            self._set_sides()  # set the sides based on the vertices
        else:
            raise ValueError(
                "Invalid parameters. Provide either three vertices or center, base_length, height, and orientation."
            )
        self.set_coordinates()

    ##
    ## vertices
    ##

    def _set_vertices(self):
        cx, cy = self.center.x, self.center.y
        half_base = self.base_length / 2
        height = self.height

        # Calculate the vertices
        vertex1 = (cx - half_base, cy - (height / 2))  # Left vertex
        vertex2 = (cx + half_base, cy - (height / 2))  # Right vertex
        vertex3 = (cx, cy + (height / 2))  # Top vertex

        # Calculate the x and y vertex offsets based on orientation
        angle_rad = math.radians(self.orientation)

        # Rotate vertices around the center
        vertices = [vertex1, vertex2, vertex3]
        rotated_vertices = []

        for x, y in vertices:
            # Translate to origin
            x -= cx
            y -= cy

            # Rotate
            new_x = x * math.cos(angle_rad) - y * math.sin(angle_rad)
            new_y = x * math.sin(angle_rad) + y * math.cos(angle_rad)

            # Translate back
            rotated_vertices.append(Point2D(new_x + cx, new_y + cy))

        self.vertices = rotated_vertices

    def get_vertices(self):
        return self.vertices

    ##
    ## sides
    ##

    def _set_sides(self):
        self.sides = [
            Line(
                self.vertices[0], self.vertices[1], num_coordinates=self.num_coordinates
            ),
            Line(
                self.vertices[1], self.vertices[2], num_coordinates=self.num_coordinates
            ),
            Line(
                self.vertices[2], self.vertices[0], num_coordinates=self.num_coordinates
            ),
        ]

    def get_sides(self):
        return self.sides

    ##
    ## properties
    ##

    def _set_properties(self):
        self._set_base_length()
        self._set_height()
        self._set_orientation()
        self._set_center()

    def get_properties(self):
        return [self.base_length, self.height, self.orientation, self.center]

    def _set_center(self):
        x_coords = [v.x for v in self.vertices]
        y_coords = [v.y for v in self.vertices]
        centroid_x = sum(x_coords) / 3
        centroid_y = sum(y_coords) / 3
        self.center = Point2D(centroid_x, centroid_y)

    def _set_base_length(self):
        self.base_length = self.sides[0].get_length()

    def get_base_length(self):
        return self.base_length

    def _set_height(self):
        one = self.vertices[0]
        two = self.vertices[1]
        three = self.vertices[2]

        area = abs(
            one.x * (two.y - three.y)
            + two.x * (three.y - one.y)
            + three.x * (one.y - two.y)
        )
        self.height = (2 * area) / self.base_length

    def get_height(self):
        return self.height

    def _set_orientation(self):
        one = self.vertices[0]
        two = self.vertices[1]

        self.orientation = math.degrees(math.atan2(two.y - one.y, two.x - one.x))

    def get_orientation(self):
        return self.orientation

    def get_center(self):
        return self.center

    ##
    ## other stuff
    ##

    def perimeter(self):
        return sum(side.get_length() for side in self.sides)

    def get_coordinates(self):
        """Get evenly spaced coordinates along the triangle's edges."""
        return self.coordinates

    def set_coordinates(self):
        """Set the number of coordinates to retrieve along the edges."""
        coordinates = []

        for side in self.sides:
            # side.set_coordinates()
            coordinates.extend(side.coordinates)
        self.coordinates = coordinates

    def draw(self, turtle_instance):
        for side in self.sides:
            side.draw(turtle_instance)

    def get_random_slice(self):
        pass

    def get_slice(self):
        pass

    # These modify the properties of the triangle.
    # Need to reset self.sides(), and other attributes

    def rotate(self, angle):
        """Rotate the triangle around its centroid."""
        new_vertices = []
        angle_rad = math.radians(angle)
        for vertice in self.vertices:
            # Translate each vertice so that the new center is (0, 0)
            # to perform rotation
            x, y = vertice.x, vertice.y
            x -= self.center.x
            y -= self.center.y

            # Rotate point
            new_x = x * math.cos(angle_rad) - y * math.sin(angle_rad)
            new_y = x * math.sin(angle_rad) + y * math.cos(angle_rad)

            # Translate point back so that center is original center
            new_vertices.append((new_x + self.center.x, new_y + self.center.y))

        self.vertices = new_vertices
        self._set_properties()
        self._set_sides()

    def translate_x(self, dx):
        vertices = self.get_vertices()
        new_vertices = []
        for vertice in self.vertices:
            new_vertices.append((vertice.x + dx, vertice.y))
        # update vertices and then recalc properties
        self.vertices = [Point2D(*v) for v in new_vertices]
        self._set_properties()
        self._set_sides()

    def translate_y(self, dy):
        vertices = self.get_vertices()
        new_vertices = []
        for vertice in vertices:
            new_vertices.append((vertice.x, vertice.y + dy))
        # update vertices and then recalc properties
        self.vertices = [Point2D(*v) for v in new_vertices]
        self._set_properties()
        self._set_sides()

    def translate_xy(self, dx, dy):
        self.translate_x(dx)
        self.translate_y(dy)
