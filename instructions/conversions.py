from instructions.base import Instruction, NoOperandInstruction
import numpy as np
from utils.singleton import unsafe_singleton


@unsafe_singleton
class I2L(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand_long(frame.pop_operand())


@unsafe_singleton
class I2F(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand(np.float32(frame.pop_operand()))


@unsafe_singleton
class I2D(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand_double(np.float64(frame.pop_operand_long()))


@unsafe_singleton
class I2B(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand(np.uint8(frame.pop_operand()))


@unsafe_singleton
class I2C(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand(np.uint16(frame.pop_operand()))


@unsafe_singleton
class I2S(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand(np.int16(frame.pop_operand()))


@unsafe_singleton
class L2I(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand(np.int32(frame.pop_operand_long()))


@unsafe_singleton
class L2F(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand(np.float32(frame.pop_operand_long()))


@unsafe_singleton
class L2D(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand_double(np.float64(frame.pop_operand_long()))


@unsafe_singleton
class F2I(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand(np.int32(frame.pop_operand()))


@unsafe_singleton
class F2L(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand_long(np.int64(frame.pop_operand()))


@unsafe_singleton
class F2D(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand_double(np.float64(frame.pop_operand()))


@unsafe_singleton
class D2I(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand(np.int32(frame.pop_operand_double()))


@unsafe_singleton
class D2L(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand_long(np.int64(frame.pop_operand_double()))


@unsafe_singleton
class D2F(NoOperandInstruction):
    def execute(self, frame):
        frame.push_operand(np.float32(frame.pop_operand_double()))
