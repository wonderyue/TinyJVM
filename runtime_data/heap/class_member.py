from runtime_data.heap import access_flags as AF


class ClassMember:

    def __init__(self, clazz, class_file_member):
        self.clazz = clazz
        self.access_flags = class_file_member.access_flags
        self.name = class_file_member.get_name()
        self.descriptor = class_file_member.get_descriptor()
        self.index = None

    def is_public(self) -> bool:
        return 0 != self.access_flags & AF.ACC_PUBLIC

    def is_private(self) -> bool:
        return 0 != self.access_flags & AF.ACC_PRIVATE

    def is_protected(self) -> bool:
        return 0 != self.access_flags & AF.ACC_PROTECTED

    def is_static(self) -> bool:
        return 0 != self.access_flags & AF.ACC_STATIC

    def is_final(self) -> bool:
        return 0 != self.access_flags & AF.ACC_FINAL

    def is_synthetic(self) -> bool:
        return 0 != self.access_flags & AF.ACC_SYNTHETIC

    def is_abstract(self) -> bool:
        return 0 != self.access_flags & AF.ACC_ABSTRACT

    def is_native(self) -> bool:
        return 0 != self.access_flags & AF.ACC_NATIVE

    def is_bridge(self) -> bool:
        return 0 != self.access_flags & AF.ACC_BRIDGE

    def is_varargs(self) -> bool:
        return 0 != self.access_flags & AF.ACC_VARARGS

    def is_strict(self) -> bool:
        return 0 != self.access_flags & AF.ACC_STRICT

    def is_accessible_from(self, other_class) -> bool:
        if self.is_public() or other_class == self.clazz:
            return True
        if self.is_protected():
            return other_class.is_sub_class_of(self.clazz) or self.clazz.get_package_name() == other_class.get_package_name()
        if not self.is_private():  # default
            return self.clazz.get_package_name() == other_class.get_package_name()
        return False
