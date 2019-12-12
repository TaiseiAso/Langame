# coding: utf-8


import pygame
from pygame.locals import *
import sys


class Key:
    def __init__(self):
        self.press = []
        self.update()

    def update(self):
        self.push = []
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                self.press.append(event.key)
                self.push.append(event.key)
            elif event.type == KEYUP:
                if event.key in self.press:
                    self.press.remove(event.key)
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
