from Automeno.Types import *
from Automeno.DefaultComponents import *
from Automeno.ComponentFactory import *

from midiutil import MIDIFile

midi_file = MIDIFile(numTracks=1, removeDuplicates=True, eventtime_is_ticks=True)
midi_file.addTempo(0, 0, 120)
midi_file.addProgramChange(0, 0, 0, 1)

file_component = AutomenoComponentFactory("FileCharacter", { "FileName": "main.py" })
character_to_note_component = AutomenoComponentFactory("CharacterToNote", { "PlayNote": Note(Pitch(Key.C, 4), Volume(100), 960 // 2), "PlayCharacters": "aeiou" })
channel_component = AutomenoComponentFactory("Channel", { "Channel": 0 })

character_to_note_component.inports["Character"].connect_outport(file_component.outports["Character"])
channel_component.inports["Notes"].connect_outport(character_to_note_component.outports["Notes"])

for tick in range(0, 960 * 30, 960 // 2):
    notes = channel_component.evaluate()

    for note in notes:
        midi_file.addNote(0, channel_component.parameters["Channel"], note.pitch.midi_pitch(), tick, note.tick_length, note.volume.volume)

    file_component.reset()
    character_to_note_component.reset()
    channel_component.reset()

with open("test.midi", "wb") as f:
    midi_file.writeFile(f)
