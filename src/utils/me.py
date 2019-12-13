# coding: utf-8


import pygame
from pygame.locals import *
from enum import Enum


class State(Enum):
    STOP = 0
    WALK = 1
    GOODBY = 2


class Vec(Enum):
    LEFT = -1
    NONE = 0
    RIGHT = 1


class Me:
    def __init__(self, imageDict):
        self.imageDict = imageDict
        self.t = 0
        self.make_chip()
        self.init()

    def init(self):
        self.state = State.STOP
        self.size_ratio = 1
        self.pos = [100,100]
        self.vec = Vec.NONE

    def make_chip(self):
        self.left_head = pygame.Surface((42,30), SRCALPHA)
        self.left_head.blit(self.imageDict['me'], (0,0), (0,0,42,30))

        self.right_head = pygame.Surface((42,30), SRCALPHA)
        self.right_head.blit(self.imageDict['me'], (0,0), (48,0,42,30))

        self.body = pygame.Surface((87,79), SRCALPHA)
        self.body.blit(self.imageDict['me'], (0,0), (0,33,87,79))

        self.shadow = pygame.Surface((73,14), SRCALPHA)
        self.shadow.blit(self.imageDict['me'], (0,0), (0,114,73,14))

        self.hand = pygame.Surface((34,34), SRCALPHA)
        self.hand.blit(self.imageDict['me'], (0,0), (94,0,34,34))

        self.left_foot = pygame.Surface((22,25), SRCALPHA)
        self.left_foot.blit(self.imageDict['me'], (0,0), (104,39,22,25))

        self.right_foot = pygame.Surface((22,25), SRCALPHA)
        self.right_foot.blit(self.imageDict['me'], (0,0), (104,71,22,25))

        self.red_cheek = pygame.Surface((6,6), SRCALPHA)
        self.red_cheek.blit(self.imageDict['me'], (0,0), (76,114,6,6))

        self.black_cheek = pygame.Surface((6,6), SRCALPHA)
        self.black_cheek.blit(self.imageDict['me'], (0,0), (76,122,6,6))

        self.opened_mouth = pygame.Surface((8,6), SRCALPHA)
        self.opened_mouth.blit(self.imageDict['me'], (0,0), (84,116,8,6))

        self.closed_mouth = pygame.Surface((8,4), SRCALPHA)
        self.closed_mouth.blit(self.imageDict['me'], (0,0), (84,124,8,4))

        self.closed_left_eye = pygame.Surface((10,18), SRCALPHA)
        self.closed_left_eye.blit(self.imageDict['me'], (0,0), (94,110,10,18))

        self.closed_right_eye = pygame.Surface((10,18), SRCALPHA)
        self.closed_right_eye.blit(self.imageDict['me'], (0,0), (106,110,10,18))

        self.opened_eye = pygame.Surface((10,18), SRCALPHA)
        self.opened_eye.blit(self.imageDict['me'], (0,0), (118,108,10,18))

        self.left_eyebrow = pygame.Surface((10,8), SRCALPHA)
        self.left_eyebrow.blit(self.imageDict['me'], (0,0), (106,98,10,8))

        self.right_eyebrow = pygame.Surface((10,8), SRCALPHA)
        self.right_eyebrow.blit(self.imageDict['me'], (0,0), (118,98,10,8))

    def update(self):
        self.t += 1
        if self.t == 30:
            self.t = 0

    def draw(self, screen):
        temp = pygame.Surface((128,118), SRCALPHA)

        if self.state == State.STOP:
            d = abs(self.t - 15)/15
            left_hand_d = right_hand_d = 0
            temp.blit(self.left_foot, (42,93))
            temp.blit(self.right_foot, (64,93))
        elif self.state == State.WALK:
            d = abs(self.t%15 - 7.5)/7.5
            left_hand_d = right_hand_d = abs(self.t - 15)/15
            temp.blit(self.left_foot,
                (42, 93 - max(0, (7-abs(self.t-15)))))
            temp.blit(self.right_foot,
                (64, 93 - max(0, (abs(self.t-15))-8)))
        elif self.state == State.GOODBY:
            d = abs(self.t - 15)/15
            left_hand_d = abs(self.t - 15)/15
            right_hand_d = 0
            temp.blit(self.left_foot, (42,93))
            temp.blit(self.right_foot, (64,93))

        if self.vec == Vec.LEFT:
            temp.blit(self.hand, (left_hand_d*10,60+d*2))
            temp.blit(self.body, (20,22+d*4))
            temp.blit(self.left_head, (18,d*4))
            temp.blit(self.hand, (94-right_hand_d*10,60+d*2))
            face_d = -12
            temp.blit(self.black_cheek, (84+face_d,54+d*4))
        elif self.vec == Vec.NONE:
            temp.blit(self.body, (20,22+d*4))
            temp.blit(self.left_head, (18,d*4))
            if self.state == State.GOODBY:
                temp.blit(self.hand, (left_hand_d*10,20+d*2))
            else:
                temp.blit(self.hand, (left_hand_d*10,60+d*2))
            temp.blit(self.hand, (94-right_hand_d*10,60+d*2))
            face_d = 0
            temp.blit(self.black_cheek, (38,54+d*4))
            temp.blit(self.black_cheek, (84,54+d*4))
        elif self.vec == Vec.RIGHT:
            temp.blit(self.hand, (94-right_hand_d*10,60+d*2))
            temp.blit(self.body, (20,22+d*4))
            temp.blit(self.right_head, (68,d*4))
            temp.blit(self.hand, (left_hand_d*10,60+d*2))
            face_d = 12
            temp.blit(self.black_cheek, (38+face_d,54+d*4))

        temp.blit(self.opened_eye, (47+face_d,42+d*4))
        temp.blit(self.opened_eye, (71+face_d,42+d*4))
        temp.blit(self.closed_mouth, (60+face_d,56+d*4))

        resize = 128*self.size_ratio
        temp = pygame.transform.scale(temp, (resize,resize))
        screen.blit(temp, (self.pos[0]-resize//2,self.pos[1]-resize))
