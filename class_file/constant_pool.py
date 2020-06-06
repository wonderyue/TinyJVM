class ConstantPool:
    _reader = None
    _constant_infos = []
    _tag2parser = {
        # CONSTANT_Utf8
        1: lambda reader: {"tag": 1, "val": reader.read_string(reader.read_int(2))},
        # CONSTANT_Integer
        3: lambda reader: {"tag": 3, "val": reader.read_int(4)},
        # CONSTANT_Float
        4: lambda reader: {"tag": 4, "val": reader.read_float()},
        # CONSTANT_Long
        5: lambda reader: {"tag": 5, "val": reader.read_int(8)},
        # CONSTANT_Double
        6: lambda reader: {"tag": 6, "val": reader.read_double()},
        # CONSTANT_Class
        7: lambda reader: {"tag": 7, "name_index": reader.read_int(2)},
        # CONSTANT_String
        8: lambda reader: {"tag": 8, "utf8_index": reader.read_int(2)},
        # CONSTANT_Fieldref
        9: lambda reader: {"tag": 9, "class_index": reader.read_int(2), "name_and_type_index": reader.read_int(2)},
        # CONSTANT_Methodref
        10: lambda reader: {"tag": 10, "class_index": reader.read_int(2), "name_and_type_index": reader.read_int(2)},
        # CONSTANT_InterfaceMethodref
        11: lambda reader: {"tag": 11, "class_index": reader.read_int(2), "name_and_type_index": reader.read_int(2)},
        # CONSTANT_NameAndType
        12: lambda reader: {"tag": 12, "name_index": reader.read_int(2), "descriptor_index": reader.read_int(2)},
        # CONSTANT_MethodHandle
        15: lambda reader: {"tag": 15, "reference_kind": reader.read_int(1), "reference_index": reader.read_int(2)},
        # CONSTANT_MethodType
        16: lambda reader: {"tag": 16, "descriptor_index": reader.read_int(2)},
        # CONSTANT_InvokeDynamic
        18: lambda reader: {"tag": 18, "bootstrap_method_attr_index": reader.read_int(2), "name_and_type_index": reader.read_int(2)},
        # CONSTANT_Package
        20: lambda reader: {"tag": 20, "name_index": reader.read_int(2)},
    }

    def __init__(self, reader):
        self._reader = reader
        self.parse()

    def parse(self):
        count = self._reader.read_int(2)
        self._constant_infos = [None] * count
        # index range: [1, count-1]
        index = 1
        while index < count:
            tag = self._reader.read_int(1)
            self.parse_constant_info(tag, index)
            # CONSTANT_Long and CONSTANT_Double consume 2 indexes
            if tag == 5 or tag == 6:
                index += 1
            index += 1

    def parse_constant_info(self, tag, index):
        self._constant_infos[index] = self._tag2parser[tag](self._reader)

    def get_constant(self, index):
        return self._constant_infos[index]

    def get_constant_value(self, index):
        return self.get_constant(index)["val"]

    def get_constants(self):
        return self._constant_infos

    def get_class_name(self, ref_index):
        if ref_index <= 0:
            return ""
        info = self.get_constant(ref_index)
        return self.get_constant_value(info["name_index"])

    def get_name_and_descriptor(self, ref_index):
        info = self.get_constant(ref_index)
        return self.get_constant_value(info["name_index"]), self.get_constant_value(info["descriptor_index"])

    def get_classname_name_and_descriptor(self, member_ref_index):
        ref_info = self.get_constant(member_ref_index)
        class_name = self.get_class_name(ref_info["class_index"])
        name, descriptor = self.get_name_and_descriptor(
            ref_info["name_and_type_index"])
        return {"class_name": class_name, "name": name, "descriptor": descriptor}
