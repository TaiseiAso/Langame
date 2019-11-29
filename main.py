# coding: utf-8


# https://support.microsoft.com/ja-jp/help/883232
# https://qiita.com/abcsupergt/items/08a1c2df03a5d4c10539

import pygame
from pygame.locals import *
from ai import AI
from src import *
import yaml
import sys


class Key:
    def __init__(self):
        self.press = []
        self.update()

    def update(self):
        self.push = []
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                self.press.append(event.key)
                self.push.append(event.key)
            elif event.type == KEYUP:
                if event.key in self.press:
                    self.press.remove(event.key)
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()


class Text:
    def __init__(self):
        self.font = pygame.font.SysFont("hg正楷書体pro", 50)

    def draw(self, screen, str, dest):
        text = self.font.render(str, True, (255,255,255))
        screen.blit(text, dest)


class User:
    def __init__(self, key, romaji_path):
        self.init_message()
        self.key = key
        self.text = Text()
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
        if len(self.ja_mes) >= 12:
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

    def draw(self, screen):
        self.text.draw(screen, self.ja_mes + self.en_mes, [20,500])


class Game:
    def __init__(self, name, size, fps):
        data_config = yaml.load(stream=open("config/data_config.yml", 'rt', encoding='utf-8'), Loader=yaml.SafeLoader)
        data_path = data_config['path']
        pygame.init()
        pygame.display.set_mode(size, 0, 32)
        pygame.display.set_caption(name)
        self.screen = pygame.display.get_surface()
        self.key = Key()
        self.user = User(self.key, data_path['romaji'])
        self.ai = AI("config/ai_config.yml")
        self.ai.prepare_test()
        self.match = Match(data_path['pattern'], data_path['synonym'])
        self.field = Field(size, data_path['map'], data_path['ground_param'], data_path['object_param'])
        self.fps = fps

    def input(self):
        self.key.update()
        message = self.user.type_message()
        if message:
            action = self.match.judge_action(message)
            if action >= 0:
                print("action: " + str(action))
            else:
                print(message + " > " + self.ai.test(message))

    def draw(self):
        self.screen.fill((0,0,0,0))
        self.field.draw(self.screen)
        self.user.draw(self.screen)
        pygame.display.update()

    def wait(self):
        pygame.time.wait(int(1000 / self.fps))

    def play(self):
        while True:
            self.input()
            self.draw()
            self.wait()


if __name__ == "__main__":
    game = Game("LANGAME DUNGEON", (800,600), 30)
    game.play()
