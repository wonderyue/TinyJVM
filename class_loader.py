import zipfile
import os
from class_file.class_reader import ClassReader
from runtime_data.heap.clazz import Class
from runtime_data.heap.utils import ATYPR_2_CLASS_NAME
from runtime_data.heap import string


class ClassLoader:
    def __init__(self, javahome, user_paths, main_class):
        self._boot_classpath = os.path.join(javahome, "jre", "lib")
        self._ext_classpath = os.path.join(javahome, "jre", "lib", "ext")
        self._user_classpaths = user_paths
        self._main_class = (
            os.path.basename(os.path.splitext(main_class)[0])
            if main_class.endswith(".class")
            else self._main_class_from_jar(main_class)
        )
        self._classes = {}
        print("BootClasspath:", self._boot_classpath)
        print("ExtClasspath", self._ext_classpath)
        print("UserClasspaths", self._user_classpaths)
        print("MainClass", self._main_class)

    def _main_class_from_jar(self, jar):
        jar = zipfile.ZipFile(jar)
        with jar.open("META-INF/MANIFEST.MF", mode="r") as manifest:
            for line in manifest.readlines():
                s = line.decode("utf-8")
                if s.startswith("Main-Class"):
                    return s.split(":")[1].strip().replace("\n\r", "")
        return None

    def _walk_dir(self, dir, filename, callback=None):
        for root, dirs, files in os.walk(dir):
            for name in files:
                if name == filename:
                    if callback is not None:
                        with open(os.path.join(root, name), "rb") as fd:
                            return callback(fd)
                elif name.endswith(".jar"):
                    res = self._walk_jar(os.path.join(root, name), filename, callback)
                    if res is not None:
                        return res
        return None

    def _walk_jar(self, jarname, filename, callback=None):
        jar = zipfile.ZipFile(jarname)
        for name in jar.namelist():
            if name == filename:
                if callback is not None:
                    with jar.open(name, mode="r") as fd:
                        return callback(fd)
        return None

    def _parse_by_fd(self, fd):
        reader = ClassReader(fd)
        reader.parse()
        return reader

    def _parse_by_name(self, filename):
        res = self._walk_dir(self._boot_classpath, filename, self._parse_by_fd)
        if res is not None:
            return res
        res = self._walk_dir(self._ext_classpath, filename, self._parse_by_fd)
        if res is not None:
            return res
        for dir in self._user_classpaths:
            res = self._walk_dir(dir, filename, self._parse_by_fd)
            if res is not None:
                return res
        return None

    def get_main_class(self):
        return self.load_class(self._main_class)

    def load_array(self, atype):
        if atype not in ATYPR_2_CLASS_NAME:
            raise RuntimeError("Invalid atype")
        return self.load_class(ATYPR_2_CLASS_NAME[atype])

    def load_class(self, fully_qualified_name):
        if fully_qualified_name in self._classes:
            return self._classes[fully_qualified_name]
        if fully_qualified_name[0] == "[":
            return self._load_array_class(fully_qualified_name)
        return self._load_non_array_class(fully_qualified_name)

    def _load_array_class(self, fully_qualified_name):
        clazz = Class.new_array(
            self,
            fully_qualified_name,
            self.load_class("java/lang/Object"),
            self._get_interfaces(),
        )
        self._classes[fully_qualified_name] = clazz
        return clazz

    def _get_interfaces(self):
        return [
            self.load_class("java/lang/Cloneable"),
            self.load_class("java/io/Serializable"),
        ]

    def _load_non_array_class(self, fully_qualified_name):
        class_reader = self._parse_by_name(fully_qualified_name + ".class")
        if class_reader is None:
            raise RuntimeError("Unknown Class: " + fully_qualified_name)
        clazz = self._define_class(class_reader)
        self._link(clazz)
        self._classes[fully_qualified_name] = clazz
        return clazz

    def _define_class(self, class_reader):
        clazz = Class.new_class(self, class_reader)
        self._resolve_super_class(clazz)
        self._resolve_interfaces(clazz)
        return clazz

    def _resolve_super_class(self, clazz):
        if clazz.class_name != "java/lang/Object":
            clazz.super_class = clazz.loader.load_class(clazz.super_class_name)

    def _resolve_interfaces(self, clazz):
        for interface_name in clazz.interface_names:
            clazz.interfaces.append(clazz.loader.load_class(interface_name))

    def _link(self, clazz):
        self._verify(clazz)
        self._prepare(clazz)

    def _verify(self, clazz):
        pass

    def _prepare(self, clazz):
        self._init_instance_field(clazz)
        self._init_static_field(clazz)

    def _init_instance_field(self, clazz):
        index = 0
        if clazz.super_class is not None:
            index = clazz.super_class.instance_field_count
        for field in clazz.fields:
            if not field.is_static():
                field.index = index
                index += 1
        clazz.instance_field_count = index

    def _init_static_field(self, clazz):
        clazz.static_fields = []
        index = 0
        for field in clazz.fields:
            if field.is_static():
                field.index = index
                index += 1
                if field.is_final():
                    if isinstance(field.val, str):
                        clazz.static_fields.append(string.new_string(self, field.val))
                    else:
                        clazz.static_fields.append(field.val)
                else:
                    clazz.static_fields.append(None)
