#!/usr/bin/env python
# -*- coding = utf-8 -*-
"""
Digital Art Jam
"""

from arbalet.core import Application, Rate
from arbalet.colors import hsv_to_rgb
import pygame, argparse, random


class LostInSpace(Application):
    def __init__(self, argparser):
        Application.__init__(self, argparser)
        self.color = None
        self.base_color = None
        self.x = self.height/2
        self.y = self.width/2
        self.life = 3
        
    def run(self):
        # Update the screen every second.
        rate = Rate(1000.0)
        with self.model:
            self.model.set_all('white')
            self.model.set_pixel(self.x,self.y, 'red')
            self.color = self.model.get_pixel(self.x,self.y)
            self.base_color = self.color
        self.source_spots = []
        self.spawn_source([0,0])
        while 1:
            for event in self.arbalet.events.get():
                if event.type in [pygame.KEYDOWN]:
                    if event.key == pygame.K_UP:
                        self.x -= 1
                    elif event.key == pygame.K_DOWN:
                        self.x += 1
                    elif event.key == pygame.K_RIGHT:
                        self.y += 1
                    elif event.key == pygame.K_LEFT:
                        self.y -= 1
                    with self.model:
                        self.color = (self.color - self.base_color / 5)
                        self.model.set_pixel(self.x, self.y, self.color)
                        #print (self.color)
                        print [self.x, self.y]
            print self.source_spots
            if [self.x, self.y] in self.source_spots:
                self.spawn_source([0,0])

    def spawn_source(self,last_position):
        color = hsv_to_rgb(random.random(),random.random(), random.random())
        #color_list = ['red', 'green', 'blue', 'black']
        #color = color_list[random.randint(0,len(color_list))-1]
        position = [random.randint(0,self.model.width),random.randint(0,self.model.height)]#random (test que different de position actuelle)
        pattern_list =[
                [[1,1],[0,0],[-1,-1],[1,-1],[-1,1]],
                [[0,1],[0,-1],[1,0],[-1,0]],
                [[0,1],[0,-1],[1,0],[3,1],[3,-1],[4,0]]
                ]
                # random dans une liste de formes (=liste de coordonnees)
        pattern = pattern_list[random.randint(0,len(pattern_list))-1]# random dans une liste de formes (=liste de coordonnees)

        self.source_spots = []
        for point in pattern:
            new_x = position[0] + point[0]
            new_y = position[1] + point[1]
            if new_x < 0:
                new_x = 0
            elif new_x > (self.model.height-1):
                new_x = self.model.height -1
            if new_y < 0:
                new_y = 0
            elif new_y > (self.model.width-1):
                new_y = self.model.width -1
            self.model.set_pixel(new_x,new_y, color)

            self.source_spots.append([new_x,new_y])
            print self.source_spots

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Do something :D')
    LostInSpace(parser).start()
