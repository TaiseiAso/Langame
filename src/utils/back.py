# coding: utf-8


import random
from .text import Text


class Hiragana:
    def __init__(self, font_path):
        self.text = Text(font_path)

        self.str = chr(random.randint(ord('ぁ'), ord('ん')))
        self.size = random.randint(12, 60)
        self.pos = [random.random(), -self.size]
        col = max(30, 230 - self.size)
        self.color = (col, col, col)
        self.spd = 0.5 + (self.size-12)/48

    def update(self):
        self.pos[1] += self.spd

    def draw(self, screen):
        width = screen.get_rect()[2]
        self.text.draw(screen, self.str,
            (self.pos[0]*(self.size + width)-self.size,self.pos[1]),
            self.size, color=self.color, bold=True)


class Back:
    def __init__(self, font_path, interval, height):
        self.font_path = font_path
        self.interval = interval
        self.height = height
        self.init()

    def init(self):
        self.hiragana_list = []
        self.t = 0

    def update(self):
        i = 0
        while True:
            if i == len(self.hiragana_list):
                break
            self.hiragana_list[i].update()
            if self.hiragana_list[i].pos[1] > self.height:
                self.hiragana_list.pop(i)
            else:
                i += 1

        self.t += 1
        if self.t == self.interval:
            self.t = 0
            new_hiragana = Hiragana(self.font_path)
            for i, hiragana in enumerate(self.hiragana_list):
                if new_hiragana.size < hiragana.size:
                    self.hiragana_list.insert(i, new_hiragana)
                    break
            else:
                self.hiragana_list.append(new_hiragana)

    def draw(self, screen):
        for hiragana in self.hiragana_list:
            hiragana.draw(screen)
