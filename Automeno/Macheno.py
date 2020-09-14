from Automeno.Component import *
from Automeno.ComponentFactory import AutomenoComponentFactory


class Macheno():
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

