# coding: utf-8


import pygame


class Text:
    def __init__(self, screen, font_path):
        self.screen = screen
        self.font_path = font_path
        self.size = 0

    def draw(self, str, pos, size, color=None, bold=False):
        if size != self.size:
            self.font = pygame.font.Font(self.font_path, size)
            self.size = size
        if color is None:
            color = (0,0,0)
        self.font.set_bold(bold)
        text = self.font.render(str, True, color)
        self.screen.blit(text, pos)
