"""
    Arbalet - ARduino-BAsed LEd Table

    Arbalet client
    Client for controlling Arbalet over the network

    Copyright 2015 Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""

import zmq
from threading import Thread
from . rate import Rate

__all__ = ['Arbaclient']

class Arbaclient(Thread):
    def __init__(self, arbalet, server='127.0.0.1', port=33400, rate=30, autorun=True):
        Thread.__init__(self)
        self.setDaemon(True)
        self.server = server
        self.port = str(port)
        self.running = True
        self.rate = Rate(rate)
        self.arbalet = arbalet

        # Network-related attributes
        self.context = zmq.Context()
        self.sender = None

        if autorun:
            self.start()

    def connect(self):
        if not self.sender:
            self.sender = self.context.socket(zmq.PAIR)
            self.sender.connect("tcp://{}:{}".format(self.server, self.port))

    def send_model(self):
        self.sender.send_json(self.arbalet.end_model.to_json())

    def receive_touch(self):
        touch_frame = self.sender.recv_json()
        touch_int = touch_frame[0]
        touch_booleans = touch_frame[1]
        self.arbalet.touch.create_event(touch_int, touch_booleans)

    def close(self, reason='unknown'):
        self.running = False

    def run(self):
        self.connect()
        while self.running:
            self.send_model()
            self.receive_touch()
            self.rate.sleep()
        self.sender.close()
