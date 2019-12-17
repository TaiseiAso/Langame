# coding: utf-8


import pygame
from pygame.locals import *
from ai import AI
from src import *
import yaml
import sys


class Game:
    def __init__(self, name, size, fps):
        data_config = yaml.load(stream=open("config/data_config.yml", 'rt', encoding='utf-8'), Loader=yaml.SafeLoader)
        data_path = data_config['path']

        pygame.init()
        pygame.display.set_mode(size, 0, 32)
        pygame.display.set_caption(name)
        self.screen = pygame.display.get_surface()

        self.sceneManager = SceneManager(SCENE_ID.TITLE, 40)
        self.imageDict = self.loadImage(data_path['img'])

        self.key = Key()
        self.user = User(self.imageDict, self.key, data_path['font'], data_path['romaji'], 20, 32)
        self.ai = AI("config/ai_config.yml")
        self.ai.prepare_test()

        self.fps = fps

        title = Title(self.screen, self.sceneManager, self.imageDict, self.ai, data_path['font'], data_path['text'])
        play = Play(self.screen, self.sceneManager, self.imageDict, self.ai, data_path['font'], data_path['pattern'], data_path['synonym'])
        self.scenes = {SCENE_ID.TITLE:title, SCENE_ID.PLAY:play}

    def loadImage(self, img_path):
        imageDict = {}
        imageDict['title'] = pygame.image.load(img_path + "title.png")
        imageDict['chara'] = pygame.image.load(img_path + "chara.png")
        imageDict['window'] = pygame.image.load(img_path + "window.png")
        imageDict['mapchip'] = pygame.image.load(img_path + "mapchip.png")
        imageDict['me'] = pygame.image.load(img_path + "me.png")
        return imageDict

    def update(self):
        self.key.update()
        message = self.user.type_message()
        self.scenes[self.sceneManager.scene_id].update(message)
        move_flag = self.sceneManager.update()
        if move_flag:
            self.scenes[self.sceneManager.scene_id].init()

    def draw(self):
        self.screen.fill((230,230,230))
        self.scenes[self.sceneManager.scene_id].draw()
        self.sceneManager.draw(self.screen)
        self.user.draw(self.screen)
        pygame.display.update()

    def wait(self):
        pygame.time.wait(int(1000 / self.fps))

    def play(self):
        while True:
            self.update()
            self.draw()
            self.wait()


if __name__ == "__main__":
    game = Game("LANGAME, Aso Taisei, 2019~", (800,600), 30)
    game.play()
