from typing import Type
import ppb

from entities.grass import Grass  # type: ignore


class WorldScene(ppb.Scene):
    def __init__(self, player_sprite: Type[ppb.Sprite], **kwargs):
        super().__init__(**kwargs)

        self.add(player_sprite())

        self.add(Grass(position=(5, 5)))

    def on_update(self, event: ppb.events.Update, signal):
        pass
