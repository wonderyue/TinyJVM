import zipfile
import os
from class_loader import ClassLoader
from interpreter.interpreter import Interpreter


class TinyJVM:
    classloader = None

    def __init__(self, javahome, userpaths, mainClass):
        self.classloader = ClassLoader(javahome, userpaths, mainClass)

    def start(self):
        print("====start====")
        Interpreter(self.classloader.get_main_class(
        ).get_main_method())
