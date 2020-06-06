from runtime_data.heap.class_member import ClassMember
from runtime_data.heap.method_descriptor import MethodDescriptorParser


class ClassMethod(ClassMember):

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
        self.arg_index = self.calc_arg_index()

    def calc_arg_index(self):
        index = 0
        parsed_descriptor = MethodDescriptorParser.parse(self.descriptor)
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
