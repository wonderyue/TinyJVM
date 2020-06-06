from instructions.base import Instruction, NoOperandInstruction, LocalIndexOperandMixin, StoreLocalMixin, StoreLocalDoubleMixin, StoreLocalLongMixin
from utils.singleton import unsafe_singleton


class ISTORE(LocalIndexOperandMixin, StoreLocalMixin, Instruction):
    pass


@unsafe_singleton
class ISTORE_0(StoreLocalMixin, NoOperandInstruction):
    def __init__(self):
        self.index = 0


@unsafe_singleton
class ISTORE_1(StoreLocalMixin, NoOperandInstruction):
    def __init__(self):
        self.index = 1


@unsafe_singleton
class ISTORE_2(StoreLocalMixin, NoOperandInstruction):
    def __init__(self):
        self.index = 2


@unsafe_singleton
class ISTORE_3(StoreLocalMixin, NoOperandInstruction):
    def __init__(self):
        self.index = 3


class DSTORE(LocalIndexOperandMixin, StoreLocalDoubleMixin, Instruction):
    pass


@unsafe_singleton
class DSTORE_0(StoreLocalDoubleMixin, NoOperandInstruction):
    def __init__(self):
        self.index = 0


@unsafe_singleton
class DSTORE_1(StoreLocalDoubleMixin, NoOperandInstruction):
    def __init__(self):
        self.index = 1


@unsafe_singleton
class DSTORE_2(StoreLocalDoubleMixin, NoOperandInstruction):
    def __init__(self):
        self.index = 2


@unsafe_singleton
class DSTORE_3(StoreLocalDoubleMixin, NoOperandInstruction):
    def __init__(self):
        self.index = 3


class LSTORE(LocalIndexOperandMixin, StoreLocalLongMixin, Instruction):
    pass


@unsafe_singleton
class LSTORE_0(StoreLocalLongMixin, NoOperandInstruction):
    def __init__(self):
        self.index = 0


@unsafe_singleton
class LSTORE_1(StoreLocalLongMixin, NoOperandInstruction):
    def __init__(self):
        self.index = 1


@unsafe_singleton
class LSTORE_2(StoreLocalLongMixin, NoOperandInstruction):
    def __init__(self):
        self.index = 2


@unsafe_singleton
class LSTORE_3(StoreLocalLongMixin, NoOperandInstruction):
    def __init__(self):
        self.index = 3
