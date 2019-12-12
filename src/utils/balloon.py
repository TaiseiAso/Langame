# coding: utf-8


import pygame
from pygame.locals import *
from .text import Text


class Balloon:
    def __init__(self, screen, imageDict, font_path, text_interval):
        self.screen = screen
        self.imageDict = imageDict
        self.text = Text(screen, font_path)
        self.text_interval = text_interval
        self.set_message("")
        self.set_parameter(vec=0, size=32, pos=(0,0))

    def set_message(self, message):
        self.message = message
        mes_list = [len(mes) for mes in self.message]
        self.mes_len = sum(mes_list)
        self.mes_width = max(mes_list) if mes_list != [] else 0
        self.mes_height = len(mes_list) if mes_list != [] else 0
        self.mes_pop_num = 0
        self.t = 0

    def set_parameter(self, vec=None, size=None, pos=None):
        if vec is not None:
            self.vec = vec
        if size is not None:
            self.size = size
        if pos is not None:
            self.pos = pos

        if vec is not None or size is not None:
            self.make_scaling_vec_chip()
        if size is not None:
            self.make_scaling_chip()

    def make_scaling_vec_chip(self):
        temp = pygame.Surface((32,32), SRCALPHA)
        if self.vec == 1:
            temp.blit(self.imageDict['window'], (0,0), (0,64,32,32))
        elif self.vec == 2:
            temp.blit(self.imageDict['window'], (0,0), (32,64,32,32))
        elif self.vec == 3:
            temp.blit(self.imageDict['window'], (0,0), (64,64,32,32))
        elif self.vec == 4:
            temp.blit(self.imageDict['window'], (0,0), (96,64,32,32))
        self.arrow = pygame.transform.scale(temp, (self.size,self.size))

    def make_scaling_chip(self):
        temp = pygame.Surface((32,32), SRCALPHA)
        temp.blit(self.imageDict['window'], (0,0), (96,32,32,32))
        self.up_left = pygame.transform.scale(temp, (self.size,self.size))

        temp = pygame.Surface((32,32), SRCALPHA)
        temp.blit(self.imageDict['window'], (0,0), (64,32,32,32))
        self.bottom_left = pygame.transform.scale(temp, (self.size,self.size))

        temp = pygame.Surface((32,32), SRCALPHA)
        temp.blit(self.imageDict['window'], (0,0), (0,32,32,32))
        self.up_right = pygame.transform.scale(temp, (self.size,self.size))

        temp = pygame.Surface((32,32), SRCALPHA)
        temp.blit(self.imageDict['window'], (0,0), (32,32,32,32))
        self.bottom_right = pygame.transform.scale(temp, (self.size,self.size))

        temp = pygame.Surface((32,32), SRCALPHA)
        temp.blit(self.imageDict['window'], (0,0), (0,0,32,32))
        self.up = pygame.transform.scale(temp, (self.size,self.size))

        temp = pygame.Surface((32,32), SRCALPHA)
        temp.blit(self.imageDict['window'], (0,0), (64,0,32,32))
        self.bottom = pygame.transform.scale(temp, (self.size,self.size))

        temp = pygame.Surface((32,32), SRCALPHA)
        temp.blit(self.imageDict['window'], (0,0), (96,0,32,32))
        self.left = pygame.transform.scale(temp, (self.size,self.size))

        temp = pygame.Surface((32,32), SRCALPHA)
        temp.blit(self.imageDict['window'], (0,0), (32,0,32,32))
        self.right = pygame.transform.scale(temp, (self.size,self.size))

        temp = pygame.Surface((32,32), SRCALPHA)
        temp.blit(self.imageDict['window'], (0,0), (0,96,32,32))
        self.body = pygame.transform.scale(temp, (self.size,self.size))

    def update(self):
        if self.mes_pop_num < self.mes_len:
            self.t += 1
            if self.t == self.text_interval:
                self.t = 0
                self.mes_pop_num += 1

    def draw(self):
        width = self.size*(self.mes_width+1)
        height = self.size*(self.mes_height+1)

        if self.vec == 0:
            first_pos = self.pos
        elif self.vec == 1:
            first_pos = [
                self.pos[0] - width//2,
                self.pos[1]]
        elif self.vec == 2:
            first_pos = [
                self.pos[0] - width,
                self.pos[1] - height//2]
        elif self.vec == 3:
            first_pos = [
                self.pos[0] - width//2,
                self.pos[1] - height]
        else:
            first_pos = [
                self.pos[0],
                self.pos[1] - height//2]

        self.screen.blit(self.up_left, first_pos)
        self.screen.blit(self.bottom_left, (first_pos[0], first_pos[1] + height))
        self.screen.blit(self.up_right, (first_pos[0] + width, first_pos[1]))
        self.screen.blit(self.bottom_right, (first_pos[0] + width, first_pos[1] + height))

        for w in range(first_pos[0] + self.size, first_pos[0] + self.size*(self.mes_width+1), self.size):
            self.screen.blit(self.up, (w, first_pos[1]))
            self.screen.blit(self.bottom, (w, first_pos[1] + height))

        for h in range(first_pos[1] + self.size, first_pos[1] + self.size*(self.mes_height+1), self.size):
            self.screen.blit(self.left, (first_pos[0], h))
            self.screen.blit(self.right, (first_pos[0] + width, h))
            for w in range(first_pos[0] + self.size, first_pos[0] + self.size*(self.mes_width+1), self.size):
                self.screen.blit(self.body, (w, h))

        self.screen.blit(self.arrow, self.pos)

        remain_pop = self.mes_pop_num
        for i, mes in enumerate(self.message):
            text_pos = (first_pos[0] + self.size, first_pos[1] + self.size*(i+1))
            if remain_pop <= len(mes):
                self.text.draw(mes[:remain_pop], text_pos, self.size)
                break
            else:
                self.text.draw(mes, text_pos, self.size)
                remain_pop -= len(mes)
