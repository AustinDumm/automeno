
_AUTOMENO_COMPONENT_DELEGATES = {}

def AutomenoComponentDelegate(name):
    def process_class(cls):
        _AUTOMENO_COMPONENT_DELEGATES[name] = cls
        
        return cls

    return process_class

def AutomenoComponentFactory(name, delegate_name, parameters):
    from Automeno.Component import Component
    if delegate_name not in _AUTOMENO_COMPONENT_DELEGATES:
        raise Exception("Delegate {} does not exist".format(delegate_name))

    return Component(name, _AUTOMENO_COMPONENT_DELEGATES[delegate_name], delegate_name, parameters)

