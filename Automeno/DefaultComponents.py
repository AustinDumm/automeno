from Automeno.AutomenoTypes import *
from Automeno.AutomenoComponentFactory import AutomenoComponentDelegate
from Automeno.AutomenoComponent import AutomenoComponentProtocol

@AutomenoComponentDelegate("FileCharacter")
class FileCharacterComponentProtocol(AutomenoComponentProtocol):
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
class CharacterToNoteComponentProtocol(AutomenoComponentProtocol):
    def inports():
        return { "Character": str }

    def outports():
        return { "Note": Note }

    def parameters_types():
        return { "PlayNote": Note, "PlayCharacters": str }

    def evaluate_generator(inports, parameters):
        while True:
            character = "".join(inports["Character"].evaluate())
            if character in parameters["PlayCharacters"]:
                yield { "Note": parameters["PlayNote"] }
            else:
                yield { "Note": None }

