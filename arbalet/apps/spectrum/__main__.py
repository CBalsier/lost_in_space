import argparse
from .spectrum import SpectrumAnalyser

parser = argparse.ArgumentParser(description='Musical spectrum display for the default system audio input')
parser.add_argument('-v', '--vertical',
                    action='store_const',
                    const=True,
                    default=False,
                    help='The spectrum must be vertical (less bands, more bins)')
SpectrumAnalyser(parser).start()

