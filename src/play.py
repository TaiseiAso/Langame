# coding: utf-8


import pygame
from pygame.locals import *
from .manager import SCENE_ID
from .utils import *


class Play:
    def __init__(self, screen, sceneManager, imageDict, ai, font_path):
        self.screen = screen
        self.sceneManager = sceneManager
        self.imageDict = imageDict
        self.ai = ai

        self.me = Me(imageDict)
        self.init()

    def init(self):
        self.me.init()
        self.me.pos = [400,450]
        self.me.state = State.GOODBY
        self.me.size_ratio = 3

    def update(self, message):
        self.me.update()

    def draw(self):
        self.me.draw(self.screen)
