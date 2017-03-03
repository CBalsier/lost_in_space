import midi                    # pip install python-midi # https://github.com/vishnubob/python-midi
import configparser
import time
from collections import deque
from copy import copy

class SongReader():
    """
    This class reads a notes.mid file and produces discrete lines
    Each MIDI event is mapped on a lane, see http://code.google.com/p/fofix/wiki/MidiSectionsMappedOut
    A discrete line contains a state for each lane:
    * background = no event on this lane
    * bump = new note on this lane
    * active = former note still active on this lane
    """
    metadata_filename = 'song.ini'
    notes_filename = 'notes.mid'
    states = ['background', 'bump', 'active']
    # mapping level-> [midi pitch for each lane]
    mapping = {'difficult' : [84, 85, 86, 87, 88],
               'expert': [96, 97, 98, 99, 100],
               'medium': [72, 73, 74, 75, 76],
               'easy': [60, 61, 62, 63, 64]
               }

    def __init__(self, path, num_lanes, level, speed):
        """
        :param path: Path of the folder of the song (should contain song.ini and notes.mid)
        :param num_lanes: deprecated? Format supports only 5 lanes
        :param level: 'difficult', 'easy' ...
        """
        self.num_lanes = num_lanes
        self.level = level
        self.speed = speed
        self.eof = False

        # Config parser
        parser = configparser.ConfigParser()
        parser.read(path+'/'+self.metadata_filename)
        self.name = parser.get('song', 'name')
        self.artist = parser.get('song', 'artist')

        # midi parser
        data = midi.read_midifile(path+'/'+self.notes_filename)
        data.make_ticks_abs() # Change ticks in absolute timestamp
        raw_metadata = data[0] # Raw metadata of midi file
        tempo_event = [e for e in raw_metadata if isinstance(e, midi.events.SetTempoEvent)]
        if len(tempo_event)!=1:
            raise Exception("Not yet able to read this file, I does not support dynamic ticks")
        self.metadata = { "tick_duration": 60/tempo_event[0].get_bpm()/data.resolution }
        self.notes = deque(data[1]) # Actual stream of notes read as a FIFO structure

        self.old_line = None
        self.start = None # Stores when the song started playing
        self.line_id = 0

    def now(self):
        """
        Return the time elapsed from the beginning of the song
        """
        return time.time()-self.start

    def read(self):
        """
        :return: The next line (5 lanes) to be displayed
        """
        if not self.start:
            self.start = time.time()

        line = ['background']*self.num_lanes
        filled = [False]*self.num_lanes       # True if the lane has been filled for this step

        while len(self.notes)>0:
            event = self.notes[0]
            if event.tick*self.metadata['tick_duration'] < self.now():
                # The next event has occurred, consume it and remove it from the FIFO
                self.notes.popleft()
                if isinstance(event, midi.NoteOnEvent):
                    try:
                        lane = self.mapping[self.level].index(event.get_pitch())
                    except:
                        pass
                    else:
                        line[lane] = 'bump'
                        filled[lane] = True
                elif isinstance(event, midi.NoteOffEvent):
                    try:
                        lane = self.mapping[self.level].index(event.get_pitch())
                    except:
                        pass
                    else:
                        line[lane] = 'background'
                        filled[lane] = True
                elif isinstance(event, midi.EndOfTrackEvent):
                    self.eof = True
                    break
            else:
                # The next event will occur later, leave the loop
                break

        # Transform previous bumps in active cells
        if self.old_line:
            for lane in range(self.num_lanes):
                if not filled[lane] and (self.old_line[lane]=='bump' or self.old_line[lane]=='active'):
                    line[lane] = 'active'
                    filled[lane] = True
        self.old_line = copy(line)

        for lane in range(self.num_lanes):
            if not filled[lane] and self.line_id%int(4./3*self.speed)==0:
                line[lane] = 'marker'
                filled[lane] = True

        self.line_id += 1
        return line

