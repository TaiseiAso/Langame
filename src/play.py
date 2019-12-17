# coding: utf-8


import pygame
from pygame.locals import *
import random
from .manager import SCENE_ID
from .utils import *


class Stage:
    def __init__(self, imageDict):
        self.imageDict = imageDict
        self.size = 0

    def init(self, width, height, size):
        self.width = width
        self.height = height
        if size != self.size:
            self.size = size
            self.make_chip()

        self.block_x = width//size + 1
        self.block_y = height//size

        self.recreate()

    def make_chip(self):
        wall = pygame.Surface((64,64))
        wall.blit(self.imageDict['mapchip'], (0,0), (0,0,64,64))
        self.wall = pygame.transform.scale(wall, (self.size,self.size))

        ground = pygame.Surface((64,64))
        ground.blit(self.imageDict['mapchip'], (0,0), (64,0,64,64))
        self.ground = pygame.transform.scale(ground, (self.size,self.size))

        bridge = pygame.Surface((64,64), SRCALPHA)
        bridge.blit(self.imageDict['mapchip'], (0,0), (0,64,64,64))
        self.bridge = pygame.transform.scale(bridge, (self.size,self.size))

        ladder = pygame.Surface((64,64), SRCALPHA)
        ladder.blit(self.imageDict['mapchip'], (0,0), (64,64,64,64))
        self.ladder = pygame.transform.scale(ladder, (self.size,self.size))

    def recreate(self):
        self.Dx = 0
        self.delete_count = 0

        self.map = []
        self.first_create()
        self.create()

    def first_create(self):
        for x in range(self.block_x):
            self.map.append([0]*(self.block_y-3) + [2,1,1,1])

    def create(self):
        for x in range(self.block_x):
            r = random.randint(0, 2)
            self.map.append([0]*(self.block_y-(3+r)) + [2] + [1]*(3+r))

    def collider(self, me):
        pass

    def update(self, over_x):
        while over_x >= self.size:
            self.map = self.map[1:]
            over_x -= self.size
            self.delete_count += 1
            if self.delete_count == self.block_x:
                self.delete_count = 0
                self.create()
        self.Dx = over_x

    def draw(self, screen):
        for x, col in enumerate(self.map):
            pos_x = self.size*x - self.Dx
            if pos_x > self.width:
                continue
            for y, block in enumerate(col):
                pos_y = self.size*y
                if block == 1:
                    screen.blit(self.wall, (pos_x,pos_y))
                elif block == 2:
                    screen.blit(self.ground, (pos_x,pos_y))


class Play:
    def __init__(self, screen, sceneManager, imageDict, ai, font_path, pattern_path, synonym_path):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        self.sceneManager = sceneManager
        self.imageDict = imageDict
        self.ai = ai

        self.match = Match(pattern_path, synonym_path)

        self.back = Back(font_path, 15, self.height)
        self.balloon = Balloon(imageDict, font_path, 3)
        self.balloon.init(3, [0,0], 24)

        self.stage = Stage(imageDict)
        self.me = Me(imageDict)

        self.block_size = 64
        self.line = self.width//2

    def init(self):
        self.back.init()
        self.stage.init(self.width, self.height, self.block_size)
        self.me.init(State.STOP, 1, [160,384], Vec.NONE, 5)

        self.pop_message_time = 0

    def action(self, message):
        action_id = self.match.judge_action(message)
        response = None

        if action_id == -1:
            response = self.ai.test(message)
        elif action_id == 0:
            self.me.stop()
            response = "とまるよ"
        elif action_id == 3:
            self.me.go(Vec.RIGHT)
            response = "れっつごー！"
        elif action_id == 6:
            self.me.go(Vec.LEFT)
            response = "もどるよ"

        return response

    def update(self, message=None):
        self.back.update()
        self.balloon.update()

        if message is not None:
            response = self.action(message)
            if response is not None:
                self.balloon.set_message([response])
                self.pop_message_time = 100
        self.me.update()

        self.stage.collider(self.me)

        over, arranged_over = self.me.arrange_pos(self.line, self.block_size)
        self.stage.update(over)

        if self.pop_message_time > 0:
            self.pop_message_time -= 1
            self.balloon.pos = [
                self.me.pos[0]-arranged_over,
                self.me.pos[1]-118*self.me.size_ratio]

    def draw(self):
        self.back.draw(self.screen)
        self.stage.draw(self.screen)
        self.me.draw(self.screen)
        if self.pop_message_time > 0:
            self.balloon.draw(self.screen)
