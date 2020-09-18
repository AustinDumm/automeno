import json
from Automeno.Types import *
from Automeno.ComponentFactory import _AUTOMENO_COMPONENT_DELEGATES

class AutomenoComponentProtocol:
    def inports():
        raise NotImplementedError("Must subclass AutomenoComponentProtocol")
    def outports():
        raise NotImplementedError("Must subclass AutomenoComponentProtocol")
    def parameters_types():
        raise NotImplementedError("Must subclass AutomenoComponentProtocol")
    def evaluate_generator(inports, parameters):
        raise NotImplementedError("Must subclass AutomenoComponentProtocol")


class Port:
    def __init__(self, name, port_type, component):
        self.name = name
        self.port_type = port_type
        self.component = component

    def evaluate(self, tick):
        raise NotImplementedError("Must subclass Port")


class OutPort(Port):
    def evaluate(self, tick):
        return self.component.evaluate_outport(self.name, tick)

class InPort(Port):
    def __init__(self, name, port_type, component):
        super().__init__(name, port_type, component)
        self.connected_outports = []

    def connect_outport(self, outport):
        if self.port_type != outport.port_type:
            raise Exception("Mismatched In/OutPort Type: {} != {}".format(self.port_type, outport.port_type))

        self.connected_outports.append(outport)

    def evaluate(self, tick):
        nested_list = list(map(lambda outport: outport.evaluate(tick), self.connected_outports))
        return [value for element in nested_list for value in element]


class Component(DictSerializable):
    def __init__(self, name, delegate, delegate_name, parameters):
        self.name = name
        self.delegate_name = delegate_name
        self.inports = dict(map(lambda key_value: (key_value[0], InPort(key_value[0], key_value[1], self)), delegate.inports().items()))
        self.outports = dict(map(lambda key_value: (key_value[0], OutPort(key_value[0], key_value[1], self)), delegate.outports().items()))
        self.parameters = parameters

        if not self.valid(delegate.parameters_types()):
            raise Exception("Invalid Component Parameters: {}".format(self.parameters))

        self.evaluate_generator = delegate.evaluate_generator(self.inports, parameters)
        self.current_evaluation = None

    def valid(self, parameters_types):
        for key, value in self.parameters.items():
            if key not in parameters_types or parameters_types[key] != type(value):
                return False

        return True

    def reset(self):
        self.current_evaluation = None

    def evaluate(self, tick):
        if self.current_evaluation == None:
            self.current_evaluation = next(self.evaluate_generator)
            self.current_evaluation = self.evaluate_generator.send(tick)

        return self.current_evaluation

    def evaluate_outport(self, outport_name, tick):
        return self.evaluate(tick)[outport_name]

    def serialize(obj):
        parameters = {}
        for name, value in obj.parameters.items():
            if callable(getattr(type(value), "serialize", None)):
                parameters[name] = type(value).serialize(value)
            else:
                parameters[name] = value

        return { "name": obj.name,\
                 "delegate_name": obj.delegate_name,\
                 "parameters": parameters }

    def deserialize(dictionary):
        delegate = _AUTOMENO_COMPONENT_DELEGATES[dictionary["delegate_name"]]
        parameter_types = delegate.parameters_types()
        raw_parameters = dictionary["parameters"]
        finished_parameters = {}
        for key, parameter_type in parameter_types.items():
            if parameter_type == type(raw_parameters[key]):
                finished_parameters[key] = raw_parameters[key]
            else:
                parameter_object = parameter_type.deserialize(raw_parameters[key])
                finished_parameters[key] = parameter_object

        return Component(dictionary["name"], delegate, dictionary["delegate_name"], finished_parameters)


