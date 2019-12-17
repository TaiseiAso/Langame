# coding: utf-8


import pygame
import sys
import random
from enum import Enum
from .manager import SCENE_ID
from .utils import *


class Flag(Enum):
    WAIT = 0
    START = 1
    END = 2


class Title:
    def __init__(self, screen, sceneManager, imageDict, ai, font_path, text_path):
        self.screen = screen
        _, _, self.width, self.height = self.screen.get_rect()
        self.sceneManager = sceneManager
        self.imageDict = imageDict
        self.ai = ai

        self.back = Back(font_path, 15, self.height)

        self.balloon = Balloon(imageDict, font_path, 3)
        self.balloon.init(4, [max(310, self.width//2-10),max(230, self.height//2-20)], 24)

        self.me = Me(imageDict)
        self.me.init(State.STOP, 2, [self.width//2-160, self.height//2+140], Vec.NONE, 0)

        self.title_text = self.load_text(text_path + "title.txt")
        self.start_text = self.load_text(text_path + "start.txt")
        self.end_text = self.load_text(text_path + "end.txt")

        self.interval = 150
        self.init()

    def init(self):
        self.t = 0
        self.wait_time = 0
        self.flag = Flag.WAIT
        self.text_id = 0
        self.back.init()
        self.balloon.set_message(self.title_text[self.text_id])

    def load_text(self, text_file_path):
        text = []
        with open(text_file_path, 'r', encoding='utf-8') as f:
            line = f.readline()
            while line:
                line = line.strip()
                text.append(line.split('_'))
                line = f.readline()
        return text

    def update(self, message=None):
        self.back.update()
        self.me.update()

        if self.wait_time == 0:
            if self.flag == Flag.START:
                self.sceneManager.move_scene(SCENE_ID.PLAY)
            elif self.flag == Flag.END:
                pygame.quit()
                sys.exit()
        else:
            self.wait_time -= 1

        if self.sceneManager.move_scene_time == 0:
            self.balloon.update()

            if self.wait_time == 0:
                self.t += 1
                if self.t == self.interval:
                    self.t = 0
                    self.text_id += 1
                    if self.text_id == len(self.title_text):
                        self.text_id = 0
                    self.balloon.set_message(self.title_text[self.text_id])

                if message is not None:
                    if message == "はじめる":
                        self.balloon.set_message(random.choice(self.start_text))
                        self.wait_time = 60
                        self.flag = Flag.START
                        self.me.state = State.WALK
                        self.me.vec = Vec.RIGHT
                    elif message == "おわる":
                        self.balloon.set_message(random.choice(self.end_text))
                        self.wait_time = 60
                        self.flag = Flag.END
                        self.me.state = State.GOODBYE
                        self.me.vec = Vec.NONE
                    else:
                        res = self.ai.test(message)
                        self.balloon.set_message([res])
                        self.t = 0

    def draw(self):
        self.back.draw(self.screen)
        self.screen.blit(self.imageDict['title'], (max(0, (self.width - 620)//2), 50))
        self.me.draw(self.screen)
        self.balloon.draw(self.screen)
