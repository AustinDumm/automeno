from Automeno.Types import DictSerializable
from Automeno.Component import *
from Automeno.ComponentFactory import AutomenoComponentFactory
from midiutil import MIDIFile
import json

class Macheno(DictSerializable):
    def __init__(self, midi_file):
        self.components = {}
        self.channels_keys = []
        self.midi_file = midi_file

    def find_component(self, name):
        if name in self.components:
            return self.components[name]

        return None

    def add_component(self, name, component):
        self.components[name] = component

    def add_channel(self, name, channel):
        self.midi_file.addProgramChange(channel.parameters["Track"], channel.parameters["Channel"], 0, channel.parameters["Program"])
        self.components[name] = channel
        self.channels_keys.append(name)

    def run(self, file_name):
        for tick in range(0, 960 * 30, 960 // 2):
            for channel_key in self.channels_keys:
                channel = self.components[channel_key]
                notes = channel.evaluate()

                for note in notes:
                    self.midi_file.addNote(0, channel.parameters["Channel"], note.pitch.midi_pitch(), tick, note.tick_length, note.volume.volume)

            for component in self.components.values():
                component.reset()

        with open(file_name, "wb") as f:
            self.midi_file.writeFile(f)

    def update_self(self, dictionary):
        new_macheno = Macheno.deserialize(dictionary)
        self.components = new_macheno.components
        self.channels_keys = new_macheno.channels_keys

    def serialize(obj):
        return { "midi_file": "blah",\
                 "components": dict(map(lambda name_component: (name_component[0], Component.serialize(name_component[1])), obj.components.items())),\
                 "channels_keys": obj.channels_keys }

    def deserialize(dictionary):
        macheno = Macheno(MIDIFile(numTracks=1, removeDuplicates=True, eventtime_is_ticks=True))
        for key, value in dictionary["components"].items():
            if key in dictionary["channels_keys"]:
                macheno.add_channel(key, Component.deserialize(value))
            else:
                macheno.add_component(key, Component.deserialize(value))

        return macheno


