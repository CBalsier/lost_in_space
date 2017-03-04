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

#size must be greater than the table size
size = 20,20
MAX_SPEED = 3
MIN_SPEED = 1


class LostInSpace(Application):
    def __init__(self, argparser):
        Application.__init__(self, argparser)
        self.base_color = None
        self.color = (1.0, 1.0, 1.0)
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

    def spawn_source(self,position, parent = None):
        new_spawn=Spawn(size, position, parent)
        self.spawns.append(new_spawn)
        for point in new_spawn.points:
            self.source_spots.append(point)
        print "spawning %s" % str(new_spawn.points)

    def mix_color(self,(r1,g1,b1),(r2,g2,b2)):
        r = (r1+r2)/2
        g = (g2+g1)/2
        b = (b1+b2)/2
        return r,g,b

    def event(self):
        action = False
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            self.offset_y = (self.offset_y - 1) % size[1]
            action = True
        elif keys[K_DOWN]:
            self.offset_y = (self.offset_y + 1) % size[1]
            action = True
        elif keys[K_RIGHT]:
            self.offset_x = (self.offset_x + 1) % size[0]
            action = True
        elif keys[K_LEFT]:
            self.offset_x = (self.offset_x - 1) % size[0]
            action = True
        elif keys[K_ESCAPE]:
            self.state = 'end'
        elif keys[K_SPACE]:
            if self.state == 'init':
                with self.model:
                    # set initial color
                    self.model.set_pixel(self.y, self.x, (1.0,1.0,1.0))
                    self.color = self.model.get_pixel(self.y, self.x)
                    self.base_color = self.color

                    # spawn first stop near the player
                    self.spawn_source([self.offset_x + self.x -2, self.offset_y + self.y])
                    self.spawn_source([self.offset_x + self.x + 2, self.offset_y + self.y])
                    self.spawn_source([self.offset_x + self.x, self.offset_y + self.y - 2])
                    self.spawn_source([self.offset_x + self.x, self.offset_y + self.y + 2])

                    self.state = 'running'
                    action = True

        if self.state == 'init':
            pass
            # self.arbalet.user_model.write("Draw me", 'blue')

        elif self.state == 'running' and action:
            self.speed = min(self.speed+1,MAX_SPEED)
            with self.model:
                # Changing color
                brightness = max(round(rgb_to_hsv(self.color)[1] - 0.1, 1), 0)
                self.color = hsv_to_rgb(rgb_to_hsv(self.color)[0], brightness, rgb_to_hsv(self.color)[2])

                # if we are on a spot
                x = (self.offset_x + self.x)%size[0]
                y = (self.offset_y + self.y)%size[1]
                if [x, y] in self.source_spots:
                    real_spawn = self.find_spawn([x,y])
                    self.base_color = real_spawn.color
                    r = int(round(real_spawn.color[0] * 255))
                    g = int(round(real_spawn.color[1] * 255))
                    b = int(round(real_spawn.color[2] * 255))
                    self.image.putpixel(((self.offset_x + self.x) % size[0], (self.offset_y + self.y) % size[1]),
                                        (r, g, b))
                    self.color = self.base_color

                    # remove spawn from list
                    for point in real_spawn.points:
                        self.source_spots.remove(point)
                    self.spawns.remove(real_spawn)
                    random.seed()
                    self.spawn_source([random.randint(0,size[0]),random.randint(0,size[1])],parent=real_spawn)
                # else we tranform the current color
                else:
                    # transforming player color to PIL RGB
                    r = int(round(self.color[0] * 255))
                    g = int(round(self.color[1] * 255))
                    b = int(round(self.color[2] * 255))

                    # we do not print on the image if we are black ou white
                    if not ((r == 255 and g == 255 and b == 255) or (r == 0 and g == 0 and b == 0)):
                        actual_color = self.image.getpixel(
                            ((self.offset_x + self.x) % size[0], (self.offset_y + self.y) % size[1]))
                        if actual_color != (255, 255, 255):
                            r, g, b = self.mix_color((r, g, b), (actual_color[0], actual_color[1], actual_color[2]))
                        self.image.putpixel(((self.offset_x + self.x) % size[0], (self.offset_y + self.y) % size[1]),
                                            (r, g, b))
                # finaly, we draw the grid
                self.draw_grid()



        if not action:
            self.speed=max(self.speed-1, MIN_SPEED)

    def draw_grid(self):
        #drag from image
        for i in range(0,self.model.width):
            for j in range(0,self.model.height):
                x = (self.offset_x + i + size[0])%size[0]
                y = (self.offset_y + j + size[1])%size[1]
                c = self.image.getpixel((x,y))
                r = c[0]/255.
                g = c[1]/255.
                b = c[2]/255.
                self.model.set_pixel(j, i, [r, g ,b])
        # draw spawn
        for spawn in self.source_spots:

            if abs(spawn[0] - (self.offset_x + self.x)%size[0]) <= self.model.width/2 and abs(spawn[1] - (self.offset_y + self.y)%size[1]) <= self.model.height/2:
                real_spawn = self.find_spawn(spawn)
                print real_spawn
                for point in real_spawn.points:
                    #if (self.offset_x <= point[0] < self.offset_x + self.model.width) and (
                            #self.offset_y <= point[1] < self.offset_y + self.model.height):
                        #self.model.set_pixel(point[1]-self.offset_y,point[0]-self.offset_x,real_spawn.color)
                    #print point
                    self.model.set_pixel((point[1]-self.offset_y + size[0])%size[0],(point[0]-self.offset_x +size[1])%size[1],real_spawn.color)

        if self.color == (1.0, 1.0, 1.0):
            self.model.set_pixel(self.y, self.x, 'black')

    def run(self):
        # Update the screen every second.
        rate = Rate(1000.0)

        while self.state is not 'end':
            self.event()
            time.sleep(0.25/self.speed)
        self.image.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Do something :D')
    LostInSpace(parser).start()
