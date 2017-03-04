#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint

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
            self.stage = parent.stage +1 # evolution stage : 0 = pixel, 1, 2, 3
        self.points = []
        print self.color

        #patterns = [
                # red stages 0 to 3
                #[
                   #[[0,0]],
                   #[[0,0],[0,1],[1,0],[0,-1],[-1,0]]
                   #[[0,0],[0,1],[1,0],[0,-1],[-1,0],[0,2],[2,0],[0,-2],[-2,0]],
                   #[[0,0],[0,1],[1,0],[0,-1],[-1,0],[0,2],[2,0],[0,-2],[-2,0],[0,3],[3,0],[0,-3],[-3,0],[1,1],[-1,1],[-1,-1],[1,-1]]
        
                    #],
                # green stages 0 to 3
                #[
                    #],
                # blue stages 0 to 3
                #[
                    #]

                #]
        #global_index = default_colors.index(self.color)
        #pattern = patterns[global_index][self.stage]

        #for point in pattern:
            #print point
            #self.points.append([(self.x + point[0] + img_size[0])%img_size[0],
                #(self.y + point[1] + img_size[1])])
        if self.stage == 0:
            self.points.append([(self.x + img_size[0])%img_size[0],self.y + img_size[1]%img_size[1]])
        #print self.points

         
