from Automeno.Macheno import Macheno
from Automeno.Types import *
from Automeno.ComponentFactory import _AUTOMENO_COMPONENT_DELEGATES
from Automeno.ComponentFactory import AutomenoComponentFactory
from collections import defaultdict
from functools import reduce

_command_dictionary = defaultdict(lambda: _command_not_found)
def _command_not_found():
    return "Command not found"

def AutomenoInteractiveCommand(name):
    def process_function(fn):
        _command_dictionary[name] = fn
        return fn
    return process_function

def AutomenoInteractiveArguments(arguments):
    def process_function(fn):
        def run_function(*args):
            if type(args[0]) != Macheno:
                raise Exception("AutomenoInteractiveCommand failed to provide Macheno")
            if len(arguments) + 1 != len(args):
                return "Invalid number of commmand arguments: {}".format(arguments)

            for i, (key, value) in enumerate(arguments):
                if args[i + 1] != None and type(args[i + 1]) != value:
                    return "Invalid command arguments: {}".format(arguments)

            return fn(*args)
        return run_function
    return process_function

@AutomenoInteractiveCommand("help")
def _command_help(*args):
    return _command_dictionary.keys()

@AutomenoInteractiveCommand("list")
@AutomenoInteractiveArguments([("Item Type", str)])
def _command_list(*args):
    macheno = args[0]
    item_type = args[1]
    if item_type == "components":
        return str(macheno.components.keys())
    elif item_type == "channels":
        return str(macheno.channels_keys)
    elif item_type == "links":
        list_string = ""
        for component_key in macheno.components.keys():
            list_string += "{}\n".format(component_key)
            component = macheno.components[component_key]
            for inport_key in component.inports.keys():
                inport = component.inports[inport_key]
                for outport in inport.connected_outports:
                    list_string += "\t{}->{}\n".format(outport.name, inport.name)

        return list_string
    else:
        return "Invalid item type [component | channels | links]"


@AutomenoInteractiveCommand("create")
@AutomenoInteractiveArguments([("[component | channel]", str), ("name", str), ("<component_delegate>", str)])
def _command_create(*args):
    macheno = args[0]
    item_type = args[1]
    item_name = args[2]
    delegate_name = args[3]

    if item_type == "component":
        if delegate_name not in _AUTOMENO_COMPONENT_DELEGATES:
            return "Unknown delegate name"

        delegate = _AUTOMENO_COMPONENT_DELEGATES[delegate_name]
        parameters = delegate.parameters_types()
        parameter_values = {}
        for key, value in parameters.items():
            parameter_values[key] = eval(input("{} ({}):".format(key, value)))

        component = AutomenoComponentFactory(delegate_name, parameter_values)
        macheno.add_component(item_name, component)
    elif item_type == "channel":
        delegate = _AUTOMENO_COMPONENT_DELEGATES["Channel"]
        parameters = delegate.parameters_types()
        parameter_values = {}
        for key, value in parameters.items():
            parameter_values[key] = value(input("{} ({}):".format(key, value)))

        channel = AutomenoComponentFactory("Channel", parameter_values)
        macheno.add_channel(item_name, channel)
    else:
        return "item_type must be \"component\" or \"channel\""

    return "{} \"{}\" added".format(item_type, item_name)

@AutomenoInteractiveCommand("delete")
def _command_delete(*args):
    pass

@AutomenoInteractiveCommand("link")
@AutomenoInteractiveArguments([("outport", str), ("inport", str)])
def _command_link(*args):
    macheno = args[0]
    outport_path = args[1].split(":")
    inport_path = args[2].split(":")
    inport = macheno.find_component(inport_path[0]).inports[inport_path[1]]
    outport = macheno.find_component(outport_path[0]).outports[outport_path[1]]

    inport.connect_outport(outport)

    return "{} -> {} created".format(outport_path, inport_path)

@AutomenoInteractiveCommand("unlink")
def _command_unlink(*args):
    pass

@AutomenoInteractiveCommand("run")
@AutomenoInteractiveArguments([("file_name", str)])
def _command_run(*args):
    macheno = args[0]
    file_name = args[1]
    macheno.run(file_name)
    return "Created {}".format(file_name)

@AutomenoInteractiveCommand("export")
@AutomenoInteractiveArguments([("file_name", str)])
def _command_export(*args):
    macheno = args[0]
    file_name = args[1]
    print(macheno.serialize())
    return f'Exported to file {file_name}'
    

@AutomenoInteractiveCommand("import")
def _command_import(*args):
    pass

    
def interactive(initial_macheno):
    while True:
        command = input("m:").split(" ")
        
        if command[0] == "exit":
            return

        print_value = _command_dictionary[command[0]](initial_macheno, *command[1:])
        print(print_value)
        

