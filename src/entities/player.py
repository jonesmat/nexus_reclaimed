from typing import Optional, Type
import ppb
import ppb.buttons
import ppb.sprites
from ppb.sprites import BaseSprite
from ppb.scenes import Scene
import math

from ppb_vector import Vector

from entities.boundary import Boundary


class Player(ppb.Sprite):
    image = ppb.Image("images/player.bmp")
    layer = 10

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.speed = 5  # GU (game units) per second
        self.target_position = self.position

        self.primary_button_held_down = False

    def on_update(self, update: ppb.events.Update, signal):
        if self.position != self.target_position:
            prev_position = self.position
            self.position = self._determine_next_position(update.time_delta)

            if self._is_touching_entity(update.scene, Boundary):
                # Collided with a boundary, reset the position and clear the target.
                self.position = prev_position
                self.target_position = self.position
                return

        if update.scene.main_camera.center != self.position:
            update.scene.main_camera.center = self.position

    def _is_touching_entity(
        self, scene: Scene, entity_type: Type[BaseSprite]
    ) -> Optional[BaseSprite]:
        for entity in scene.get(kind=entity_type):
            if not (
                self.left >= entity.right
                or self.right <= entity.left
                or self.top <= entity.bottom
                or self.bottom >= entity.top
            ):
                return entity

        return None

    def _determine_next_position(self, time_delta: float) -> Vector:
        speed_tick = self.speed * time_delta
        position_delta = self.target_position - self.position
        return self.position + position_delta.truncate(speed_tick)

    def on_button_pressed(self, event: ppb.events.ButtonPressed, signal):
        if event.button is ppb.buttons.Primary:
            self.primary_button_held_down = True
            self.target_position = event.position

    def on_mouse_motion(self, event: ppb.events.MouseMotion, signal):
        if self.primary_button_held_down:
            self.target_position = event.position

    def on_button_released(self, event: ppb.events.ButtonPressed, signal):
        if event.button is ppb.buttons.Primary:
            self.primary_button_held_down = False
