from typing import List, Type
from ppb import Sprite
from PIL import Image
from entities.boundary import Boundary
from entities.grass import Grass

WORLD_GEN_COLORS = {
    "PLAYER": (0, 0, 255),  # BLUE
    "GRASS": (0, 255, 0),  # GREEN
    "BOUNDARY": (0, 0, 0),  # BLACK
}

TILE_ORIENTATION_ROTATION_ANGLE = {"NORTH": 0, "EAST": 90, "SOUTH": 180, "WEST": -90}


class WorldTile:
    """Handle"""

    def __init__(self, tile_image_path: str, **kwargs):

        self._tile_image_path = tile_image_path
        self.tile_orientation = kwargs.get("tile_orientation", "NORTH")

    def load_player_sprite(self, player_sprite: Type[Sprite]) -> Sprite:
        with Image.open(self._tile_image_path) as img:

            rotation_angle = TILE_ORIENTATION_ROTATION_ANGLE.get(self.tile_orientation, 0)
            rotated_img = img.rotate(rotation_angle, expand=True)

            pixels = rotated_img.load()
            if not pixels:
                raise RuntimeError()

            width, height = rotated_img.size

            for y in range(height):
                for x in range(width):
                    color = pixels[x, y]

                    if color[:3] == WORLD_GEN_COLORS["PLAYER"]:
                        return player_sprite(position=(x, y))

            # Unable to find the player pixel in the image
            raise RuntimeError("Unable to find the player position")

    def load_tile_sprites(self) -> List[Sprite]:
        sprites: List[Sprite] = []

        with Image.open(self._tile_image_path) as img:
            rotation_angle = TILE_ORIENTATION_ROTATION_ANGLE.get(self.tile_orientation, 0)
            rotated_img = img.rotate(rotation_angle, expand=True)

            pixels = rotated_img.load()
            if not pixels:
                raise RuntimeError()

            width, height = rotated_img.size

            for y in range(height):
                for x in range(width):
                    color = pixels[x, y]

                    if color[3] == 0:  # TRANSPARENT
                        pass

                    elif color[:3] == WORLD_GEN_COLORS["GRASS"]:
                        entity = Grass(position=(x, y))
                        sprites.append(entity)

                    elif color[:3] == WORLD_GEN_COLORS["BOUNDARY"]:
                        entity = Boundary(position=(x, y))
                        sprites.append(entity)

        return sprites
