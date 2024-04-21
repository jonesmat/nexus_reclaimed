from typing import List, Optional, Type
from ppb import Sprite, Vector, events, Scene
from entities.boundary import Boundary
from entities.grass import Grass
from world_tile import WorldTile


class WorldScene(Scene):

    def __init__(self, player_sprite: Type[Sprite], starting_map_tile_path: str, **kwargs):
        super().__init__(**kwargs)

        self.player_sprite = player_sprite

        self.offscreen_chunking_distance = 0
        self.last_chuck_update_player_position = Vector(-1000, -1000)
        self.offscreen_sprites: List[Sprite] = []

        self.current_tile = WorldTile(starting_map_tile_path, tile_orientation="WEST")
        self.player = self.current_tile.load_player_sprite(self.player_sprite)
        self.add(self.player)

        self.offscreen_sprites.extend(self.current_tile.load_tile_sprites())

    def on_update(self, event: events.Update, signal):
        self.offscreen_chunking_distance = (float(max(self.main_camera.width, self.main_camera.height)) * 1.5) / 2
        self._process_chunking()

        print(f"Items being rendered: {len(self.children)}")

    def _process_chunking(self):
        if (self.player.position - self.last_chuck_update_player_position).length > (
            self.offscreen_chunking_distance / 10
        ):
            self.last_chuck_update_player_position = self.player.position
            self._chunk_load_offscreen_sprites()
            self._chunk_unload_offscreen_sprites()

    def _chunk_load_offscreen_sprites(self):
        # Check for "offscreen" sprites that need to be added to the scene.
        sprites_remaining_offscreen: List[Sprite] = []
        for sprite in self.offscreen_sprites:
            if (sprite.position - self.player.position).length <= self.offscreen_chunking_distance:
                self.add(sprite)
            else:
                sprites_remaining_offscreen.append(sprite)

        self.offscreen_sprites = sprites_remaining_offscreen

    def _chunk_unload_offscreen_sprites(self):
        # Check for "onscreen" sprites in the scene that need to be moved "offscreen".
        for child in self.children:
            if type(child) not in [Grass, Boundary]:
                continue

            if (child.position - self.player.position).length > self.offscreen_chunking_distance:  # type: ignore
                self.remove(child)
                self.offscreen_sprites.append(child)  # type: ignore
