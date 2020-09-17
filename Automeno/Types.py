from enum import IntEnum

class DictSerializable():
    def serialize(obj):
        raise NotImplementedError("Must subclass DictSerializable")
    def deserialize(dictionary):
        raise NotImplementedError("Must subclass DictSerializable")

class Key(DictSerializable, IntEnum):
    C = 0
    C_SHARP = 1
    D = 2
    D_SHARP = 3
    E = 4
    F = 5
    F_SHARP = 6
    G = 7
    G_SHARP = 8
    A = 9
    A_SHARP = 10
    B = 11

    def serialize(obj):
        return int(obj)

    def deserialize(dictionary):
        return Key(dictionary)


class Pitch(DictSerializable):
    pitch_offset = 12

    def __init__(self, key: Key, octave: int):
        self.key = key
        self.octave = octave

    def midi_pitch(self) -> int:
        return self.octave * 12 + self.pitch_offset + self.key

    def serialize(obj):
        return { "key": Key.serialize(obj.key),\
                 "octave": obj.octave }

    def deserialize(dictionary):
        return Pitch(Key.deserialize(dictionary["key"], dictionary["octave"]))


class Volume(DictSerializable):
    min_volume = 0
    max_volume = 127
    def __init__(self, volume: int):
        self.volume = max(self.min_volume, min(self.max_volume, volume))

    def serialize(obj):
        return obj.volume

    def deserialize(dictionary):
        return Volume(dictionary)

class Note(DictSerializable):
    def __init__(self, pitch: Pitch, volume: Volume, tick_length: int):
        self.pitch = pitch
        self.volume = volume
        self.tick_length = tick_length

    def __str__(self):
        return "({}, {}, {}, {})".format(str(self.pitch.key), self.pitch.octave, self.volume.volume, self.tick_length)

    def from_string(string):
        sections = string.strip("()").split[","]
        return Note(Pitch(Key[sections[0]], sections[1]), Volume(sections[2]), sections[3])

    def serialize(obj):
        return { "pitch": Pitch.serialize(obj.pitch),\
                 "volume": Volume.serialize(obj.volume),\
                 "tick_length": obj.tick_length }

    def deserialize(dictionary):
        return Note(Pitch.deserialize(dictionary["pitch"]),\
                Volume.deserialize(dictionary["volume"]),\
                dictionary["volume"])
