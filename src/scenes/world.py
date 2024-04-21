from typing import List, Optional, Type
import ppb
from PIL import Image

from entities.boundary import Boundary
from entities.grass import Grass


class WorldScene(ppb.Scene):

    def __init__(
        self, player_sprite: Type[ppb.Sprite], starting_map_tile_path: str, **kwargs
    ):
        super().__init__(**kwargs)

        self.player_sprite = player_sprite
        self.player: Optional[ppb.Sprite] = None

        self.offscreen_chunking_distance = 0
        self.last_chuck_update_player_position = ppb.Vector(-1000, -1000)
        self.offscreen_sprites: List[ppb.Sprite] = []

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

            for y in range(height):
                for x in range(width):
                    color = pixels[x, y]

                    if color[3] == 0:  # TRANSPARENT
                        pass

                    elif (
                        color[:3] == WorldScene.WORLD_GEN_COLORS["PLAYER"]
                        and not self.player
                    ):
                        self.player = self.player_sprite(position=(x, y))
                        self.add(self.player)

                    elif color[:3] == WorldScene.WORLD_GEN_COLORS["GRASS"]:
                        entity = Grass(position=(x, y))
                        self.offscreen_sprites.append(entity)

                    elif color[:3] == WorldScene.WORLD_GEN_COLORS["BOUNDARY"]:
                        entity = Boundary(position=(x, y))
                        self.offscreen_sprites.append(entity)

    def on_update(self, event: ppb.events.Update, signal):
        self.offscreen_chunking_distance = (
            float(max(self.main_camera.width, self.main_camera.height)) * 1.2
        )
        self._process_chunking()

    def _process_chunking(self):
        if self.player and (
            self.player.position - self.last_chuck_update_player_position
        ).length > (self.offscreen_chunking_distance / 2):
            self.last_chuck_update_player_position = self.player.position
            self._chunk_load_offscreen_sprites()
            self._chunk_unload_offscreen_sprites()

    def _chunk_load_offscreen_sprites(self):
        # Check for "offscreen" sprites that need to be added to the scene.
        sprites_remaining_offscreen: List[ppb.Sprite] = []
        for sprite in self.offscreen_sprites:
            if (
                self.player
                and (sprite.position - self.player.position).length
                <= self.offscreen_chunking_distance
            ):
                self.add(sprite)
            else:
                sprites_remaining_offscreen.append(sprite)

        self.offscreen_sprites = sprites_remaining_offscreen

    def _chunk_unload_offscreen_sprites(self):
        # Check for "onscreen" sprites in the scene that need to be moved "offscreen".
        for child in self.children:
            if type(child) not in [Grass, Boundary]:
                continue

            if (
                child.position - self.player.position  # type: ignore
            ).length > self.offscreen_chunking_distance:
                self.remove(child)
                self.offscreen_sprites.append(child)  # type: ignore
