#!/usr/bin/env python
"""
Digital Art Jam
"""

from arbalet.core import Application, Rate
import pygame, argparse


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
                        print self.color


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Do something :D')
    LostInSpace(parser).start()