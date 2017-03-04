#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Spawn():
    def __init__(self,img_size, position,parent):
        self.x = position[0]
        self.y = position[1]
        if parent is None:
            self.stage = 0
            self.color = [1.0,1.0,0]
        else:
            self.color = parent.color
            self.stage = parent.stage +1 # evolution stage : 0 = pixel, 1, 2, 3
        self.points = []
        if self.stage == 0:
            self.points.append([(self.x + img_size[0])%img_size[0],self.y + img_size[1]%img_size[1]])


         
