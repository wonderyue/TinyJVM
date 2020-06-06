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
        if (method:= lookup_method_in_interfaces(
                interface.interfaces, name, descriptor)) is not None:
            return method
    return None
