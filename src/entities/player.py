import ppb  # type: ignore
import math


class Player(ppb.Sprite):
    image = ppb.Image("images/player.bmp")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.speed = 5  # GU (game units) per second
        self.target_position = self.position

    def on_update(self, update: ppb.events.Update, signal):
        if self.position != self.target_position:
            self.move_to_target_position(update.time_delta)

        update.scene.main_camera.center = self.position

    def on_button_pressed(self, event: ppb.events.ButtonPressed, signal):
        print(f"Player: on_button_pressed: {type(event.button)} - {event.position}")

        self.target_position = event.position

    def move_to_target_position2(self, time_delta: float):
        speed_tick = self.speed * time_delta
        distance_to_target = math.dist(self.position, self.target_position)
        move_ratio = min(speed_tick / distance_to_target, 1.0)

        full_position_delta = self.target_position - self.position
        position_delta = full_position_delta * move_ratio
        self.position += position_delta

    def move_to_target_position(self, time_delta: float):
        speed_tick = self.speed * time_delta
        position_delta = self.target_position - self.position
        self.position += position_delta.truncate(speed_tick)
