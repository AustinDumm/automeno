from Automeno.AutomenoTypes import *
from Automeno.DefaultComponents import *
from Automeno.AutomenoComponentFactory import *

file_component = AutomenoComponentFactory("FileCharacter", { "FileName": "main.py" })
character_to_note_component = AutomenoComponentFactory("CharacterToNote", { "PlayNote": Note(Pitch(Key.C, 4), Volume(100), 960 / 2), "PlayCharacters": "aeiou" })
character_to_note_component.inports["Character"].connect_outport(file_component.outports["Character"])

for _ in range(0, 50):
    character = file_component.outports["Character"].evaluate()
    note = character_to_note_component.outports["Note"].evaluate()
    if note == None:
        print("_")
    else:
        print(note.pitch.key)
    file_component.reset()
    character_to_note_component.reset()

