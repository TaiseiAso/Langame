# coding: utf-8


import pygame
import sys
import random
from .utils import *


class Title:
    def __init__(self, screen, sceneManager, imageDict, ai, font_path, text_path):
        self.screen = screen
        self.sceneManager = sceneManager
        self.imageDict = imageDict
        self.back = Back(screen, font_path, 15)
        self.balloon = Balloon(screen, imageDict, font_path, 3)
        self.balloon.set_parameter(vec=4, size=24, pos=[380,266])
        self.ai = ai

        self.title_text = self.load_text(text_path + "title.txt")
        self.start_text = self.load_text(text_path + "start.txt")
        self.end_text = self.load_text(text_path + "end.txt")

        self.interval = 150
        self.init()

    def init(self):
        self.t = 0
        self.wait_time = 0
        self.flag = 0
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

    def update(self, message):
        self.back.update()

        if self.wait_time == 0:
            if self.flag == 1:
                self.sceneManager.move_scene(0)
            elif self.flag == 2:
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
                        self.flag = 1
                    elif message == "おわる":
                        self.balloon.set_message(random.choice(self.end_text))
                        self.wait_time = 60
                        self.flag = 2
                    else:
                        res = self.ai.test(message)
                        self.balloon.set_message([res])
                        self.t = 0

    def draw(self):
        self.back.draw()
        self.screen.blit(self.imageDict['title'], (90,50))
        self.screen.blit(self.imageDict['chara'], (80,200))
        self.balloon.draw()
