# coding: utf-8


from pygame.locals import *
from .utils import *


class User:
    def __init__(self, screen, imageDict, key, font_path, romaji_path):
        self.init_message()
        self.screen = screen
        self.imageDict = imageDict
        self.key = key
        self.text = Text(screen, font_path)
        self.romaji = self.load_romaji(romaji_path)

    def load_romaji(self, romaji_path):
        romaji = []
        with open(romaji_path, 'r', encoding='utf-8') as f:
            line = f.readline()
            while line:
                line = line.strip()
                alphabets, hiragana = line.split(':')
                for alphabet in alphabets.split('^'):
                    romaji.append((alphabet, hiragana))
                line = f.readline()
        return romaji

    def init_message(self):
        self.ja_mes = ""
        self.en_mes = ""

    def check_message(self):
        return self.ja_mes != "" and self.en_mes == ""

    def print_message(self):
        print(self.ja_mes + self.en_mes)

    def backspace(self):
        if self.en_mes == "":
            self.ja_mes = self.ja_mes[:-1]
        else:
            self.en_mes = self.en_mes[:-1]

    def add_character(self, ch):
        if len(self.ja_mes) >= 20:
            return

        if self.en_mes == "n" and ch not in ['a','i','u','e','o','y','n']:
            self.ja_mes += "ん"
            self.en_mes = ch
            return

        next_mes = self.en_mes + ch
        for alphabet, hiragana in self.romaji:
            if next_mes == alphabet[:len(next_mes)]:
                if len(next_mes) == len(alphabet):
                    self.ja_mes += hiragana
                    self.en_mes = ""
                else:
                    self.en_mes = next_mes
                break

    def type_message(self):
        message = None
        for key_id in self.key.push:
            if key_id == K_BACKSPACE:
                self.backspace()
            elif K_a <= key_id <= K_z or key_id in [K_1, K_SLASH, K_COMMA, K_MINUS]:
                self.add_character(chr(key_id))
            elif key_id == K_RETURN:
                if self.check_message():
                    message = self.ja_mes
                    self.init_message()
        return message

    def draw(self):
        self.screen.blit(self.imageDict['window'], (32,484), (96,32,32,32))
        self.screen.blit(self.imageDict['window'], (32,516), (96,0,32,32))
        self.screen.blit(self.imageDict['window'], (32,548), (64,32,32,32))
        for w in range(64,736,32):
            self.screen.blit(self.imageDict['window'], (w,484), (0,0,32,32))
            self.screen.blit(self.imageDict['window'], (w,516), (0,96,32,32))
            self.screen.blit(self.imageDict['window'], (w,548), (64,0,32,32))
        self.screen.blit(self.imageDict['window'], (736,484), (0,32,32,32))
        self.screen.blit(self.imageDict['window'], (736,516), (32,0,32,32))
        self.screen.blit(self.imageDict['window'], (736,548), (32,32,32,32))

        self.text.draw(self.ja_mes + self.en_mes, (64,516), 32)
