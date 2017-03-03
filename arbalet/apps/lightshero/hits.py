from pygame import K_F1, K_F2, K_F3, K_F4, K_F5, KEYDOWN, KEYUP, JOYBUTTONDOWN

# Import a bunch of modules to get X11 keyboards event without opening a window (threaded)
from Xlib import X, display
from Xlib.ext import record
from Xlib.protocol import rq
from threading import Thread, Lock

# event.detail mapping of keys
# TODO: different for each machine?
X11_F1 = 67
X11_F2 = 68
X11_F3 = 69
X11_F4 = 70
X11_F5 = 71

class UserHits():
    """
    This is the class counting the score of the user and returning pressed keys
    This is normally pretty simple but since it is not possible to read keys from no window, this is a hack to
    get x11 events making the class less understandable. A X11 event recorder is started in a thread and updates self.keys

    TODO: add some tolerance with the hit window
    """
    #hit_window = {'easy': 0.2, 'medium': 0.18, 'difficult': 0.16, 'expert': 0.14 }
    # More precise hit window: https://raw.githubusercontent.com/fofix/fofix/master/doc/old/hitwindows.htm

    def __init__(self, num_lanes, arbalet, sound, simulate_player):
        self.simulate_player = simulate_player
        self.sound = sound
        self.sliding_failures = -50  # Starting with negative will give some extra time before starting
        self.window_failures = 25  # Number of consecutive errors accepted
        self.score = 0
        self.arbalet = arbalet
        self.max_score = 0  # measures the maximum score that the user could have
        self.num_lanes = num_lanes
        self.active_notes = [False]*num_lanes
        self.keys = [False]*num_lanes
        self.keys_lock = Lock()

        ####### START X11 KEY RECORDER
        ####### thank you http://sourceforge.net/p/python-xlib/code/HEAD/tree/trunk/examples/put_selection.py
        self.record_dpy = display.Display()
        if not self.record_dpy.has_extension("RECORD"):
            print("X11 RECORD extension not found, the game will not work without GUI")
            self.x11_events = False
        else:
            self.x11_events = True
            self.ctx = self.record_dpy.record_create_context(0, [record.AllClients],
                                                             [{ 'core_requests': (0, 0),
                                                                 'core_replies': (0, 0),
                                                                 'ext_requests': (0, 0, 0, 0),
                                                                 'ext_replies': (0, 0, 0, 0),
                                                                 'delivered_events': (0, 0),
                                                                 'device_events': (X.KeyPress, X.MotionNotify),
                                                                 'errors': (0, 0),
                                                                 'client_started': False,
                                                                 'client_died': False, }])
            def threaded_recorder(): self.record_dpy.record_enable_context(self.ctx, self.update_keys)
            self.recorder = Thread(None, threaded_recorder)
            self.recorder.setDaemon(True)
            self.recorder.start()
        ###############################

    def close(self):
        if self.x11_events:
            self.record_dpy.record_free_context(self.ctx)

    def set_note(self, num_lane, active):
        self.active_notes[num_lane] = active

    def update_keys(self, reply=None):
        """
        Update the map self.keys according to user inputs.
        It uses either the x11 method or the pygame events
        :reply: If the x11 method is used, this is the message returned from x11
        """
        with self.keys_lock:
            if reply:  # Use x11 events
                data = reply.data
                while len(data):
                    evt, data = rq.EventField(None).parse_binary_value(data, self.record_dpy.display, None, None)
                    if evt.type in [X.KeyPress, X.KeyRelease]:
                        if evt.detail==X11_F1:
                            self.keys[0] = evt.type==X.KeyPress
                        elif evt.detail==X11_F2:
                            self.keys[1] = evt.type==X.KeyPress
                        elif evt.detail==X11_F3:
                            self.keys[2] = evt.type==X.KeyPress
                        elif evt.detail==X11_F4:
                            self.keys[3] = evt.type==X.KeyPress
                        elif evt.detail==X11_F5:
                            self.keys[4] = evt.type==X.KeyPress
            else:  # Use pygame events
                for evt in self.arbalet.events.get():
                    if evt.type in [KEYDOWN, KEYUP]:
                        if evt.key==K_F1:
                            self.keys[0] = evt.type==KEYDOWN
                        elif evt.key==K_F2:
                            self.keys[1] = evt.type==KEYDOWN
                        elif evt.key==K_F3:
                            self.keys[2] = evt.type==KEYDOWN
                        elif evt.key==K_F4:
                            self.keys[3] = evt.type==KEYDOWN
                        elif evt.key==K_F5:
                            self.keys[4] = evt.type==KEYDOWN
                    elif evt.type == JOYBUTTONDOWN:
                        self.switch_simulation()

            for event in self.arbalet.touch.get():
                if event['key']==1:
                    self.keys[0] = event['type']=='down'
                elif event['key']==2:
                    self.keys[1] = event['type']=='down'
                elif event['key']==3:
                    self.keys[2] = event['type']=='down'
                elif event['key']==4:
                    self.keys[3] = event['type']=='down'
                elif event['key']==5:
                    self.keys[4] = event['type']=='down'

    def switch_simulation(self):
        self.simulate_player = not self.simulate_player
        if self.simulate_player:
            self.set_playing_well(True)

    def set_playing_well(self, playing_well):
        """
        Call this method each time a note must be played,
        :param sucess: True if the user has correctly played this song, False otherwise
        :return:
        """
        if playing_well:
            self.sliding_failures = 0
            self.sound.set_playing_well(True)
        else:
            self.sliding_failures = min(self.sliding_failures + 1, self.window_failures)
            if self.sliding_failures == self.window_failures:
                self.sound.set_playing_well(False)

    def get_pressed_keys(self):
        """
        Count score and return the pressed lanes
        :return: vector of one boolean per lane True if the corresponding lane is being pressed
        """
        # 1. Get pressed keys
        self.update_keys()

        # 2. Update the score and the maximum score
        playing_well = True
        must_update = False
        for lane in range(self.num_lanes):
            if self.keys[lane] and self.active_notes[lane]:
                # Playing while he must
                self.score += 10
                must_update = True
            elif self.keys[lane] and not self.active_notes[lane]:
                # Playing while he must not
                self.score -= 2
                playing_well = False
                must_update = True
            elif not self.keys[lane] and self.active_notes[lane]:
                # Not playing while he must
                playing_well = False
                must_update = True

            if self.active_notes[lane]:
                self.max_score += 10
        if must_update and not self.simulate_player:
            self.set_playing_well(playing_well)
        return self.keys


