from typing import List, Optional, Type
from ppb import Sprite, Vector, events, Scene
from data_structs.quad_tree import QuadTree
from data_structs.shapes import Rectangle
from entities.boundary import Boundary
from entities.grass import Grass
from world_tile import WorldTile


class WorldScene(Scene):

    def __init__(self, player_sprite: Type[Sprite], starting_map_tile_path: str, **kwargs):
        super().__init__(**kwargs)

        self.player_sprite = player_sprite

        self.world_width = 1000
        self.world_height = 1000
        world_boundary = Rectangle(0, 0, self.world_width, self.world_height)
        self.quadtree = QuadTree(world_boundary, capacity=10)
        self.last_scene_entity_update_player_position = Vector(-1000, -1000)

        self.current_tile = WorldTile(starting_map_tile_path, tile_orientation="NORTH")
        self.player = self.current_tile.load_player_sprite(self.player_sprite)
        self.add(self.player)

        self.quadtree.add(self.current_tile.load_tile_sprites())

    def on_update(self, event: events.Update, signal):
        self._update_scene_entities()

    def _update_scene_entities(self):
        camera_width = self.main_camera.width
        camera_height = self.main_camera.height
        view_distance = (float(max(camera_width, camera_height)) * 1.5) / 2

        if (self.player.position - self.last_scene_entity_update_player_position).length <= (view_distance / 10):
            # The player hasn't moved far enough to recheck which entities should be rendered.
            return

        visible_sprites = []

        view_range = Rectangle(
            self.player.position.x - view_distance,
            self.player.position.y - view_distance,
            view_distance * 2,
            view_distance * 2,
        )
        self.quadtree.query(view_range, visible_sprites)

        for child in self.children:
            if type(child) not in [Grass, Boundary]:
                continue

            if child not in visible_sprites:
                self.remove(child)

        for visible_sprite in visible_sprites:
            if visible_sprite not in self.children:
                self.add(visible_sprite)

        self.last_scene_entity_update_player_position = self.player.position
