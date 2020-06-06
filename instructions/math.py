from instructions.base import Instruction, NoOperandInstruction
import numpy as np
from utils.singleton import unsafe_singleton


@unsafe_singleton
class IADD(NoOperandInstruction):
    def execute(self, frame):
        val2 = frame.pop_operand()
        val1 = frame.pop_operand()
        frame.push_operand(val1 + val2)


@unsafe_singleton
class LADD(NoOperandInstruction):
    def execute(self, frame):
        val2 = frame.pop_operand_long()
        val1 = frame.pop_operand_long()
        frame.push_operand_long(val1 + val2)


@unsafe_singleton
class DADD(NoOperandInstruction):
    def execute(self, frame):
        val2 = frame.pop_operand_double()
        val1 = frame.pop_operand_double()
        frame.push_operand_double(val1 + val2)


@unsafe_singleton
class ISUB(NoOperandInstruction):
    def execute(self, frame):
        val2 = frame.pop_operand()
        val1 = frame.pop_operand()
        frame.push_operand(val1 - val2)


@unsafe_singleton
class LSUB(NoOperandInstruction):
    def execute(self, frame):
        val2 = frame.pop_operand_long()
        val1 = frame.pop_operand_long()
        frame.push_operand_long(val1 - val2)


@unsafe_singleton
class DSUB(NoOperandInstruction):
    def execute(self, frame):
        val2 = frame.pop_operand_double()
        val1 = frame.pop_operand_double()
        frame.push_operand_double(val1 - val2)


@unsafe_singleton
class IMUL(NoOperandInstruction):
    def execute(self, frame):
        val2 = frame.pop_operand()
        val1 = frame.pop_operand()
        frame.push_operand(val1 * val2)


@unsafe_singleton
class LMUL(NoOperandInstruction):
    def execute(self, frame):
        val2 = frame.pop_operand_long()
        val1 = frame.pop_operand_long()
        frame.push_operand_long(val1 * val2)


@unsafe_singleton
class DMUL(NoOperandInstruction):
    def execute(self, frame):
        val2 = frame.pop_operand_double()
        val1 = frame.pop_operand_double()
        frame.push_operand_double(val1 * val2)


@unsafe_singleton
class IDIV(NoOperandInstruction):
    def execute(self, frame):
        val2 = frame.pop_operand()
        val1 = frame.pop_operand()
        frame.push_operand(val1 / val2)


@unsafe_singleton
class LDIV(NoOperandInstruction):
    def execute(self, frame):
        val2 = frame.pop_operand_long()
        val1 = frame.pop_operand_long()
        frame.push_operand_long(val1 / val2)


@unsafe_singleton
class DDIV(NoOperandInstruction):
    def execute(self, frame):
        val2 = frame.pop_operand_double()
        val1 = frame.pop_operand_double()
        frame.push_operand_double(val1 / val2)


@unsafe_singleton
class IREM(NoOperandInstruction):
    def execute(self, frame):
        val2 = frame.pop_operand()
        val1 = frame.pop_operand()
        frame.push_operand(val1 % val2)


@unsafe_singleton
class LREM(NoOperandInstruction):
    def execute(self, frame):
        val2 = frame.pop_operand_long()
        val1 = frame.pop_operand_long()
        frame.push_operand_long(val1 % val2)


@unsafe_singleton
class DREM(NoOperandInstruction):
    def execute(self, frame):
        val2 = frame.pop_operand_double()
        val1 = frame.pop_operand_double()
        frame.push_operand_double(val1 % val2)


@unsafe_singleton
class INEG(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand(-frame.pop_operand())


@unsafe_singleton
class LNEG(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand_long(-frame.pop_operand_long())


@unsafe_singleton
class DNEG(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand_double(-frame.pop_operand_double())


@unsafe_singleton
class ISHL(NoOperandInstruction):
    def execute(self, frame):
        val2 = frame.pop_operand() & 0x1f  # max shifts: 31
        val1 = frame.pop_operand()
        frame.push_operand(np.int32(val1 << val2))


@unsafe_singleton
class ISHR(NoOperandInstruction):
    def execute(self, frame):
        val2 = frame.pop_operand() & 0x1f  # max shifts: 31
        val1 = frame.pop_operand()
        frame.push_operand(np.int32(val1 >> val2))


@unsafe_singleton
class IUSHR(NoOperandInstruction):
    def execute(self, frame):
        val2 = frame.pop_operand() & 0x1f  # max shifts: 31
        val1 = np.uint32(frame.pop_operand())
        frame.push_operand(np.int32(val1 >> val2))


@unsafe_singleton
class LSHL(NoOperandInstruction):
    def execute(self, frame):
        val2 = frame.pop_operand() & 0x3f  # max shifts: 63
        val1 = frame.pop_operand_long()
        frame.push_operand_long(np.int32(val1 << val2))


@unsafe_singleton
class LSHR(NoOperandInstruction):
    def execute(self, frame):
        val2 = frame.pop_operand() & 0x3f  # max shifts: 63
        val1 = frame.pop_operand_long()
        frame.push_operand_long(val1 >> val2)


@unsafe_singleton
class LUSHR(NoOperandInstruction):
    def execute(self, frame):
        val2 = frame.pop_operand() & 0x3f  # max shifts: 63
        val1 = frame.pop_operand_long() % 0x10000000000000000
        frame.push_operand_long(val1 >> val2)


@unsafe_singleton
class IAND(NoOperandInstruction):
    def execute(self, frame):
        val2 = frame.pop_operand()
        val1 = frame.pop_operand()
        frame.push_operand(val1 & val2)


@unsafe_singleton
class IOR(NoOperandInstruction):
    def execute(self, frame):
        val2 = frame.pop_operand()
        val1 = frame.pop_operand()
        frame.push_operand(val1 | val2)


@unsafe_singleton
class IXOR(NoOperandInstruction):
    def execute(self, frame):
        val2 = frame.pop_operand()
        val1 = frame.pop_operand()
        frame.push_operand(val1 ^ val2)


@unsafe_singleton
class LAND(NoOperandInstruction):
    def execute(self, frame):
        val2 = frame.pop_operand_long()
        val1 = frame.pop_operand_long()
        frame.push_operand_long(val1 & val2)


@unsafe_singleton
class LOR(NoOperandInstruction):
    def execute(self, frame):
        val2 = frame.pop_operand_long()
        val1 = frame.pop_operand_long()
        frame.push_operand_long(val1 | val2)


@unsafe_singleton
class LXOR(NoOperandInstruction):
    def execute(self, frame):
        val2 = frame.pop_operand_long()
        val1 = frame.pop_operand_long()
        frame.push_operand_long(val1 ^ val2)


class IINC(Instruction):

    def fetch_operand(self, reader):
        self.index = reader.read_uint(1)
        self.const = reader.read_int(1)

    def execute(self, frame):
        frame.set_local(self.index, frame.get_local(self.index) + self.const)
