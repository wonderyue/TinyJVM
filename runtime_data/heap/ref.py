from runtime_data.heap.utils import lookup_method_in_class, lookup_method_in_interfaces


class Ref:

    def __init__(self, runtime_constant_pool, class_name):
        self.class_name = class_name
        self.constant_pool = runtime_constant_pool
        self.clazz = None

    def resolved_class(self):
        if self.clazz is None:
            self.resolve_class_ref()
        return self.clazz

    def resolve_class_ref(self):
        cur = self.constant_pool.clazz
        class_ref = cur.loader.load_class(self.class_name)
        if not class_ref.is_accessible_from(cur):
            raise RuntimeError("java.lang.IllegalAccessError: access {0} from {1}".format(
                self.class_name, cur.class_name))
        self.clazz = class_ref


class ClassRef(Ref):
    pass


class MemberRef(Ref):

    def __init__(self, runtime_constant_pool, kw):
        super().__init__(runtime_constant_pool, kw["class_name"])
        self.name = kw["name"]
        self.descriptor = kw["descriptor"]
        self.member = None

    def resolved_member(self):
        if self.member is None:
            self.resolve_member_ref()
        return self.member

    def resolve_member_ref(self):
        raise NotImplementedError


class FieldRef(MemberRef):

    def resolve_member_ref(self):
        cur = self.constant_pool.clazz
        ref_class = self.resolved_class()
        field = self.look_up_field(ref_class, self.name, self.descriptor)
        if field is None:
            raise RuntimeError("java.lang.NoSuchFieldError: {0}.{1}".format(
                self.class_name, self.name))
        if not field.is_accessible_from(cur):
            raise RuntimeError("java.lang.IllegalAccessError: access {0}.{1} from {2}".format(
                self.class_name, self.name, cur.class_name))
        self.member = field

    def look_up_field(self, clazz, name, descriptor):
        for field in clazz.fields:
            if field.name == name and field.descriptor == descriptor:
                return field
        for interface in clazz.interfaces:
            if (field:= self.look_up_field(interface, name, descriptor)) is not None:
                return field
        if clazz.super_class is not None:
            return self.look_up_field(clazz.super_class, name, descriptor)
        return None


class MethodRef(MemberRef):

    def resolve_member_ref(self):
        cur = self.constant_pool.clazz
        ref_class = self.resolved_class()
        if ref_class.is_interface():
            raise RuntimeError("java.lang.IncompatibleClassChangeError")
        method = self.look_up_method(ref_class, self.name, self.descriptor)
        if method is None:
            raise RuntimeError("java.lang.NoSuchMethodError: {0}.{1}".format(
                self.class_name, self.name))
        if not method.is_accessible_from(cur):
            raise RuntimeError("java.lang.IllegalAccessError: access {0}.{1} from {2}".format(
                self.class_name, self.name, cur.class_name))
        self.member = method

    def look_up_method(self, clazz, name, descriptor):
        if (method:= lookup_method_in_class(clazz, name, descriptor)) is not None:
            return method
        return lookup_method_in_interfaces(clazz.interfaces, name, descriptor)


class InterfaceMethodRef(MemberRef):

    def resolve_member_ref(self):
        cur = self.constant_pool.clazz
        ref_class = self.resolved_class()
        if not ref_class.is_interface():
            raise RuntimeError("java.lang.IncompatibleClassChangeError")
        method = self.look_up_method(ref_class, self.name, self.descriptor)
        if method is None:
            raise RuntimeError("java.lang.NoSuchMethodError: {0}.{1}".format(
                self.class_name, self.name))
        if not method.is_accessible_from(cur):
            raise RuntimeError("java.lang.IllegalAccessError: access {0}.{1} from {2}".format(
                self.class_name, self.name, cur.class_name))
        self.member = method

    def look_up_method(self, clazz, name, descriptor):
        for method in clazz.methods:
            if method.name == name and method.descriptor == descriptor:
                return method
        return lookup_method_in_interfaces(clazz.interfaces, name, descriptor)
