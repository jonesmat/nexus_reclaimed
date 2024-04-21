from ppb import Sprite
from src.data_structs.quad_tree import QuadTree
from src.data_structs.shapes import Rectangle


def test_add_sprite():
    boundary = Rectangle(0, 0, 100, 100)
    qt = QuadTree(boundary, 4)
    sprite = Sprite(position=(10, 10), size=10)
    qt.add(sprite)
    assert len(qt.sprites) == 1


def test_query_sprite():
    boundary = Rectangle(0, 0, 100, 100)
    qt = QuadTree(boundary, 4)
    sprite = Sprite(position=(10, 10), size=10)
    qt.add([sprite])
    found = []
    qt.query(Rectangle(5, 5, 20, 20), found)
    assert sprite in found


def test_add_til_split():
    boundary = Rectangle(0, 0, 20, 20)
    qt = QuadTree(boundary, 4)

    # Place sprites in what should become the northwest quadrant after a division.
    qt.add(Sprite(position=(2, 18), size=10))
    qt.add(Sprite(position=(2, 12), size=10))
    qt.add(Sprite(position=(8, 18), size=10))
    qt.add(Sprite(position=(8, 12), size=10))

    # Place a sprite in what should become the southwest quadrant that will trigger the division.
    qt.add(Sprite(position=(5, 5), size=10))

    assert len(qt.children) == 4
    assert len(qt.northwest.sprites) == 4
    assert len(qt.southwest.sprites) == 1


def test_add_til_double_split():
    boundary = Rectangle(0, 0, 20, 20)
    qt = QuadTree(boundary, 4)

    # Place sprites in what should become the southwest quadrant after a division.
    qt.add(Sprite(position=(1, 1), size=10))  # southwest -> southwest
    qt.add(Sprite(position=(1, 4), size=10))  # southwest -> northwest
    qt.add(Sprite(position=(4, 1), size=10))  # southwest -> southeast
    qt.add(Sprite(position=(4, 4), size=10))  # southwest -> northeast

    qt.add(Sprite(position=(8, 8), size=10))

    assert len(qt.children) == 4
    assert len(qt.southwest.sprites) == 0
    assert len(qt.southwest.children) == 4
    assert len(qt.southwest.southwest.sprites) == 4
    assert len(qt.southwest.northwest.sprites) == 0
    assert len(qt.southwest.southeast.sprites) == 0
    assert len(qt.southwest.northeast.sprites) == 1


def test_remove_sprite():
    boundary = Rectangle(0, 0, 10, 10)
    qt = QuadTree(boundary, 4)
    sprite = Sprite(position=(1, 1), size=10)

    qt.add([sprite])
    qt.remove([sprite])

    assert len(qt.sprites) == 0


def test_remove_sprite_deep():
    boundary = Rectangle(0, 0, 10, 10)
    qt = QuadTree(boundary, 4)
    sprite = Sprite(position=(1, 1), size=10)

    qt.add([sprite])
    qt.subdivide()  # Force subdivision to occur
    qt.remove([sprite])

    assert len(qt.sprites) == 0
    assert len(qt.southwest.sprites) == 0


def test_cleanup():
    boundary = Rectangle(0, 0, 100, 100)
    qt = QuadTree(boundary, 1)
    sprite = Sprite(position=(50, 50), size=5)

    qt.add([sprite])
    qt.subdivide()  # Force subdivision to occur
    qt.remove([sprite])
    qt.cleanup()

    assert qt.divided == False
    assert qt.children == []
