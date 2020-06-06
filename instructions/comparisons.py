from instructions.base import Instruction, NoOperandInstruction, BranchOperandMixin
import numpy as np
from utils.singleton import unsafe_singleton


@unsafe_singleton
class LCMP(NoOperandInstruction):
    def execute(self, frame):
        val2 = frame.pop_operand_long()
        val1 = frame.pop_operand_long()
        res = 0
        if val1 > val2:
            res = 1
        elif val1 < val2:
            res = -1
        frame.push_operand(res)


def fcmp(frame, flag):
    val2 = frame.pop_operand()
    val1 = frame.pop_operand()
    res = 0
    if np.isnan(val1) or np.isnan(val2):
        res = 1 if flag else -1
    elif val1 > val2:
        res = 1
    elif val1 < val2:
        res = -1
    frame.push_operand(res)


def dcmp(frame, flag):
    val2 = frame.pop_operand_double()
    val1 = frame.pop_operand_double()
    res = 0
    if np.isnan(val1) or np.isnan(val2):
        res = 1 if flag else -1
    elif val1 > val2:
        res = 1
    elif val1 < val2:
        res = -1
    frame.push_operand(res)


@unsafe_singleton
class FCMPG(NoOperandInstruction):
    def execute(self, frame):
        fcmp(frame, True)


@unsafe_singleton
class FCMPL(NoOperandInstruction):
    def execute(self, frame):
        fcmp(frame, False)


@unsafe_singleton
class DCMPG(NoOperandInstruction):
    def execute(self, frame):
        dcmp(frame, True)


@unsafe_singleton
class DCMPL(NoOperandInstruction):
    def execute(self, frame):
        dcmp(frame, False)


class IFEQ(BranchOperandMixin, Instruction):
    def execute(self, frame):
        val = frame.pop_operand()
        if val == 0:
            frame.jump(self.offset)


class IFNE(BranchOperandMixin, Instruction):
    def execute(self, frame):
        val = frame.pop_operand()
        if val != 0:
            frame.jump(self.offset)


class IFLT(BranchOperandMixin, Instruction):
    def execute(self, frame):
        val = frame.pop_operand()
        if val < 0:
            frame.jump(self.offset)


class IFLE(BranchOperandMixin, Instruction):
    def execute(self, frame):
        val = frame.pop_operand()
        if val <= 0:
            frame.jump(self.offset)


class IFGT(BranchOperandMixin, Instruction):
    def execute(self, frame):
        val = frame.pop_operand()
        if val > 0:
            frame.jump(self.offset)


class IFGE(BranchOperandMixin, Instruction):
    def execute(self, frame):
        val = frame.pop_operand()
        if val >= 0:
            frame.jump(self.offset)


class IF_ICMPEQ(BranchOperandMixin, Instruction):
    def execute(self, frame):
        val2 = frame.pop_operand()
        val1 = frame.pop_operand()
        if val1 == val2:
            frame.jump(self.offset)


class IF_ICMPNE(BranchOperandMixin, Instruction):
    def execute(self, frame):
        val2 = frame.pop_operand()
        val1 = frame.pop_operand()
        if val1 != val2:
            frame.jump(self.offset)


class IF_ICMPLT(BranchOperandMixin, Instruction):
    def execute(self, frame):
        val2 = frame.pop_operand()
        val1 = frame.pop_operand()
        if val1 < val2:
            frame.jump(self.offset)


class IF_ICMPLE(BranchOperandMixin, Instruction):
    def execute(self, frame):
        val2 = frame.pop_operand()
        val1 = frame.pop_operand()
        if val1 <= val2:
            frame.jump(self.offset)


class IF_ICMPGT(BranchOperandMixin, Instruction):
    def execute(self, frame):
        val2 = frame.pop_operand()
        val1 = frame.pop_operand()
        if val1 > val2:
            frame.jump(self.offset)


class IF_ICMPGE(BranchOperandMixin, Instruction):
    def execute(self, frame):
        val2 = frame.pop_operand()
        val1 = frame.pop_operand()
        if val1 >= val2:
            frame.jump(self.offset)


class IF_ACMPEQ(BranchOperandMixin, Instruction):
    def execute(self, frame):
        val2 = frame.pop_operand()
        val1 = frame.pop_operand()
        if val1 is val2:
            frame.jump(self.offset)


class IF_ACMPNE(BranchOperandMixin, Instruction):
    def execute(self, frame):
        val2 = frame.pop_operand()
        val1 = frame.pop_operand()
        if val1 is not val2:
            frame.jump(self.offset)
