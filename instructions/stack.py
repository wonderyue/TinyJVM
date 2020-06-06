from instructions.base import Instruction, NoOperandInstruction
from utils.singleton import unsafe_singleton


@unsafe_singleton
class POP(NoOperandInstruction):

    def execute(self, frame):
        frame.pop_operand()


@unsafe_singleton
class POP2(NoOperandInstruction):

    def execute(self, frame):
        frame.pop_operand()
        frame.pop_operand()


@unsafe_singleton
class DUP(NoOperandInstruction):

    def execute(self, frame):
        val = frame.pop_operand()
        frame.push_operand(val)
        frame.push_operand(val)


@unsafe_singleton
class DUP_X1(NoOperandInstruction):

    def execute(self, frame):
        val1 = frame.pop_operand()
        val2 = frame.pop_operand()
        frame.push_operand(val1)
        frame.push_operand(val2)
        frame.push_operand(val1)


@unsafe_singleton
class DUP_X2(NoOperandInstruction):

    def execute(self, frame):
        val1 = frame.pop_operand()
        val2 = frame.pop_operand()
        val3 = frame.pop_operand()
        frame.push_operand(val1)
        frame.push_operand(val3)
        frame.push_operand(val2)
        frame.push_operand(val1)


@unsafe_singleton
class DUP2(NoOperandInstruction):

    def execute(self, frame):
        val1 = frame.pop_operand()
        val2 = frame.pop_operand()
        frame.push_operand(val1)
        frame.push_operand(val2)
        frame.push_operand(val1)
        frame.push_operand(val2)


@unsafe_singleton
class DUP2_X1(NoOperandInstruction):

    def execute(self, frame):
        val1 = frame.pop_operand()
        val2 = frame.pop_operand()
        val3 = frame.pop_operand()
        frame.push_operand(val2)
        frame.push_operand(val1)
        frame.push_operand(val3)
        frame.push_operand(val2)
        frame.push_operand(val1)


@unsafe_singleton
class DUP2_X2(NoOperandInstruction):

    def execute(self, frame):
        val1 = frame.pop_operand()
        val2 = frame.pop_operand()
        val3 = frame.pop_operand()
        val4 = frame.pop_operand()
        frame.push_operand(val2)
        frame.push_operand(val1)
        frame.push_operand(val4)
        frame.push_operand(val3)
        frame.push_operand(val2)
        frame.push_operand(val1)


@unsafe_singleton
class SWAP(NoOperandInstruction):

    def execute(self, frame):
        val1 = frame.pop_operand()
        val2 = frame.pop_operand()
        frame.push_operand(val1)
        frame.push_operand(val2)
