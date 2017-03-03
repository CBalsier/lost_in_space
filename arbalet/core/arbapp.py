"""
    Arbalet - ARduino-BAsed LEd Table
    Application - Arbalet Application

    All Application for Arbalet should inherit from this class.
    Wanna create an awesome Arbalet application? Start here.

    Copyright 2015 Yoan Mollard - Arbalet project - http://github.com/arbalet-project
    License: GPL version 3 http://www.gnu.org/licenses/gpl.html
"""

from .arbalet import Arbalet
import argparse

__all__ = ['Application']

class Application(object):
    app_declared = False  # True when an Application has been instanciated

    def __init__(self, argparser=None, moke_execution=False, touch_mode='off'):
        if Application.app_declared:
            raise RuntimeError('Application can be instanciated only once')

        Application.app_declared = True
        self.read_args(argparser)
        self.arbalet = Arbalet(not moke_execution and not self.args.no_gui, not moke_execution and self.args.hardware,
                               self.args.server, self.args.brightness, self.args.factor_sim, self.args.config, interactive=False)
        self.arbalet.touch.set_mode('off' if self.args.no_touch else touch_mode)
        self.width = self.arbalet.width
        self.height = self.arbalet.height

        self.init_font(self.model)

    @property
    def model(self):
        return self.arbalet.user_model

    def init_font(self, model):
        try:
            model.set_font(self.arbalet.config['font'], self.arbalet.config['vertical'])
        except KeyError:
            model.set_font()

    def is_interactive(self):
        """
        :return: True if the code is running interactively with IPYTHON, False otherwise
        """
        try:
            __IPYTHON__
        except NameError:
            return False
        else:
            return True

    def read_args(self, argparser):

        if argparser:
            parser = argparser
        else:
            parser = argparse.ArgumentParser(description='This script runs on Arbalet and allows the following arguments:')

        parser.add_argument('-w', '--hardware',
                            action='store_const',
                            const=True,
                            default=False,
                            help='The program must connect directly to Arbalet hardware')
        parser.add_argument('-ng', '--no-gui',
                            action='store_const',
                            const=True,
                            default=False,
                            help='The program must not be simulated on the workstation in a 2D window')
        parser.add_argument('-s', '--server',
                            type=str,
                            nargs='?',
                            const='127.0.0.1',
                            default='',
                            help='Address and port of the Arbaserver sharing hardware (ex: myserver.local:33400, 192.168.0.15, ...)')
        parser.add_argument('-c', '--config',
                            type=str,
                            default='',
                            help='Name of the config file describing the table (.json file), if missing the default config in arbasdk/default.cfg will be selected')
        parser.add_argument('-b', '--brightness',
                            type=float,
                            default=1,
                            help='Brightness, intensity of hardware LEDs between 0.0 (all LEDs off) and 1.0 (all LEDs at full brightness)')
        parser.add_argument('-f', '--factor_sim',
                            type=int,
                            default=40,
                            help='Size of the simulated pixels')
        parser.add_argument('-nt', '--no-touch',
                            action='store_const',
                            const=True,
                            default=False,
                            help='Disable the touch feature. This option has no influence on apps that are not touch-compatible')

        # We parse args normally if running in non-interactive mode, otherwise we ignore args to avoid conflicts with ipython
        self.args = parser.parse_args([] if self.is_interactive() else None)


    def run(self):
        raise NotImplementedError("Application.run() must be overidden")

    def start(self):
        try:
            self.run()
        except:
            self.close("Program raised exception")
            raise
        else:
            self.close("Program naturally ended")

    def close(self, reason='unknown'):
        self.arbalet.close(reason)
