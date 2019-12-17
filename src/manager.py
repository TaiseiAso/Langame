# coding: utf-8


from enum import Enum


class SCENE_ID(Enum):
    TITLE = 0
    PLAY = 1


class SceneManager:
    def __init__(self, initial_scene, move_scene_interval):
        self.move_scene_interval = move_scene_interval
        self.scene_id = initial_scene
        self.move_scene_time = 0

    def move_scene(self, next_scene_id):
        if self.move_scene_time == 0:
            self.next_scene_id = next_scene_id
            self.move_scene_time = self.move_scene_interval*2

    def update(self):
        if self.move_scene_time > 0:
            self.move_scene_time -= 1
            if self.move_scene_time == self.move_scene_interval:
                self.scene_id = self.next_scene_id
                return True
        return False

    def draw(self, screen):
        if self.move_scene_time > 0:
            _, _, width, height = screen.get_rect()
            d = width*self.move_scene_time//self.move_scene_interval
            left = max(0, d - width)
            right = min(width, d)
            screen.fill((20,20,20), (left,0,right-left,height))
