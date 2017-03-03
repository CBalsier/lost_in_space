#!/usr/bin/env python
"""
    simpleTester.py - simple Arbalet tester.
    Copyright 2015 Thierry Chantier
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html

    Arbalet - ARduino-BAsed LEd Table
    Copyright 2015 Thierry Chantier, Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""

from arbalet.core import Application, Rate
import pygame, argparse


class SimpleTester(Application):
    def __init__(self, argparser):
        Application.__init__(self, argparser)
        self.colors = ['red', 'green', 'blue']
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
            self.model.set_pixel(self.x,self.y, self.colors[0])
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
    parser = argparse.ArgumentParser(
        description='Light every pixel one by one for hardware address debuging purposes. Columns are filled in first progressively, then rows. All pixels in a column share the same color.')
    SimpleTester(parser).start()