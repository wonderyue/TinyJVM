from runtime_data.heap.ref import ClassRef, FieldRef, MethodRef, InterfaceMethodRef


class RuntimeConstanPool:

    _tag2parser = {
        # CONSTANT_Utf8
        1: lambda class_cp, runtime_cp, index: {
            "tag": 1,
            "val": class_cp.get_constant_value(index),
        },
        # CONSTANT_Integer
        3: lambda class_cp, runtime_cp, index: {
            "tag": 3,
            "val": class_cp.get_constant_value(index),
        },
        # CONSTANT_Float
        4: lambda class_cp, runtime_cp, index: {
            "tag": 4,
            "val": class_cp.get_constant_value(index),
        },
        # CONSTANT_Long
        5: lambda class_cp, runtime_cp, index: {
            "tag": 5,
            "val": class_cp.get_constant_value(index),
        },
        # CONSTANT_Double
        6: lambda class_cp, runtime_cp, index: {
            "tag": 6,
            "val": class_cp.get_constant_value(index),
        },
        # CONSTANT_Class
        7: lambda class_cp, runtime_cp, index: {
            "tag": 7,
            "val": ClassRef(runtime_cp, class_cp.get_class_name(index)),
        },
        # CONSTANT_String
        8: lambda class_cp, runtime_cp, index: {
            "tag": 8,
            "val": class_cp.get_string_value(index),
        },
        # CONSTANT_Fieldref
        9: lambda class_cp, runtime_cp, index: {
            "tag": 9,
            "val": FieldRef(
                runtime_cp, class_cp.get_classname_name_and_descriptor(index)
            ),
        },
        # CONSTANT_Methodref
        10: lambda class_cp, runtime_cp, index: {
            "tag": 10,
            "val": MethodRef(
                runtime_cp, class_cp.get_classname_name_and_descriptor(index)
            ),
        },
        # CONSTANT_InterfaceMethodref
        11: lambda class_cp, runtime_cp, index: {
            "tag": 11,
            "val": InterfaceMethodRef(
                runtime_cp, class_cp.get_classname_name_and_descriptor(index)
            ),
        },
    }

    def __init__(self, clazz, constant_pool):
        self.clazz = clazz
        self._constant_pool = constant_pool
        infos = constant_pool.get_constants()
        self._constants = [None] * len(infos)
        # index range: [1, count-1]
        index = 1
        while index < len(infos):
            info = infos[index]
            tag = info["tag"]
            if tag in self._tag2parser:
                self._constants[index] = self._tag2parser[tag](
                    constant_pool, self, index
                )
                # CONSTANT_Long and CONSTANT_Double consume 2 indexes
                if tag == 5 or tag == 6:
                    index += 1
            index += 1

    def get_constant(self, index):
        return self._constants[index]

    def get_constant_value(self, index):
        return self._constants[index]["val"]
