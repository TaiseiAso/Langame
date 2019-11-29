# coding: utf-8


import pygame


class Me:
    def __init__(self):
        self.pos = [0, 0]

    def draw(self, screen, gap, len):
        screen.fill(
            (230,230,255),
            (
                gap[0]+self.pos[0]*len+len//5,
                gap[1]+self.pos[1]*len-len//4,
                3*len//5,
                len
            )
        )


class Field:
    def __init__(self, screen_size, map_path, ground_param_path, object_param_path):
        self.screen_size = screen_size
        self.load_map(map_path)
        self.me = Me()
        self.set_map(0)

    def load_map(self, map_path):
        self.map = []
        self.size = []
        self.len = []
        self.gap = []
        self.init_pos = []
        read_type = 0
        with open(map_path, 'r', encoding='utf-8') as f:
            line = f.readline()
            while line:
                if line != '\n' and line[0] != '#':
                    line = line.strip()
                    if read_type == 0:
                        _init_pos = [int(s) for s in line.split(',')]
                        self.init_pos.append(_init_pos)
                        read_type = 1
                    elif read_type == 1:
                        _size = [int(s) for s in line.split(',')]
                        self.size.append(_size)

                        len_x = (self.screen_size[0] - 20)//_size[0]
                        len_y = (self.screen_size[1] - 120)//_size[1]
                        _len = min(len_x, len_y)
                        self.len.append(_len)

                        gap_x = (self.screen_size[0] - _size[0]*_len)//2
                        gap_y = (self.screen_size[1] - 100 - _size[1]*_len)//2
                        self.gap.append([gap_x, gap_y])

                        _map = [[{} for _ in range(_size[0])] for _ in range(_size[1])]
                        row = 0
                        read_type = 2
                    else:
                        for col, data in enumerate(line.split()):
                            if '_' not in data:
                                if read_type == 2:
                                    _map[row][col]['grd_img_id'] = int(data[:2])
                                    _map[row][col]['grd_id'] = int(data[2:])
                                elif read_type == 3:
                                    _map[row][col]['obj_img_id'] = int(data[:2])
                                    _map[row][col]['obj_id'] = int(data[2:])
                                else:
                                    _map[row][col]['dec_img_id'] = int(data)
                        row += 1
                        if row == _size[1]:
                            row = 0
                            read_type += 1
                            if read_type == 5:
                                self.map.append(_map)
                                read_type = 0
                line = f.readline()

    def set_map(self, map_id):
        self.map_id = map_id
        self.me.pos = self.init_pos[map_id]

    def command(self, action):
        pass

    def draw(self, screen):
        _size = self.size[self.map_id]
        _len = self.len[self.map_id]
        _gap = self.gap[self.map_id]
        _map = self.map[self.map_id]

        for y in range(_size[1]):
            for x in range(_size[0]):
                maptcip = _map[y][x]
                grd_img_id = maptcip.get('grd_img_id')
                obj_img_id = maptcip.get('obj_img_id')
                dec_img_id = maptcip.get('dec_img_id')

                if grd_img_id is not None:
                    rect = (_gap[0]+x*_len, _gap[1]+y*_len, _len, _len)
                    if grd_img_id == 0:
                        color = (50,200,50)
                    elif grd_img_id == 1:
                        color = (20,20,220)
                    elif grd_img_id == 2:
                        color = (150,150,150)
                    elif grd_img_id == 3:
                        color = (50,50,50)
                    screen.fill(color, rect)

                if obj_img_id is not None:
                    rect = (_gap[0]+x*_len+_len//5, _gap[1]+y*_len+_len//5, 3*_len//5, 3*_len//5)
                    if obj_img_id == 0:
                        color = (50,50,50)
                    screen.fill(color, rect)

                if dec_img_id is not None:
                    if dec_img_id == 0:
                        pygame.draw.polygon(
                            screen,
                            (0,200,0),
                            [
                                [_gap[0]+x*_len, _gap[1]+y*_len],
                                [_gap[0]+x*_len+_len//3, _gap[1]+y*_len-_len//4],
                                [_gap[0]+x*_len+_len//2, _gap[1]+y*_len]
                            ]
                        )

            if y == self.me.pos[1]:
                self.me.draw(screen, _gap, _len)
