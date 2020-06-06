from runtime_data.heap import access_flags as AF
from runtime_data.heap.runtime_constant_pool import RuntimeConstanPool
from runtime_data.heap.class_field import ClassField
from runtime_data.heap.class_method import ClassMethod
from runtime_data.heap.object import Object
from runtime_data.frame import Frame
import os


class Class:

    def __init__(self, class_reader, class_loader):
        self.access_flags = class_reader.access_flags
        self.class_name = class_reader.get_class_name()
        self.super_class_name = class_reader.get_super_class_name()
        self.super_class = None
        self.loader = class_loader
        self.interface_names = class_reader.interfaces.get_interface_names()
        self.interfaces = []
        self.constant_pool = RuntimeConstanPool(
            self, class_reader.constant_pool)
        self.fields = ClassField.new_fields(self, class_reader.fields)
        self.instance_field_count = 0
        self.methods = ClassMethod.new_methods(self, class_reader.methods)
        self.static_fields = []
        self._is_clinit_started = False

    @property
    def is_clinit_started(self) -> bool:
        return self._is_clinit_started

    def start_clinit(self):
        self._is_clinit_started = True

    def is_public(self) -> bool:
        return 0 != self.access_flags & AF.ACC_PUBLIC

    def is_final(self) -> bool:
        return 0 != self.access_flags & AF.ACC_FINAL

    def is_super(self) -> bool:
        return 0 != self.access_flags & AF.ACC_SUPER

    def is_interface(self) -> bool:
        return 0 != self.access_flags & AF.ACC_INTERFACE

    def is_abstract(self) -> bool:
        return 0 != self.access_flags & AF.ACC_ABSTRACT

    def is_synthetic(self) -> bool:
        return 0 != self.access_flags & AF.ACC_SYNTHETIC

    def is_annotation(self) -> bool:
        return 0 != self.access_flags & AF.ACC_ANNOTATION

    def is_enum(self) -> bool:
        return 0 != self.access_flags & AF.ACC_ENUM

    def is_accessible_from(self, other_cllass) -> bool:
        return self.is_public() or self.get_package_name() == other_cllass.get_package_name()

    def get_package_name(self):
        return os.path.dirname(self.class_name)

    def is_sub_class_of(self, other_class) -> bool:
        clazz = self.super_class
        while clazz:
            if clazz == other_class:
                return True
            clazz = clazz.super_class
        return False

    def is_super_class_of(self, other_interface) -> bool:
        return other_interface.is_sub_class_of(self)

    def is_implements(self, other_interface) -> bool:
        clazz = self
        while clazz:
            for interface in clazz.interfaces:
                if interface == other_interface or interface.is_sub_interface_of(other_interface):
                    return True
            clazz = clazz.super_class
        return False

    def is_assignable_from(self, other_class) -> bool:
        if other_class == self:
            return True
        if not self.is_interface():
            return other_class.is_sub_class_of(self)
        else:
            return other_class.is_implements(self)

    def is_sub_interface_of(self, other_interface) -> bool:
        for super_interface in self.interfaces:
            if super_interface == other_interface or super_interface.is_sub_interface_of(other_interface):
                return True
        return False

    def get_main_method(self):
        return self.get_static_method("main", "([Ljava/lang/String;)V")

    def get_clinit_method(self):
        return self.get_static_method("<clinit>", "()V")

    def get_static_method(self, name, descriptor):
        for method in self.methods:
            if method.is_static() and method.name == name and method.descriptor == descriptor:
                return method
        return None

    def new_object(self):
        return Object(self)

    def clinit(self, thread):
        self.start_clinit()
        self.schedule_clinit(thread)
        self.init_super_class(thread)

    def schedule_clinit(self, thread):
        clinit = self.get_clinit_method()
        if clinit is not None:
            thread.push_frame(Frame(thread, clinit))

    def init_super_class(self, thread):
        if not self.is_interface():
            if self.super_class is not None and not self.super_class.is_clinit_started:
                self.super_class.clinit(thread)
