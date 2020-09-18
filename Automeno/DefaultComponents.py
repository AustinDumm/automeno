from Automeno.Types import *
from Automeno.ComponentFactory import AutomenoComponentDelegate
from Automeno.Component import AutomenoComponentProtocol

@AutomenoComponentDelegate("FileCharacter")
class FileCharacterComponentDelegate(AutomenoComponentProtocol):
    def inports():
        return {}

    def outports():
        return { "Character": str }

    def parameters_types():
        return { "FileName": str }

    def evaluate_generator(inports, parameters):
        while True:
            with open(parameters["FileName"], "r") as f:
                character = f.read(1)
                while character:
                    yield { "Character": character }
                    character = f.read(1)


@AutomenoComponentDelegate("CharacterToNote")
class CharacterToNoteComponentDelegate(AutomenoComponentProtocol):
    def inports():
        return { "Character": str }

    def outports():
        return { "Notes": [Note] }

    def parameters_types():
        return { "PlayNote": Note, "PlayCharacters": str }

    def evaluate_generator(inports, parameters):
        while True:
            tick = 0
            character = "".join(inports["Character"].evaluate(tick))
            if character in parameters["PlayCharacters"]:
                tick = yield { "Notes": [parameters["PlayNote"]] }
            else:
                tick = yield { "Notes": [] }

@AutomenoComponentDelegate("Channel")
class ChannelSinkComponentDelegate(AutomenoComponentProtocol):
    def inports():
        return { "Notes": [Note] }

    def outports():
        return {}

    def parameters_types():
        return { "Channel": int, "Program": int, "Track": int }

    def evaluate_generator(inports, parameters):
        tick = 0
        while True:
            tick = yield inports["Notes"].evaluate(tick)


