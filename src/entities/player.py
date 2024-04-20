import ppb
import ppb.buttons
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

    def move_to_target_position(self, time_delta: float):
        speed_tick = self.speed * time_delta
        position_delta = self.target_position - self.position
        self.position += position_delta.truncate(speed_tick)

    def on_button_pressed(self, event: ppb.events.ButtonPressed, signal):
        if event.button is ppb.buttons.Primary:
            self.target_position = event.position
