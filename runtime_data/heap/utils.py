def lookup_method_in_class(clazz, name, descriptor):
    while clazz:
        for method in clazz.methods:
            if method.name == name and method.descriptor == descriptor:
                return method
        clazz = clazz.super_class
    return None


def lookup_method_in_interfaces(interfaces, name, descriptor):
    for interface in interfaces:
        for method in interface.methods:
            if method.name == name and method.descriptor == descriptor:
                return method
        if (
            method := lookup_method_in_interfaces(
                interface.interfaces, name, descriptor
            )
        ) is not None:
            return method
    return None


PRIMITIVE_TYPE = {
    "void": "V",
    "boolean": "Z",
    "byte": "B",
    "short": "S",
    "int": "I",
    "long": "J",
    "char": "C",
    "float": "F",
    "double": "D",
}

PRIMITIVE_DEFAULT_VALUE = {
    "Z": False,
    "B": 0x00,
    "S": 0,
    "I": 0,
    "J": 0,
    "C": 0,
    "F": 0.0,
    "D": 0.0,
}

ATYPR_2_CLASS_NAME = {
    # AT_BOOLEAN
    4: "[Z",
    # AT_CHAR
    5: "[C",
    # AT_FLOAT
    6: "[F",
    # AT_DOUBLE
    7: "[D",
    # AT_BYTE
    8: "[B",
    # AT_SHORT
    9: "[S",
    # AT_INT
    10: "[I",
    # AT_LONG
    11: "[J",
}


def is_primitive(class_name) -> bool:
    return class_name in PRIMITIVE_TYPE.values()


def get_default_value(descriptor):
    return PRIMITIVE_DEFAULT_VALUE.get(descriptor, None)


def get_array_class_name(class_name):
    return "[" + to_descriptor(class_name)


def get_component_class_name(class_name):
    if class_name in ATYPR_2_CLASS_NAME.values():
        return class_name
    if class_name[0] == "[":
        return to_class_name(class_name[1:])
    raise RuntimeError("Invalid class name of array: " + class_name)


def to_descriptor(class_name):
    """
    class_name -> descriptor:
    [XXX => [XXX
    int  => I
    XXX  => LXXX;
    """
    if class_name[0] == "[":
        return class_name
    return PRIMITIVE_TYPE.get(class_name, "L") + class_name + ";"


def to_class_name(descriptor):
    if descriptor[0] == "[":
        return descriptor
    if descriptor[0] == "L":
        return descriptor[1 : len(descriptor) - 1]
    for class_name, d in PRIMITIVE_TYPE.items():
        if d == descriptor:
            return class_name
    raise RuntimeError("Invalid descriptor: " + descriptor)
