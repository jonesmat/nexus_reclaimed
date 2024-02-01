import ppb


class Player(ppb.Sprite):
    pass


def setup(scene):
    scene.add(Player())


ppb.run(setup=setup)