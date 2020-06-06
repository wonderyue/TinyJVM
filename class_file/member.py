from class_file.attributes import Attributes


class Member:
    """
    field_info {
        u2 access_flags;
        u2 name_index;
        u2 descriptor_index;
        u2 attributes_count; 
        attribute_info attributes[attributes_count];
    }
    """

    def __init__(self, reader, constant_pool):
        self._reader = reader
        self._constant_pool = constant_pool
        self._parse()

    def _parse(self):
        self.access_flags = self._reader.read_int(2)
        self._name_index = self._reader.read_int(2)
        self._descriptor_index = self._reader.read_int(2)
        self._attributes = Attributes(self._reader, self._constant_pool)

    def get_code(self):
        for attribute in self._attributes.attribute_infos:
            if attribute["name"] == "Code":
                return attribute
        return None

    def get_value(self):
        """
        for field only
        """
        for attribute in self._attributes.attribute_infos:
            if attribute["name"] == "ConstantValue":
                return attribute["val"]
        return None

    def get_name(self):
        return self._constant_pool.get_constant_value(self._name_index)

    def get_descriptor(self):
        return self._constant_pool.get_constant_value(self._descriptor_index)
