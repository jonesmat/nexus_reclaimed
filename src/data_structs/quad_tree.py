from data_structs.shapes import Rectangle


class SpriteOutOfBounds(Exception):
    pass


class QuadTree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary  # This defines the quadtree boundary
        self.capacity = capacity  # Max number of items before subdividing
        self.sprites = []  # Sprites within this quadtree
        self.divided = False
        self.children = []

    def subdivide(self):
        center_x, center_y = self.boundary.center.x, self.boundary.center.y
        w, h = self.boundary.width, self.boundary.height
        child_w = w / 2
        child_h = h / 2

        self.southwest = QuadTree(Rectangle(center_x - w / 2, center_y - h / 2, child_w, child_h), self.capacity)
        self.northwest = QuadTree(Rectangle(center_x - w / 2, center_y, child_w, child_h), self.capacity)
        self.southeast = QuadTree(Rectangle(center_x, center_y - h / 2, child_w, child_h), self.capacity)
        self.northeast = QuadTree(Rectangle(center_x, center_y, child_w, child_h), self.capacity)

        self.children = [self.northeast, self.northwest, self.southeast, self.southwest]
        self.divided = True

        # Redistribute sprites into the new quadrants
        existing_sprites = self.sprites[:]
        self.sprites = []  # Clear current list
        self.add(existing_sprites)

    def add(self, sprites):
        if not isinstance(sprites, list):
            sprites = [sprites]  # Ensure sprites is a list for single sprite input
        for sprite in sprites:
            self._add_single(sprite)

    def _add_single(self, sprite) -> bool:
        if not self.boundary.contains(sprite.position):
            return False

        if not self.divided and len(self.sprites) < self.capacity:
            self.sprites.append(sprite)
            return True

        if not self.divided:
            self.subdivide()

        # Insert into appropriate quadrant
        for child in self.children:
            if child._add_single(sprite):
                return True

        # Failed to add sprite to this QuadTree, or one of it's children, this should never happen.
        raise SpriteOutOfBounds

    def remove(self, sprites):
        if not isinstance(sprites, list):
            sprites = [sprites]  # Ensure sprites is a list for single sprite input
        for sprite in sprites:
            self._remove_single(sprite)

    def _remove_single(self, sprite):
        if not self.boundary.contains(sprite.position):
            return False

        if sprite in self.sprites:
            self.sprites.remove(sprite)
            return True

        if self.divided:
            for child in self.children:
                if child._remove_single(sprite):
                    return True
        return False

    def query(self, range, found):
        if not self.boundary.intersects(range):
            return False

        for sprite in self.sprites:
            if range.contains(sprite.position):
                found.append(sprite)

        if self.divided:
            for child in self.children:
                child.query(range, found)

        return True

    def cleanup(self):
        if self.divided:
            # Recursively cleanup children first
            for child in self.children:
                child.cleanup()

            # Check if all children are now leaf nodes without sprites
            if all(not child.sprites and not child.divided for child in self.children):
                # Collapse the children
                self.children = []
                self.divided = False

    def __repr__(self, level=0):
        ret = "\t" * level + "QuadTree" + str(self.boundary) + "\n"

        for sprite in self.sprites:
            ret += "\t" * (level + 1) + "-> Sprite " + str(sprite.position) + "\n"

        if self.divided:
            ret += "\t" * (level + 1) + "SW " + self.southwest.__repr__(level + 1)
            ret += "\t" * (level + 1) + "NW " + self.northwest.__repr__(level + 1)
            ret += "\t" * (level + 1) + "SE " + self.southeast.__repr__(level + 1)
            ret += "\t" * (level + 1) + "NE " + self.northeast.__repr__(level + 1)

        return ret
