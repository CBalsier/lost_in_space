#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
from pygame import mixer


class Spawn():
    def __init__(self,img_size, position,parent=None, color = None):
        self.x = position[0]
        self.y = position[1]
        default_colors = [[0.83921,0.22745,0.17647],[0,0.64705,0.37254],[0,0.04705,0.38823],[0,0.61176,0.61176],[0.76470,0,0.21960],[0.96470,0.90588,0.11764]] # RGBCMY
        
        if parent is None:
            self.stage = 0
            self.color = default_colors[color] if color is not None else default_colors[randint(0,len(default_colors)-1)]
        else:
            self.color = default_colors[color] if color is not None else parent.color
            self.stage = min(parent.stage +1, 3) # evolution stage : 0 = pixel, 1, 2, 3
        self.points = []

        #self.color = default_colors[0] # for testing purposes !
        #self.stage = randint(0,1) # for testing purposes !

        patterns = [
                # red stages 0 to 3
                [
                    [[0,0]],
                    [[0,0],[1,1],[1,-1],[-1,-1],[-1,1]],
                    [[0,0],[1,1],[1,-1],[-1,-1],[-1,1],[2,2],[2,-2],[-2,-2],[-2,2]],
                    [[0,0],[1,1],[1,-1],[-1,-1],[-1,1],[2,2],[2,-2],[-2,-2],[-2,2],[3,3],[3,-3],[-3,-3],[-3,3]]
                    ],
                # green stages 0 to 3
                [
                    [[0,0]],
                    [[0,0]],
                    [[0,0]],
                    [[0,0]]
                    ],
                # blue stages 0 to 3
                [
                    [[0,0]],
                    [[0,0],[0,1],[1,0],[0,-1],[-1,0]],
                    [[0,0],[0,1],[1,0],[0,-1],[-1,0],[0,2],[2,0],[0,-2],[-2,0]],
                    [[0,0],[0,1],[1,0],[0,-1],[-1,0],[0,2],[2,0],[0,-2],[-2,0],[0,3],[3,0],[0,-3],[-3,0]]

                    ],
                # cyan stages 0 to 3
                [
                    [[0,0]],
                    [[0,0],[0,1],[1,0],[0,-1],[-1,0]],
                    [[0,0],[0,1],[1,0],[0,-1],[-1,0],[0,2],[2,0],[0,-2],[-2,0]],
                    [[0,0],[0,1],[1,0],[0,-1],[-1,0],[0,2],[2,0],[0,-2],[-2,0],[0,3],[3,0],[0,-3],[-3,0]]
                    ],
                # magenta stages 0 to 3
                [
                    [[0,0]],
                    [[0,0],[1,1],[1,-1],[-1,-1],[-1,1]],
                    [[0,0],[1,1],[1,-1],[-1,-1],[-1,1],[2,2],[2,-2],[-2,-2],[-2,2]],
                    [[0,0],[1,1],[1,-1],[-1,-1],[-1,1],[2,2],[2,-2],[-2,-2],[-2,2],[3,3],[3,-3],[-3,-3],[-3,3]]
                    ],
                # yellow stages 0 to 3
                [
                    [[0,0]],
                    [[0,0]],
                    [[0,0]],
                    [[0,0]]
                    ]
                ]
        speed_mods = [
                # red stages 0 to 3
                [1, 2, 4],
                # green stages 0 to 3
                [1, 1.6, pow(1.6,2)],
                # blue stages 0 to 3
                [1, 1.3, pow(1.3,2)],
                # cyan stages 0 to 3
                [1, 1.3, pow(1.3, 2)],
                # magenta stages 0 to 3
                [1, 2, 4],
                # yellow stages 0 to 3
                [1, 1.6, pow(1.6, 2)],
                ]
        fading_mods = [
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
        
        sound_files = [
                # red
                [
                    "red_0.ogg","red_1.ogg","red_2.ogg","red_3.ogg"
                    ],
                # green
                [
                    "green_0.ogg","green_1.ogg","green_2.ogg","green_3.ogg"
                    ],
                # blue
                [
                    "blue_0.ogg","blue_1.ogg","blue_2.ogg","blue_3.ogg"
                    ],
                # cyan
                [
                    "cyan_0.ogg","cyan_1.ogg","cyan_2.ogg","cyan_3.ogg"
                    ],
                # magenta
                [
                    "magenta_0.ogg","magenta_1.ogg","magenta_2.ogg","magenta_3.ogg"
                    ],
                #yellow
                [
                    "yellow_0.ogg","yellow_1.ogg","yellow_2.ogg","yellow_3.ogg"
                    ]
                ]

        color_index = default_colors.index(self.color)
        pattern = patterns[color_index][self.stage]

        self.speed = speed_mods[color_index][min(self.stage,2)]
        self.fading = fading_mods[color_index][min(self.stage,2)]

        mixer.init()
        self.sound_effect = mixer.Sound(sound_files[color_index][self.stage])

        for point in pattern:
            #print point
            self.points.append([(self.x + point[0] + img_size[0])%img_size[0],
                (self.y + point[1] + img_size[1])%img_size[1]])
        #if self.stage == 0:
            #self.points.append([(self.x + img_size[0])%img_size[0],self.y + img_size[1]%img_size[1]])
        #print self.points

         
