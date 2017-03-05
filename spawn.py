#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
from pygame import mixer

SOUND_FILES = [
    # red
    [
        "Explosion.ogg", "red_1.ogg", "red_2.ogg", "red_3.ogg"
    ],
    # green
    [
        "Explosion.ogg", "green_1.ogg", "green_2.ogg", "green_3.ogg"
    ],
    # blue
    [
        "Explosion.ogg", "blue_1.ogg", "blue_2.ogg", "blue_3.ogg"
    ],
    # cyan
    [
        "Explosion.ogg", "cyan_1.ogg", "cyan_2.ogg", "cyan_3.ogg"
    ],
    # magenta
    [
        "Explosion.ogg", "magenta_1.ogg", "magenta_2.ogg", "magenta_3.ogg"
    ],
    # yellow
    [
        "Explosion.ogg", "yellow_1.ogg", "yellow_2.ogg", "yellow_3.ogg"
    ]
]

SPEED_MODS = [
    # red stages 0 to 3
    [1, 2, 4],
    # green stages 0 to 3
    [1, 1.6, pow(1.6, 2)],
    # blue stages 0 to 3
    [1, 1.3, pow(1.3, 2)],
    # cyan stages 0 to 3
    [1, 1.3, pow(1.3, 2)],
    # magenta stages 0 to 3
    [1, 2, 4],
    # yellow stages 0 to 3
    [1, 1.6, pow(1.6, 2)],
]

PATTERNS = [
    # red stages 0 to 3
    [
        [[0, 0]],
        [[0, 0], [1, 1], [0, 1], [0, -1], [1, -1], [-1, -1], [-1, 1]],
        [[0, 0], [1, 1], [1, -1], [-1, -1], [-1, 1], [2, 2], [2, -2], [-2, -2], [-2, 2], [0, 1], [0, -1], [2, 0],
         [-2, 0], [0, 2], [0, -2]],
        [[0, 0], [1, 1], [1, -1], [-1, -1], [-1, 1], [2, 2], [2, -2], [-2, -2], [-2, 2], [0, 1], [0, -1], [2, 0],
         [-2, 0], [0, 2], [0, -2], [3, -1], [3, 0], [3, 1], [-1, 3], [0, 3], [1, 3], [-3, -1], [-3, 0], [-3, 1],
         [-1, -3], [0, -3], [1, -3]]
    ],
    # green stages 0 to 3
    [
        [[0, 0]],
        [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]],
        [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1], [1, 2], [2, 1], [2, -1], [1, -2],
         [-1, -2], [-2, -1], [-2, 1], [-1, 2]],
        [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1], [1, 2], [2, 1], [2, -1],
         [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2], [0, 3], [3, 0], [0, -3], [-3, 0]]
    ],
    # blue stages 0 to 3
    [
        [[0, 0]],
        [[0, 0], [0, 1], [1, 0], [0, -1], [-1, 0]],
        [[0, 1], [1, 0], [0, -1], [-1, 0], [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2]],
        [[0, 1], [1, 0], [0, -1], [-1, 0], [1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2],
         [2, 3], [3, 2], [3, -2], [2, -3], [-2, -3], [-3, -2], [-3, 2], [-2, 3]]

    ],
    # cyan stages 0 to 3
    [
        [[0, 0]],
        [[0, 0], [0, 1], [1, 0], [0, -1], [-1, 0]],
        [[0, 0], [0, 1], [1, 0], [0, -1], [-1, 0], [0, 2], [2, 0], [0, -2], [-2, 0]],
        [[0, 0], [0, 1], [1, 0], [0, -1], [-1, 0], [0, 2], [2, 0], [0, -2], [-2, 0], [0, 3], [3, 0], [0, -3], [-3, 0]]
    ],
    # magenta stages 0 to 3
    [
        [[0, 0]],
        [[0, 0], [1, 1], [1, -1], [-1, -1], [-1, 1]],
        [[0, 0], [1, 1], [1, -1], [-1, -1], [-1, 1], [2, 2], [2, -2], [-2, -2], [-2, 2]],
        [[0, 0], [1, 1], [1, -1], [-1, -1], [-1, 1], [2, 2], [2, -2], [-2, -2], [-2, 2], [3, 3], [3, -3], [-3, -3],
         [-3, 3]]
    ],
    # yellow stages 0 to 3
    [
        [[0, 0]],
        [[0, 0], [1, 1], [1, 0], [1, -1], [-1, -1], [-1, 0], [-1, 1]],
        [[0, 0], [1, 1], [1, 0], [1, -1], [-1, -1], [-1, 0], [-1, 1], [0, -2], [0, 2], [2, 0], [-2, 0]],
        [[0, 0], [1, 1], [1, 0], [1, -1], [-1, -1], [-1, 0], [-1, 1],
         [0, -2], [0, 2], [2, 0], [-2, 0], [-4, 0], [-3, 1], [-3, 0], [-3, -1], [-2, 2], [-2, -2], [-1, 3], [-1, -3],
         [0, 4], [0, -4], [1, 3], [1, -3], [2, -2], [2, 2], [3, 1], [3, 0], [3, -1], [4, 0]]
    ],
]

FADING_MODS = [
        # red stages 0 to 3
        [10, 20, 40],
        # green stages 0 to 3
        [13, 20.8, 33.28],
        # blue stages 0 to 3
        [17, 22.1,28.73],
        # cyan stages 0 to 3
        [17, 22.1, 28.73],
        # magenta stages 0 to 3
        [10, 20, 40],
        # yellow stages 0 to 3
        [13, 20.8, 33.28],
]

DEFAULT_COLORS = [[0.83921,0.22745,0.17647],[0,0.64705,0.37254],[0,0.04705,0.38823],[0,0.61176,0.61176],[0.76470,0,0.21960],[0.96470,0.90588,0.11764]]  # RGBCMY

class Spawn():
    def __init__(self,img_size, position,parent=None, color = None):
        self.x = position[0]
        self.y = position[1]

        if parent is None:
            self.color_id = color if color is not None else randint(0,len(DEFAULT_COLORS)-1)
            self.color = DEFAULT_COLORS[self.color_id]
        else:
            self.color_id = color if color is not None else parent.color_id
            self.color = DEFAULT_COLORS[self.color_id]

    def get_points(self, level, img_size):
        print self.color_id
        ret = []
        for point in PATTERNS[self.color_id][level]:
            ret.append([(self.x + point[0] + img_size[0])%img_size[0],
                (self.y + point[1] + img_size[1])%img_size[1]])
        return ret

    def get_speed(self, level):
        return SPEED_MODS[self.color_id][min(level, 2)]

    def get_fading(self, level):
        return FADING_MODS[self.color_id][min(level, 2)]

    def get_sound(self, level):
        mixer.init()
        return mixer.Sound(SOUND_FILES[self.color_id][level])
