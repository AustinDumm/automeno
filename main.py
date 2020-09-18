from Automeno.Types import *
from Automeno.DefaultComponents import *
from Automeno.ComponentFactory import *
from Automeno.Macheno import *
from Automeno.Interactive import *

from midiutil import MIDIFile

midi_file = MIDIFile(numTracks=1, removeDuplicates=True, eventtime_is_ticks=True)
midi_file.addTempo(0, 0, 120)

interactive(Macheno())

