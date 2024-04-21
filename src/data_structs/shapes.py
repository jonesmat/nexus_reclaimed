from ppb import Vector


class Rectangle:
    def __init__(self, x, y, width, height):
        # The x, y position represents the bottom-left corner of the rectangle (this matches ppb's x, y axis)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def center(self):
        return Vector(self.x + self.width / 2, self.y + self.height / 2)

    def contains(self, point):
        """Check if the rectangle contains a point."""
        return self.x <= point.x < self.x + self.width and self.y <= point.y < self.y + self.height

    def intersects(self, other):
        """Check if this rectangle intersects with another rectangle."""
        return (
            self.x < other.x + other.width
            and self.x + self.width > other.x
            and self.y < other.y + other.height
            and self.y + self.height > other.y
        )

    def __repr__(self):
        return f"(x={self.x}, y={self.y}, width={self.width}, height={self.height})"
