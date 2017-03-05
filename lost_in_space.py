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
from pygame import mixer
from threading import Thread

from spawn import Spawn

#size must be greater than the table size
size = 25,25
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
        self.spawns = []
        self.speed = 1
        self.fade = 1
        self.vector = None
        self.color_level = [0]*6
        self.last_spawn_color = 0
        print self.color_level
        print "State: init"

    def find_spawn(self, coord):
        for spawn in self.spawns:
            if coord in spawn.points:
                return spawn

    def spawn_source(self,position, parent = None, color=None):
        new_spawn=Spawn(size, position, parent,color)
        self.spawns.append(new_spawn)

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
            self.vector = 'up'
            action = True
        elif keys[K_DOWN]:
            self.offset_y = (self.offset_y + 1) % size[1]
            self.vector = 'down'
            action = True
        elif keys[K_RIGHT]:
            self.offset_x = (self.offset_x + 1) % size[0]
            self.vector = 'right'
            action = True
        elif keys[K_LEFT]:
            self.offset_x = (self.offset_x - 1) % size[0]
            self.vector = 'left'
            action = True
        elif keys[K_SPACE]:
            if self.state == 'init':
                with self.model:
                    # set initial color
                    self.model.set_pixel(self.y, self.x, (1.0,1.0,1.0))
                    self.color = self.model.get_pixel(self.y, self.x)
                    self.base_color = self.color

                    # spawn first stop near the player
                    self.spawn_source([self.offset_x + self.x, self.offset_y + self.y + 2], color=0)
                    self.spawn_source([self.offset_x + self.x - 2, self.offset_y + self.y + 1], color=1)
                    self.spawn_source([self.offset_x + self.x - 2, self.offset_y + self.y - 1], color=2)
                    self.spawn_source([self.offset_x + self.x, self.offset_y + self.y - 2], color=3)
                    self.spawn_source([self.offset_x + self.x + 2, self.offset_y + self.y + 1], color=4)
                    self.spawn_source([self.offset_x + self.x + 2, self.offset_y + self.y - 1], color=5)
                    print "State: running"
                    self.state = 'running'
                    action = True

        if keys[K_ESCAPE]:
            self.state = 'end'
            print "State end"
            return
        if not action:
            self.speed = max(self.speed/1.2, MIN_SPEED)
            self.fade = max(self.fade/1.2, 1)
            if self.speed!=MIN_SPEED:
                if self.vector=='up':
                    self.offset_y = (self.offset_y - 1) % size[1]
                elif self.vector=='down':
                    self.offset_y = (self.offset_y + 1) % size[1]
                elif self.vector=='left':
                    self.offset_x = (self.offset_x - 1) % size[0]
                elif self.vector=='right':
                    self.offset_x = (self.offset_x + 1) % size[0]
                action = True
        if self.state == 'init':
            return
            # self.arbalet.user_model.write("Draw me", 'blue')
        elif self.state == 'running' and action:
            with self.model:
                # Changing color
                brightness = max(rgb_to_hsv(self.color)[1] - 1./self.fade, 0)
                self.color = hsv_to_rgb(rgb_to_hsv(self.color)[0], brightness, rgb_to_hsv(self.color)[2])
                collide_spawn = None
                # if we are on a spot
                x = (self.offset_x + self.x)%size[0]
                y = (self.offset_y + self.y)%size[1]
                for spawn in self.spawns:
                    if (x, y) == (spawn.x, spawn.y):
                        collide_spawn = spawn
                if collide_spawn is not None:
                    spawn = collide_spawn
                    self.last_spawn_color = spawn.color
                    #print self.last_spawn_color
                    self.base_color = spawn.color
                    r = int(round(spawn.color[0] * 255))
                    g = int(round(spawn.color[1] * 255))
                    b = int(round(spawn.color[2] * 255))
                    self.image.putpixel(((self.offset_x + self.x) % size[0], (self.offset_y + self.y) % size[1]),
                                        (r, g, b))
                    self.color = self.base_color

                    # play sound
                    sound = spawn.get_sound(self.color_level[spawn.color_id])
                    sound.play()
                    sound.fadeout(3000)

                    # draw spawn
                    points = spawn.get_points(self.color_level[spawn.color_id], size)
                    for point in points:
                        self.image.putpixel((point[0], point[1]),(r, g, b))
                    self.spawns.remove(spawn)

                    # generate two new spawns
                    random.seed()
                    self.spawn_source([random.randint(0,size[0]),random.randint(0,size[1])],parent=spawn)
                    self.spawn_source([random.randint(0, size[0]), random.randint(0, size[1])])

                    # get information about speed and fading
                    self.speed = spawn.get_speed(self.color_level[spawn.color_id])
                    self.fade = spawn.get_fading(self.color_level[spawn.color_id])

                    self.color_level[spawn.color_id] = min(self.color_level[spawn.color_id]+1, 3)

                # else we tranform the current color
                else:
                    # transforming player color to PIL RGB
                    r = int(round(self.color[0] * 255))
                    g = int(round(self.color[1] * 255))
                    b = int(round(self.color[2] * 255))

                    # we only print on the image if we still have color
                    if not (rgb_to_hsv(self.color)[0] == 0.):
                        actual_color = self.image.getpixel(
                            ((self.offset_x + self.x) % size[0], (self.offset_y + self.y) % size[1]))
                        if actual_color != (255, 255, 255):
                            r, g, b = self.mix_color((r, g, b), (actual_color[0], actual_color[1], actual_color[2]))
                        self.image.putpixel(((self.offset_x + self.x) % size[0], (self.offset_y + self.y) % size[1]),
                                            (r, g, b))
                    # diffusion on the sides with bluuuueee !   
                        if self.last_spawn_color == [0, 0.04705, 0.38823]: # blue is hard-coded
                            #print "fuuuuuusioooon"
                            tmp_brightness = max(rgb_to_hsv(self.color)[1] -5./self.fade, 0)
                            tmp_color = hsv_to_rgb(rgb_to_hsv(self.color)[0], tmp_brightness, rgb_to_hsv(self.color)[2])


                            r = int(round(tmp_color[0] * 255))
                            g = int(round(tmp_color[1] * 255))
                            b = int(round(tmp_color[2] * 255))

                            #r, g, b = self.mix_color((r, g, b), (actual_color[0], actual_color[1], actual_color[2]))

                            if self.vector ==  'up':
                                self.image.putpixel(((self.offset_x + self.x+1) % size[0],
                                    (self.offset_y + self.y+1) % size[1]),
                                            (r, g, b))
                                self.image.putpixel(((self.offset_x + self.x-1) % size[0],
                                    (self.offset_y + self.y+1) % size[1]),
                                            (r, g, b))
                            elif self.vector == 'down':
                                self.image.putpixel(((self.offset_x + self.x+1) % size[0],
                                    (self.offset_y + self.y-1) % size[1]),
                                            (r, g, b))
                                self.image.putpixel(((self.offset_x + self.x-1) % size[0],
                                    (self.offset_y + self.y-1) % size[1]),
                                            (r, g, b))
                            elif self.vector == 'left':
                                self.image.putpixel(((self.offset_x + self.x+1) % size[0],
                                    (self.offset_y + self.y+1) % size[1]),
                                            (r, g, b))
                                self.image.putpixel(((self.offset_x + self.x+1) % size[0],
                                    (self.offset_y + self.y-1) % size[1]),
                                            (r, g, b))
                            elif self.vector == 'right':
                                self.image.putpixel(((self.offset_x + self.x-1) % size[0],
                                    (self.offset_y + self.y+1) % size[1]),
                                            (r, g, b))
                                self.image.putpixel(((self.offset_x + self.x-1) % size[0],
                                    (self.offset_y + self.y-1) % size[1]),
                                            (r, g, b))

                    else:
                        self.color=(1.0, 1.0, 1.0)
                        for i in range(len(self.color_level)):
                            self.color_level[i] = 0
                        self.speed = max(self.speed / 1.2, MIN_SPEED)

        # finaly, we draw the grid
        self.draw_grid()

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
        #if abs(spawn[0] - (self.offset_x + self.x)%size[0]) <= self.model.width/2 and abs(spawn[1] - (self.offset_y + self.y)%size[1]) <= self.model.height/2:
        for spawn in self.spawns:
            try:
                self.model.set_pixel((spawn.y-self.offset_y+size[1])%size[1],(spawn.x-self.offset_x+size[0])%size[0],spawn.color)
            except:
                pass
        if self.color == (1.0, 1.0, 1.0):
            self.model.set_pixel(self.y, self.x, 'black')

    def run(self):
        # Update the screen every second.
        rate = Rate(1000.0)

        while self.state is not 'end':
            self.event()
            time.sleep(0.18/self.speed)
        self.image.resize((1000,1000)).show()
        self.model.set_all('black')
        #self.arbalet.user_model.write("Digital Art Jam", 'blue')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Do something :D')
    LostInSpace(parser).start()
