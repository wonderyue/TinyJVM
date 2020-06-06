from class_file.constant_pool import ConstantPool
from class_file.interfaces import Interfaces
from class_file.member import Member
from class_file.attributes import Attributes
from utils.reader_mixin import ReaderMixin
import struct


class ClassReader(ReaderMixin):
    """
    https:docs.oracle.comjavasespecsjvmsse14htmljvms-4.html
    ClassFile {
        u4 magic;
        u2 minor_version;
        u2 major_version;
        u2 constant_pool_count;
        cp_info constant_pool[constant_pool_count-1];
        u2 access_flags;
        u2 _this_class;
        u2 super_class;
        u2 interfaces_count;
        u2 interfaces[interfaces_count];
        u2 fields_count;
        field_info fields[fields_count];
        u2 methods_count;
        method_info methods[methods_count];
        u2 attributes_count;
        attribute_info attributes[attributes_count];
    }
    """

    def __init__(self, file):
        self._file = file

    def parse(self):
        self.magic = self._file.read(4)
        self.minor_version = self.read_int(2)
        self.major_version = self.read_int(2)
        self.constant_pool = ConstantPool(self)
        self.access_flags = self.read_int(2)
        self._this_class_index = self.read_int(2)
        self._super_class_index = self.read_int(2)
        self.interfaces = Interfaces(self, self.constant_pool)
        count = self.read_int(2)
        self.fields = [None] * count
        for i in range(count):
            self.fields[i] = Member(self, self.constant_pool)
        count = self.read_int(2)
        self.methods = [None] * count
        for i in range(count):
            self.methods[i] = Member(self, self.constant_pool)
        self.attributes = Attributes(self, self.constant_pool)

    def read_byte(self, n):
        return self._file.read(n)

    def get_class_name(self):
        return self.constant_pool.get_class_name(self._this_class_index)

    def get_super_class_name(self):
        return self.constant_pool.get_class_name(self._super_class_index)
