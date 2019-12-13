# coding: utf-8


import pygame
from pygame.locals import *
from .text import Text


class Balloon:
    def __init__(self, imageDict, font_path, text_interval):
        self.imageDict = imageDict
        self.text = Text(font_path)
        self.text_interval = text_interval
        self.set_message("")

    def set_message(self, message):
        self.message = message
        mes_list = [len(mes) for mes in self.message]
        self.mes_len = sum(mes_list)
        self.mes_width = max(mes_list) if mes_list != [] else 0
        self.mes_height = len(mes_list) if mes_list != [] else 0
        self.mes_pop_num = 0
        self.t = 0

    def update(self):
        if self.mes_pop_num < self.mes_len:
            self.t += 1
            if self.t == self.text_interval:
                self.t = 0
                self.mes_pop_num += 1

    def draw(self, screen, vec, pos, size):
        width = 32*(self.mes_width + 1)
        height = 32*(self.mes_height + 1)
        temp = pygame.Surface((width+32,height+32), SRCALPHA)

        temp.blit(self.imageDict['window'], (0,0), (96,32,32,32))
        temp.blit(self.imageDict['window'], (0,height), (64,32,32,32))
        temp.blit(self.imageDict['window'], (width,height), (32,32,32,32))
        temp.blit(self.imageDict['window'], (width,0), (0,32,32,32))

        for w in range(32,width,32):
            temp.blit(self.imageDict['window'], (w,0), (0,0,32,32))
            temp.blit(self.imageDict['window'], (w,height), (64,0,32,32))

        for h in range(32,height,32):
            temp.blit(self.imageDict['window'], (0,h), (96,0,32,32))
            temp.blit(self.imageDict['window'], (width,h), (32,0,32,32))
            for w in range(32,width,32):
                temp.blit(self.imageDict['window'], (w,h), (0,96,32,32))

        resized_width = size*(self.mes_width + 2)
        resized_height = size*(self.mes_height + 2)

        if vec == 1:
            temp.blit(self.imageDict['window'], (width//2,0), (0,64,32,32))
            put_pos = (pos[0]-resized_width//2, pos[1])
        elif vec == 2:
            temp.blit(self.imageDict['window'], (width,height//2), (32,64,32,32))
            put_pos = (pos[0]-resized_width, pos[1]-resized_height//2)
        elif vec == 3:
            temp.blit(self.imageDict['window'], (width//2,height), (64,64,32,32))
            put_pos = (pos[0]-resized_width//2, pos[1]-resized_height)
        elif vec == 4:
            temp.blit(self.imageDict['window'], (0,height//2), (96,64,32,32))
            put_pos = (pos[0], pos[1]-resized_height//2)
        else:
            put_pos = pos

        remain_pop = self.mes_pop_num
        for i, mes in enumerate(self.message):
            text_pos = (32,32*(i+1))
            if remain_pop <= len(mes):
                self.text.draw(temp, mes[:remain_pop], text_pos, 32)
                break
            else:
                self.text.draw(temp, mes, text_pos, 32)
                remain_pop -= len(mes)

        temp = pygame.transform.smoothscale(temp, (resized_width,resized_height))
        screen.blit(temp, put_pos)
