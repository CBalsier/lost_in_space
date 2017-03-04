#!/usr/bin/env python
# -*- coding = utf-8 -*-
"""
Digital Art Jam
"""

from arbalet.core import Application, Rate
from arbalet.colors import hsv_to_rgb, rgb_to_hsv
import pygame, argparse, random
from pygame.locals import *
from PIL import Image
import time

from spawn import Spawn

size = 50,50
MAX_SPEED = 10
MIN_SPEED = 1

class LostInSpace(Application):
    def __init__(self, argparser):
        Application.__init__(self, argparser)
        self.base_color = None
        self.color = None
        # relative coordonate to image center
        self.y = self.height/2
        self.x = self.width/2
        # offset from
        self.offset_y = 0
        self.offset_x = 0
        self.model.set_all('white')
        self.state = 'init'
        self.image = Image.new('RGB',size, (255,255,255))
        self.source_spots = []
        self.spawns = []
        self.speed = 1

    def find_spawn(self, coord):
        for spawn in self.spawns:
            if coord in spawn.points:
                return spawn

    def spawn_source(self,position=[random.randint(0,size[0]),random.randint(0,size[1])], parent = None):
        new_spawn=Spawn(size, position, parent)
        self.spawns.append(new_spawn)
        for point in new_spawn.points:
            self.source_spots.append(point)

    def event(self):
        action = False
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            self.offset_y -= 1 % size[1]
            action = True
        elif keys[K_DOWN]:
            self.offset_y += 1 % size[1]
            action = True
        elif keys[K_RIGHT]:
            self.offset_x += 1 % size[0]
            action = True
        elif keys[K_LEFT]:
            self.offset_x -= 1 % size[0]
            action = True
        if keys[K_ESCAPE]:
            self.state = 'end'
        elif keys[K_SPACE]:
            with self.model:
                # set initial color
                self.model.set_pixel(self.y, self.x, hsv_to_rgb(0, 1, 1))
                self.color = self.model.get_pixel(self.y, self.x)
                self.base_color = self.color

                # spawn first stop near the player
                self.spawn_source([self.offset_x + 4, self.offset_y + 4])

                self.state = 'running'

        if self.state == 'init':
            pass
            #self.arbalet.user_model.write("Draw me", 'blue')
        elif self.state == 'running' and action:
            self.speed = min(self.speed+1,MAX_SPEED)
            with self.model:
                # Generating image
                r = int(round(self.color[0] * 255))
                g = int(round(self.color[1] * 255))
                b = int(round(self.color[2] * 255))


                # we do not print if we are black ou white
                if not((r == 255 and g == 255 and b == 255) or (r == 0 and g == 0 and b == 0)):
                    self.image.putpixel(((self.offset_x+self.x)%size[0], (self.offset_y+self.y)%size[1]), (r,g,b))

                # Changing color
                brightness = max(round(rgb_to_hsv(self.color)[1] - 0.1, 1), 0)
                self.color = hsv_to_rgb(rgb_to_hsv(self.color)[0], brightness, rgb_to_hsv(self.color)[2])

                # if we are on a spot
                if [self.offset_x + self.x, self.offset_y + self.y] in self.source_spots:
                    real_spawn = self.find_spawn([self.offset_x + self.x,self.offset_y + self.y])
                    self.base_color = real_spawn.color
                    self.color = self.base_color

                    # remove spawn from list
                    for point in real_spawn.points:
                        self.source_spots.remove(point)
                    self.spawns.remove(real_spawn)
                # finaly, we draw the grid
                self.draw_grid()
        if not action:
            self.speed=max(self.speed-1, MIN_SPEED)

    def draw_grid(self):
        for i in range(0,self.model.width):
            for j in range(0,self.model.height):
                x = (self.offset_x + i + size[0])%size[0]
                y = (self.offset_y + j + size[1])%size[1]
                c = self.image.getpixel((x,y))
                r = c[0]/255.
                g = c[1]/255.
                b = c[2]/255.
                self.model.set_pixel(j, i, [r, g ,b])
        for spawn in self.source_spots:
            if (self.offset_x <= spawn[0] < self.offset_x+self.model.width) and (self.offset_y <= spawn[1] < self.offset_y+self.model.height):
                real_spawn = self.find_spawn(spawn)
                for point in real_spawn.points:
                    self.model.set_pixel(point[1]-self.offset_y,point[0]-self.offset_x,real_spawn.color)

        if self.color == (1.0, 1.0, 1.0):
            self.model.set_pixel(self.y, self.x, 'black')

    def run(self):
        # Update the screen every second.
        rate = Rate(1000.0)

        while self.state is not 'end':
            self.event()
            time.sleep(0.25/self.speed)
        #self.image.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Do something :D')
    LostInSpace(parser).start()
