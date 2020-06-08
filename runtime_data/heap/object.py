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
    def length(self):
        return len(self._data)

    @staticmethod
    def new_object(clazz):
        return Object(clazz, [None] * clazz.instance_field_count)

    @staticmethod
    def new_array(clazz, count):
        # TODO: default value
        return Object(clazz, [None] * count)

    def is_array(self) -> bool:
        return self.clazz.is_array()

    def is_instance_of(self, clazz) -> bool:
        return clazz.is_assignable_from(self.clazz)
