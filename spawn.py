#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
from pygame import mixer


class Spawn():
    def __init__(self,img_size, position,parent=None):
        self.x = position[0]
        self.y = position[1]
        default_colors = [[1.0,0,0],[0,1.0,0],[0,0,1.0],[0,1.0,1.0],[1.0,0,1.0],[1.0,1.0,0]] # RGBCMY
        
        if parent is None:
            self.stage = 0
            self.color = default_colors[randint(0,len(default_colors)-1)]
        else:
            self.color = parent.color
            self.stage = parent.stage +1 # evolution stage : 0 = pixel, 1, 2, 3
        self.points = []

        self.color = default_colors[0] # for testing purposes !
        self.stage = randint(0,1) # for testing purposes !

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
                    [[0,0],[0,1],[1,0],[0,-1],[-1,0],[0,2],[2,0],[0,-2],[-2,0],[0,3],[3,0],[0,-3],[-3,0],[1,1],[-1,1],[-1,-1],[1,-1]] 
                    ],
                # cyan stages 0 to 3
                [
                    [[0,0]],
                    [[0,0],[0,1],[1,0],[0,-1],[-1,0]],
                    [[0,0],[0,1],[1,0],[0,-1],[-1,0],[0,2],[2,0],[0,-2],[-2,0]],
                    [[0,0],[0,1],[1,0],[0,-1],[-1,0],[0,2],[2,0],[0,-2],[-2,0],[0,3],[3,0],[0,-3],[-3,0],[1,1],[-1,1],[-1,-1],[1,-1]] 
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
                2,
                # green stages 0 to 3
                1.6,
                # blue stages 0 to 3
                1.3,
                # cyan stages 0 to 3
                1.3,
                # magenta stages 0 to 3
                2,
                # yellow stages 0 to 3
                1.6
                ]
        fading_mods = [
                # red stages 0 to 3
                10,
                # green stages 0 to 3
                13,
                # blue stages 0 to 3
                17,
                # cyan stages 0 to 3
                17,
                # magenta stages 0 to 3
                10,
                # yellow stages 0 to 3
                13
                ]
        
        sound_files = [
                # red
                [
                    "red_0.wav","red_1.wav","red_2.wav","red_3.wav"
                    ],
                # green
                [
                    "green_0.wav","green_1.wav","green_2.wav","green_3.wav"
                    ],
                # blue
                [
                    "blue_0.wav","blue_1.wav","blue_2.wav","blue_3.wav"
                    ],
                # cyan
                [
                    "cyan_0.wav","cyan_1.wav","cyan_2.wav","cyan_3.wav"
                    ],
                # magenta
                [
                    "magenta_0.wav","magenta_1.wav","magenta_2.wav","magenta_3.wav"
                    ],
                #yellow
                [
                    "yellow_0.wav","yellow_1.wav","yellow_2.wav","yellow_3.wav"
                    ]
                ]

        color_index = default_colors.index(self.color)
        pattern = patterns[color_index][self.stage]
        self.speed = speed_mods[color_index]
        self.fading = fading_mods[color_index]
        mixer.init(44100,-16,2,208)
        self.sound_effect = mixer.Sound(sound_files[color_index][self.stage])
        for point in pattern:
            #print point
            self.points.append([(self.x + point[0] + img_size[0])%img_size[0],
                (self.y + point[1] + img_size[1])])
        #if self.stage == 0:
            #self.points.append([(self.x + img_size[0])%img_size[0],self.y + img_size[1]%img_size[1]])
        print self.points

         
