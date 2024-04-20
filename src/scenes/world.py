from typing import Type
import ppb
from PIL import Image

from entities.boundary import Boundary
from entities.grass import Grass  # type: ignore


class WorldScene(ppb.Scene):
    def __init__(
        self, player_sprite: Type[ppb.Sprite], starting_map_tile_path: str, **kwargs
    ):
        super().__init__(**kwargs)

        self.player_sprite = player_sprite

        self._create_world_from_image(starting_map_tile_path)

    WORLD_GEN_COLORS = {
        "PLAYER": (0, 0, 255),  # BLUE
        "GRASS": (0, 255, 0),  # GREEN
        "BOUNDARY": (0, 0, 0),  # BLACK
    }

    def _create_world_from_image(self, image_path: str):
        with Image.open(image_path) as img:
            pixels = img.load()
            if not pixels:
                raise RuntimeError()

            width, height = img.size
            player_added = False

            for y in range(height):
                for x in range(width):
                    color = pixels[x, y]

                    if color[3] == 0:  # TRANSPARENT
                        pass

                    elif (
                        color[:3] == WorldScene.WORLD_GEN_COLORS["PLAYER"]
                        and not player_added
                    ):
                        self.add(self.player_sprite(position=(x, y)))
                        player_added = True

                    elif color[:3] == WorldScene.WORLD_GEN_COLORS["GRASS"]:
                        entity = Grass(position=(x, y))
                        self.add(entity)

                    elif color[:3] == WorldScene.WORLD_GEN_COLORS["BOUNDARY"]:
                        entity = Boundary(position=(x, y))
                        self.add(entity)

    def on_update(self, event: ppb.events.Update, signal):
        pass
