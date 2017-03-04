#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Spawn():
    def __init__(self,position,parent, source_spots):
        self.x = position[0]
        self.y = position[1]
        self.color = parent.color
        self.stage = parent.stage +1 # evolution stage : 0 = pixel, 1, 2, 3
        self.points = []
        if self.stage == 0:
            self.points.append([0,0])

        for point in self.points:
            source_spots.append([self.x + point[0],self.y + point[1]])
         
