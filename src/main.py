import ppb

from entities.player import Player


class Game(ppb.Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add(Player())


ppb.run(starting_scene=Game)
