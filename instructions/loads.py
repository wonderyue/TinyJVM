from instructions.base import Instruction, NoOperandInstruction, LocalIndexOperandMixin, LoadLocalMixin, LoadLocalDoubleMixin, LoadLocalLongMixin
from utils.singleton import unsafe_singleton


class ILOAD(LocalIndexOperandMixin, LoadLocalMixin, Instruction):
    pass


@unsafe_singleton
class ILOAD_0(LoadLocalMixin, NoOperandInstruction):
    def __init__(self):
        self.index = 0


@unsafe_singleton
class ILOAD_1(LoadLocalMixin, NoOperandInstruction):
    def __init__(self):
        self.index = 1


@unsafe_singleton
class ILOAD_2(LoadLocalMixin, NoOperandInstruction):
    def __init__(self):
        self.index = 2


@unsafe_singleton
class ILOAD_3(LoadLocalMixin, NoOperandInstruction):
    def __init__(self):
        self.index = 3


class DLOAD(LocalIndexOperandMixin, LoadLocalDoubleMixin, Instruction):
    pass


@unsafe_singleton
class DLOAD_0(LoadLocalDoubleMixin, NoOperandInstruction):
    def __init__(self):
        self.index = 0


@unsafe_singleton
class DLOAD_1(LoadLocalDoubleMixin, NoOperandInstruction):
    def __init__(self):
        self.index = 1


@unsafe_singleton
class DLOAD_2(LoadLocalDoubleMixin, NoOperandInstruction):
    def __init__(self):
        self.index = 2


@unsafe_singleton
class DLOAD_3(LoadLocalDoubleMixin, NoOperandInstruction):
    def __init__(self):
        self.index = 3


class LLOAD(LocalIndexOperandMixin, LoadLocalLongMixin, Instruction):
    pass


@unsafe_singleton
class LLOAD_0(LoadLocalLongMixin, NoOperandInstruction):
    def __init__(self):
        self.index = 0


@unsafe_singleton
class LLOAD_1(LoadLocalLongMixin, NoOperandInstruction):
    def __init__(self):
        self.index = 1


@unsafe_singleton
class LLOAD_2(LoadLocalLongMixin, NoOperandInstruction):
    def __init__(self):
        self.index = 2


@unsafe_singleton
class LLOAD_3(LoadLocalLongMixin, NoOperandInstruction):
    def __init__(self):
        self.index = 3
