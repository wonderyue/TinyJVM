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


def _store_array_value(frame, value):
    index = frame.pop_operand()
    arr_obj = frame.pop_operand()
    if arr_obj is None:
        raise RuntimeError("java.lang.NullPointerException")
    if index < 0 or index >= arr_obj.length:
        raise RuntimeError("ArrayIndexOutOfBoundsException")
    arr_obj[index] = value


@unsafe_singleton
class IASTORE(NoOperandInstruction):
    def execute(self, frame):
        _store_array_value(frame, frame.pop_operand())


@unsafe_singleton
class DASTORE(NoOperandInstruction):
    def execute(self, frame):
        _store_array_value(frame, frame.pop_operand_double())


@unsafe_singleton
class LASTORE(NoOperandInstruction):
    def execute(self, frame):
        _store_array_value(frame, frame.pop_operand_long())
