import ppb

from src.entities.player import Player

class Game(ppb.Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add(Player())
