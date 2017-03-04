#!/usr/bin/env python
# -*- coding = utf-8 -*-
"""
Digital Art Jam
"""

from arbalet.core import Application, Rate
from arbalet.colors import hsv_to_rgb, rgb_to_hsv
import pygame, argparse, random
from PIL import Image

size = 50,50

class LostInSpace(Application):
    def __init__(self, argparser):
        Application.__init__(self, argparser)
        self.color = None
        self.base_color = None
        # relative coordonate to image center
        self.y = self.height/2
        self.x = self.width/2
        # offset from
        self.offset_y = 0
        self.offset_x = 0
        self.life = 3
        self.model.set_all('white')
        self.state = 'init'
        self.image = Image.new('RGB',size, (255,255,255))
        self.source_spots = []

    def run(self):
        # Update the screen every second.
        rate = Rate(1000.0)
        while self.state is not 'end':
            self.event()
        self.image.show()
        with self.model:
            self.model.set_pixel(self.x,self.y, 'red')
            self.color = self.model.get_pixel(self.x,self.y)
            self.base_color = self.color
        self.source_spots = []
        self.spawn_source([0,0])

    def spawn_source(self,last_position):
        # Random generation
        #color = hsv_to_rgb(random.random(),random.random(), random.random())
        # Random in a list
        #color_list = ['red', 'green', 'blue', 'black']
        #color = color_list[random.randint(0,len(color_list))-1]
        # Debug
        color = 'green'

        # Random spawn
        #position = [random.randint(0,self.model.width),random.randint(0,self.model.height)]#random (test que different de position actuelle)
        # Debug
        position = [2,2]
        #pattern_list =[
                #[[1,1],[0,0],[-1,-1],[1,-1],[-1,1]],
                #[[0,1],[0,-1],[1,0],[-1,0]],
                #[[0,1],[0,-1],[1,0],[3,1],[3,-1],[4,0]]
                #]
                # random dans une liste de formes (=liste de coordonnees)
        #pattern = pattern_list[random.randint(0,len(pattern_list))-1]# random dans une liste de formes (=liste de coordonnees)
        pattern = [0,0]
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
                new_y =self.model.width -1
            self.model.set_pixel(new_x,new_y, color)
            self.source_spots.append([new_x,new_y])
            print self.source_spots

    def event(self):
        for event in self.arbalet.events.get():
            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_UP:
                    self.offset_y -= 1 % size[1]
                elif event.key == pygame.K_DOWN:
                    self.offset_y += 1 % size[1]
                elif event.key == pygame.K_RIGHT:
                    self.offset_x += 1 % size[0]
                elif event.key == pygame.K_LEFT:
                    self.offset_x -= 1 % size[0]
                elif event.key == pygame.K_ESCAPE:
                    self.state = 'end'
                    return
                elif event.key == pygame.K_SPACE:
                    with self.model:
                        # set initial color
                        self.model.set_pixel(self.y, self.x, hsv_to_rgb(0, 1, 1))
                        self.color = self.model.get_pixel(self.y, self.x)
                        self.base_color = self.color
                        self.state = 'running'
                if self.state == 'init':
                    pass
                    #self.arbalet.user_model.write("Draw me", 'blue')
                elif self.state == 'running':
                    with self.model:
                        # Generating image
                        r = int(round(self.color[0] * 255))
                        g = int(round(self.color[1] * 255))
                        b = int(round(self.color[2] * 255))
                        self.image.putpixel(((self.offset_x+self.x)%size[0], (self.offset_y+self.y)%size[1]), (r,g,b))

                        # Changing color
                        value = max(round(rgb_to_hsv(self.color)[2] - 0.2, 1), 0)
                        self.color = hsv_to_rgb(rgb_to_hsv(self.color)[0], rgb_to_hsv(self.color)[1], value)
                        self.draw_grid()
                        
                        # Interact with sources

                        print self.source_spots
                        if [self.x, self.y] in self.source_spots:
                            self.spawn_source([0,0])
    def draw_grid(self):
        for i in range(0,self.model.width):
            for j in range(0,self.model.height):
                x = (self.offset_x + i + size[0])%size[0]
                y = (self.offset_y + j + size[1])%size[1]
                if i == 0 and j == 0:
                    print self.offset_x + i
                    print x, y
                c = self.image.getpixel((x,y))
                r = c[0]/255.
                g = c[1]/255.
                b = c[2]/255.
                self.model.set_pixel(j, i, [r,g,b])



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Do something :D')
    LostInSpace(parser).start()
