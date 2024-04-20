import ppb

from entities.player import Player
from scenes.world import WorldScene


ppb.run(
    starting_scene=WorldScene,
    title="Nexus Reclaimed",
    scene_kwargs={
        "player_sprite": Player,
        "starting_map_tile_path": "images/map/starting_tile_1.bmp",
    },
)
