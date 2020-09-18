from Automeno.Types import DictSerializable
from Automeno.Component import *
from Automeno.ComponentFactory import AutomenoComponentFactory
from midiutil import MIDIFile
from functools import reduce
import json

class Macheno(DictSerializable):
    percussion_channel = 9

    def __init__(self):
        self.components = {}
        self.channels_keys = []

    def find_component(self, name):
        if name in self.components:
            return self.components[name]

        return None

    def add_component(self, name, component):
        self.components[name] = component

    def add_channel(self, name, channel):
        self.components[name] = channel
        self.channels_keys.append(name)

    def num_tracks_needed(self):
        num_drums_tracks = len(list(filter(lambda channel_key: "Track" in self.components[channel_key].parameters and self.components[channel_key].parameters["Track"] == Macheno.percussion_channel, self.channels_keys)))
        return max(num_drums_tracks, (len(self.components) // 16) + 1)

    def run(self, file_name):
        print(self.num_tracks_needed())
        midi_file = MIDIFile(numTracks=self.num_tracks_needed(), removeDuplicates=True, eventtime_is_ticks=True)

        for key in self.channels_keys:
            channel = self.components[key]
            midi_file.addProgramChange(channel.parameters["Track"], channel.parameters["Channel"], 0, channel.parameters["Program"])

        for tick in range(0, 960 * 30, 960 // 2):
            for channel_key in self.channels_keys:
                channel = self.components[channel_key]
                notes = channel.evaluate(tick)

                for note in notes:
                    midi_file.addNote(0, channel.parameters["Channel"], note.pitch.midi_pitch(), tick, note.tick_length, note.volume.volume)

            for component in self.components.values():
                component.reset()

        with open(file_name, "wb") as f:
            midi_file.writeFile(f)

    def update_self(self, dictionary):
        new_macheno = Macheno.deserialize(dictionary)
        self.components = new_macheno.components
        self.channels_keys = new_macheno.channels_keys

    def serialized_links(self):
        format_link = lambda outport, inport: "{}:{}->{}:{}".format(outport.component.name, outport.name, inport.component.name, inport.name)
        pairs_for_inport = lambda inport: list(map(lambda outport: (outport, inport), inport.connected_outports))
        serialized_links_for_inport = lambda inport: format_link(*pairs_for_inport(inport))
        serialized_links_for_inport = lambda inport: list(map(lambda pair: format_link(*pair), pairs_for_inport(inport)))
        serialized_links_for_component = lambda component: list(reduce(lambda acc, inport: acc + serialized_links_for_inport(inport), component.inports.values(), []))
        return list(reduce(lambda acc, component: acc + serialized_links_for_component(component), self.components.values(), []))

    def serialize(obj):
        return { "components": dict(map(lambda name_component: (name_component[0], Component.serialize(name_component[1])), obj.components.items())),\
                 "channels_keys": obj.channels_keys,
                 "links": obj.serialized_links() }

    def deserialize(dictionary):
        macheno = Macheno()
        for key, value in dictionary["components"].items():
            if key in dictionary["channels_keys"]:
                macheno.add_channel(key, Component.deserialize(value))
            else:
                macheno.add_component(key, Component.deserialize(value))

        for link in dictionary["links"]:
            link_split = link.split("->")
            outport_split = link_split[0].split(":")
            inport_split = link_split[1].split(":")
            macheno.components[inport_split[0]].inports[inport_split[1]].connect_outport(macheno.components[outport_split[0]].outports[outport_split[1]])

        return macheno


