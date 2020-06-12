from runtime_data.heap import access_flags as AF
from runtime_data.heap.runtime_constant_pool import RuntimeConstanPool
from runtime_data.heap.class_field import ClassField
from runtime_data.heap.class_method import ClassMethod
from runtime_data.heap.object import Object
from runtime_data.frame import Frame
from runtime_data.heap.utils import (
    get_array_class_name,
    get_component_class_name,
    is_primitive,
)
import os


class Class:
    def __init__(self, class_loader):
        self.loader = class_loader
        self.access_flags = None
        self.class_name = None
        self.super_class_name = None
        self.super_class = None
        self.interface_names = []
        self.interfaces = []
        self.constant_pool = None
        self.fields = []
        self.instance_field_count = 0
        self.methods = []
        self.static_fields = []
        self._is_clinit_started = False
        self.class_obj = None  # "object of java/lang/Class"

    @staticmethod
    def new_class(class_loader, class_reader):
        clazz = Class(class_loader)
        clazz.access_flags = class_reader.access_flags
        clazz.class_name = class_reader.get_class_name()
        clazz.super_class_name = class_reader.get_super_class_name()
        clazz.interface_names = class_reader.interfaces.get_interface_names()
        clazz.constant_pool = RuntimeConstanPool(clazz, class_reader.constant_pool)
        clazz.fields = ClassField.new_fields(clazz, class_reader.fields)
        clazz.methods = ClassMethod.new_methods(clazz, class_reader.methods)
        return clazz

    @staticmethod
    def new_array(class_loader, fully_qualified_name, super_class, interfaces):
        clazz = Class(class_loader)
        clazz.access_flags = AF.ACC_PUBLIC
        clazz.class_name = fully_qualified_name
        clazz.super_class = super_class
        clazz.interfaces = interfaces
        clazz.start_clinit()
        return clazz

    @property
    def is_clinit_started(self) -> bool:
        return self._is_clinit_started

    def start_clinit(self):
        self._is_clinit_started = True

    def is_primitive(self) -> bool:
        return is_primitive(self.class_name)

    def is_array(self) -> bool:
        return self.class_name[0] == "["

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
        return (
            self.is_public()
            or self.get_package_name() == other_cllass.get_package_name()
        )

    def get_package_name(self):
        return os.path.dirname(self.class_name)

    def is_sub_class_of(self, other_class) -> bool:
        clazz = self.super_class
        while clazz is not None:
            if clazz == other_class:
                return True
            clazz = clazz.super_class
        return False

    def is_super_class_of(self, other_interface) -> bool:
        return other_interface.is_sub_class_of(self)

    def is_implements(self, other_interface) -> bool:
        clazz = self
        while clazz is not None:
            for interface in clazz.interfaces:
                if interface == other_interface or interface.is_sub_interface_of(
                    other_interface
                ):
                    return True
            clazz = clazz.super_class
        return False

    def is_assignable_from(self, other_class) -> bool:
        if other_class == self:
            return True
        if not other_class.is_array():
            if not other_class.is_interface():
                if not self.is_interface():
                    return other_class.is_sub_class_of(self)
                else:
                    return other_class.is_implements(self)
            else:
                if not self.is_interface():
                    return self.is_jl_object()
                else:
                    return self.is_super_interface_of(other_class)
        else:
            if not self.is_array():
                if not self.is_interface():
                    return self.is_jl_object()
                else:
                    return self.is_jl_cloneable() or self.is_jio_serializable()
            else:
                sc = other_class.get_component_class()
                tc = self.get_component_class()
                return sc == tc or tc.is_assignable_from(sc)

    def is_sub_interface_of(self, other_interface) -> bool:
        for super_interface in self.interfaces:
            if (
                super_interface == other_interface
                or super_interface.is_sub_interface_of(other_interface)
            ):
                return True
        return False

    def is_super_interface_of(self, other_interface) -> bool:
        return other_interface.is_sub_interface_of(self)

    def is_jl_object(self):
        return self.class_name == "java/lang/Object"

    def is_jl_cloneable(self):
        return self.class_name == "java/lang/Cloneable"

    def is_jio_serializable(self):
        return self.class_name == "java/io/Serializable"

    @property
    def java_name(self):
        return self.class_name.replace("/", ".")

    def get_method(self, name, descriptor, is_static):
        c = self
        while c is not None:
            for method in c.methods:
                if (
                    method.is_static() == is_static
                    and method.name == name
                    and method.descriptor == descriptor
                ):
                    return method
            c = c.super_class
        return None

    def get_field(self, name, descriptor, is_static):
        c = self
        while c is not None:
            for field in c.fields:
                if (
                    field.is_static() == is_static
                    and field.name == name
                    and field.descriptor == descriptor
                ):
                    return field
            c = c.super_class
        return None

    def get_instance_method(self, name, descriptor):
        return self.get_method(name, descriptor, False)

    def get_main_method(self):
        return self.get_method("main", "([Ljava/lang/String;)V", True)

    def get_clinit_method(self):
        return self.get_method("<clinit>", "()V", True)

    def new_object(self):
        data = [None] * self.instance_field_count
        c = self
        while c is not None:
            for field in c.fields:
                if not field.is_static() and data[field.index] is None:
                    data[field.index] = field.val
            c = c.super_class
        return Object.new_object(self, data)

    def new_array_object(self, count):
        return Object.new_array(self, count)

    def get_array_class(self):
        "classname -> [class_name"
        return self.loader.load_class(get_array_class_name(self.class_name))

    def get_component_class(self):
        "[class_name -> class_name"
        return self.loader.load_class(get_component_class_name(self.class_name))

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

    def get_static_field(self, name, descriptor):
        return self.static_fields[self.get_field(name, descriptor, True).index]

    def set_static_field(self, name, descriptor, value):
        self.static_fields[self.get_field(name, descriptor, True).index] = value
