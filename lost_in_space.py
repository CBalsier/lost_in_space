#!/usr/bin/env python
"""
Digital Art Jam
"""

from arbalet.core import Application, Rate
from arbalet.colors import hsv_to_rgb, rgb_to_hsv
import pygame, argparse
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

    def draw_grid(self):
        for i in range(0,self.model.width):
            for j in range(0,self.model.height):
                x = (self.offset_x + i + size[0])%size[0]
                y = (self.offset_y + j + size[1])%size[1]
                c = self.image.getpixel((x,y))
                r = c[0]/255.
                g = c[1]/255.
                b = c[2]/255.
                self.model.set_pixel(j, i, [r,g,b])

    def run(self):
        # Update the screen every second.
        rate = Rate(1000.0)

        while self.state is not 'end':
            self.event()
        self.image.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Do something :D')
    LostInSpace(parser).start()