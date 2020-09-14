from enum import IntEnum

class Key(IntEnum):
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


class Pitch:
    pitch_offset = 12

    def __init__(self, key: Key, octave: int):
        self.key = key
        self.octave = octave

    def midi_pitch(self) -> int:
        return self.octave * 12 + self.pitch_offset + self.key


class Volume:
    min_volume = 0
    max_volume = 127
    def __init__(self, volume: int):
        self.volume = max(self.min_volume, min(self.max_volume, volume))


class Note:
    def __init__(self, pitch: Pitch, volume: Volume, tick_length: int):
        self.pitch = pitch
        self.volume = volume
        self.tick_length = tick_length

    def __str__(self):
        return "({}, {}, {}, {})".format(str(self.pitch.key), self.pitch.octave, self.volume.volume, self.tick_length)

    def from_string(string):
        sections = string.strip("()").split[","]
        return Note(Pitch(Key[sections[0]], sections[1]), Volume(sections[2]), sections[3])
