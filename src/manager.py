# coding: utf-8


class SceneManager:
    def __init__(self, screen, move_scene_interval):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        self.move_scene_interval = move_scene_interval
        self.scene_id = 0
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

    def draw(self):
        if self.move_scene_time > 0:
            d = self.width*self.move_scene_time//self.move_scene_interval
            left = max(0, d - self.width)
            right = min(self.width, d)
            self.screen.fill((20,20,20), (left, 0, right - left, self.height))
