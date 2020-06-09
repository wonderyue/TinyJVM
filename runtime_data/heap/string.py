from runtime_data.heap.object import Object


_string_pool = {}


def new_string(class_loader, python_str):
    if (interned_str := _string_pool.get(python_str)) is not None:
        return interned_str
    java_char_array = Object(class_loader.load_class("[C"), list(python_str))
    java_str = class_loader.load_class("java/lang/String").new_object()
    java_str.set_field_value("value", "[C", java_char_array)
    _string_pool[python_str] = java_str
    return java_str


def python_string(java_str):
    char_array = java_str.get_field_value("value", "[C")
    return "".join(char_array.data)


def intern(java_str):
    python_str = python_string(java_str)
    if (interned_str := _string_pool.get(python_str)) is not None:
        return interned_str
    _string_pool[python_str] = java_str
    return java_str
