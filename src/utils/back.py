# coding: utf-8


import random
from .text import Text


class Hiragana:
    def __init__(self, screen, font_path):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        self.text = Text(screen, font_path)

        self.str = chr(random.randint(ord('ぁ'), ord('ん')))
        self.size = random.randint(12, 60)
        self.pos = [random.randint(0, self.width - self.size), -self.size]
        col = max(30, 230 - self.size)
        self.color = (col, col, col)
        self.spd = 0.5 + (self.size-12)/48
        self.out = False

    def update(self):
        self.pos[1] += self.spd
        if self.pos[1] > self.height:
            self.out = True

    def draw(self):
        self.text.draw(self.str, self.pos, self.size, color=self.color, bold=True)


class Back:
    def __init__(self, screen, font_path, interval):
        self.screen = screen
        self.font_path = font_path
        self.interval = interval
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
            if self.hiragana_list[i].out:
                self.hiragana_list.pop(i)
            else:
                i += 1

        self.t += 1
        if self.t == self.interval:
            self.t = 0
            new_hiragana = Hiragana(self.screen, self.font_path)
            for i, hiragana in enumerate(self.hiragana_list):
                if new_hiragana.size < hiragana.size:
                    self.hiragana_list.insert(i, new_hiragana)
                    break
            else:
                self.hiragana_list.append(new_hiragana)

    def draw(self):
        for hiragana in self.hiragana_list:
            hiragana.draw()
