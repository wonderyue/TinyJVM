from runtime_data.heap.class_member import ClassMember


class ClassField(ClassMember):

    def __init__(self, clazz, class_file_member):
        super().__init__(clazz, class_file_member)
        self.val = class_file_member.get_value()

    @staticmethod
    def new_fields(clazz, class_file_members):
        fields = []
        for member in class_file_members:
            fields.append(ClassField(clazz, member))
        return fields
