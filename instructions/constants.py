from instructions.base import (
    Instruction,
    NoOperandInstruction,
    LocalIndexOperandMixin,
    ConstantPoolIndexOperandMixin,
)
from utils.singleton import unsafe_singleton
from runtime_data.heap import string
from runtime_data.heap.ref import ClassRef


@unsafe_singleton
class NOP(NoOperandInstruction):
    def execute(self, frame):
        pass


@unsafe_singleton
class ACONST_NULL(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand(None)


@unsafe_singleton
class DCONST_0(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand(0.0)


@unsafe_singleton
class DCONST_1(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand(1.0)


@unsafe_singleton
class FCONST_0(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand(0.0)


@unsafe_singleton
class FCONST_1(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand(1.0)


@unsafe_singleton
class FCONST_2(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand(2.0)


@unsafe_singleton
class ICONST_M1(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand(-1)


@unsafe_singleton
class ICONST_0(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand(0)


@unsafe_singleton
class ICONST_1(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand(1)


@unsafe_singleton
class ICONST_2(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand(2)


@unsafe_singleton
class ICONST_3(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand(3)


@unsafe_singleton
class ICONST_4(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand(4)


@unsafe_singleton
class ICONST_5(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand(5)


@unsafe_singleton
class LCONST_0(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand_long(0)


@unsafe_singleton
class LCONST_1(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand_long(1)


class BIPUSH(Instruction):
    def fetch_operand(self, reader):
        self.val = reader.read_int(1)

    def execute(self, frame):
        frame.push_operand(self.val)


class SIPUSH(Instruction):
    def fetch_operand(self, reader):
        self.val = reader.read_int(2)

    def execute(self, frame):
        frame.push_operand(self.val)


class _LDC:
    def execute(self, frame):
        cur_class = frame.method.clazz
        runtime_cp = cur_class.constant_pool
        val = runtime_cp.get_constant_value(self.index)
        if isinstance(val, str):
            frame.push_operand(string.new_string(cur_class.loader, val))
        elif isinstance(val, ClassRef):
            frame.push_operand(val.resolved_class().class_obj)
        else:
            frame.push_operand(val)


class LDC(_LDC, LocalIndexOperandMixin, Instruction):
    pass


class LDC_W(_LDC, ConstantPoolIndexOperandMixin, Instruction):
    pass


class LDC2_W(ConstantPoolIndexOperandMixin, Instruction):
    def execute(self, frame):
        runtime_cp = frame.method.clazz.constant_pool
        constant = runtime_cp.get_constant(self.index)
        if constant["tag"] == 5:  # long
            frame.push_operand_long(constant["val"])
        elif constant["tag"] == 6:  # double
            frame.push_operand_double(constant["val"])
