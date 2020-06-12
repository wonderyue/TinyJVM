from runtime_data.heap.class_member import ClassMember
from runtime_data.heap.method_descriptor import MethodDescriptorParser
import struct


class ClassMethod(ClassMember):

    _return_type_2_instruction = {
        "I": 0xAC,
        "J": 0xAD,
        "F": 0xAE,
        "D": 0xAF,
        "L": 0xB0,
        "[": 0xB0,
        "V": 0xB1,
        "Z": 0xAC,
        "B": 0xAC,
        "C": 0xAC,
        "S": 0xAC,
    }

    def __init__(self, clazz, class_file_member):
        super().__init__(clazz, class_file_member)
        self.max_locals = 0
        self.max_stack = 0
        self.code = None
        code_attr = class_file_member.get_code()
        if code_attr is not None:
            self.max_locals = code_attr["max_locals"]
            self.max_stack = code_attr["max_stack"]
            self.code = code_attr["code"]
        parsed_descriptor = MethodDescriptorParser.parse(self.descriptor)
        self.arg_index = self.calc_arg_index(parsed_descriptor)
        if self.is_native():
            self.inject_code_attribute(parsed_descriptor.return_type)

    def calc_arg_index(self, parsed_descriptor):
        index = 0
        for param_type in parsed_descriptor.parameter_types:
            index += 1
            if param_type == "J" or param_type == "D":  # long or double
                index += 1
        if not self.is_static():  # this reference
            index += 1
        return index

    @staticmethod
    def new_methods(clazz, class_file_methods):
        methods = []
        for member in class_file_methods:
            methods.append(ClassMethod(clazz, member))
        return methods

    def inject_code_attribute(self, return_type):
        self.max_stack = 4
        self.max_locals = self.arg_index
        return_instruction = self._return_type_2_instruction[return_type[0]]
        self.code = struct.pack("BB", 0xFE, return_instruction)  # 0xFE: native method
