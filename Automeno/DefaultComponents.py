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


@AutomenoComponentDelegate("NoteGenerator")
class NoteGeneratorDelegate(AutomenoComponentProtocol):
    def inports():
        return { "On": bool }

    def outports():
        return { "Notes": [Note] }

    def parameters_types():
        return { "PlayNote": Note,
                 "NeedAllOn": bool }

    def evaluate_generator(inports, parameters):
        tick = 0
        while True:
            if parameters["NeedAllOn"] and all(inports["On"].evaluate(tick)):
                tick = yield { "Notes": [parameters["PlayNote"]] }
            elif not parameters["NeedAllOn"] and any(inports["On"].evaluate(tick)):
                tick = yield { "Notes": [parameters["PlayNote"]] }
            else:
                tick = yield { "Notes": [] }

@AutomenoComponentDelegate("WordExists")
class WordExistsDelegate(AutomenoComponentProtocol):
    def inports():
        return { "Word": str }

    def outports():
        return { "Exists": bool }

    def parameters_types():
        return { "WordToCheck": str,
                 "NeedAllMatch": bool }

    def evaluate_generator(inports, parameters):
        tick = 0
        while True:
            check = inports["Word"].evaluate(tick)
            if parameters["NeedAllMatch"]:
                tick = yield  { "Exists": all(map(lambda word: word in parameters["WordToCheck"], check) )}
            else:
                tick = yield  { "Exists": any(map(lambda word: word in parameters["WordToCheck"], check) )}
            

@AutomenoComponentDelegate("RhythmGenerator")
class RhythmGeneratorDelegate(AutomenoComponentProtocol):
    def inports():
        return {}

    def outports():
        return { "On": bool }

    def parameters_types():
        return { "Equation": str }

    def evaluate_generator(inports, parameters):
        tick = 0
        while True:
            equation = parameters["Equation"]
            value = eval(equation, { "tick": tick })
            tick = yield { "On": value }
                

@AutomenoComponentDelegate("Channel")
class ChannelSinkComponentDelegate(AutomenoComponentProtocol):
    def inports():
        return { "Notes": [Note] }

    def outports():
        return {}

    def parameters_types():
        return { "Channel": int, "Program": int }

    def evaluate_generator(inports, parameters):
        tick = 0
        while True:
            tick = yield inports["Notes"].evaluate(tick)


