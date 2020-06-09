from runtime_data.heap.utils import (
    is_primitive,
    get_default_value,
)


class Object:
    def __init__(self, clazz, data):
        """
        for Array Object: 
            data: array of elements
        for Class Object:
            data: array of class fields
        """
        self.clazz = clazz
        self._data = data

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    @property
    def data(self):
        return self._data

    @property
    def length(self):
        return len(self._data)

    @staticmethod
    def new_object(clazz, data):
        return Object(clazz, data)

    @staticmethod
    def new_array(clazz, count):
        component_class_name = clazz.class_name[1:]
        default = None
        if is_primitive(component_class_name):
            default = get_default_value(component_class_name)
        return Object(clazz, [default] * count)

    def is_array(self) -> bool:
        return self.clazz.is_array()

    def is_instance_of(self, clazz) -> bool:
        return clazz.is_assignable_from(self.clazz)

    def set_field_value(self, name, descriptor, value):
        field = self.clazz.get_field(name, descriptor, False)
        self._data[field.index] = value

    def get_field_value(self, name, descriptor):
        field = self.clazz.get_field(name, descriptor, False)
        return self._data[field.index]
