from instructions.base import Instruction, NoOperandInstruction, BranchOperandMixin
import numpy as np
from utils.singleton import unsafe_singleton


class GOTO(BranchOperandMixin, Instruction):
    def execute(self, frame):
        frame.jump(self.offset)


class TABLE_SWITCH(Instruction):
    def fetch_operand(self, reader):
        reader.skip_padding()
        self.defaultOffset = reader.read_int(4)
        self.low = reader.read_int(4)
        self.high = reader.read_int(4)
        count = self.high - self.low + 1
        self.jumpOffsets = [reader.read_int(4) for _ in range(count)]

    def execute(self, frame):
        index = frame.pop_operand()
        if index >= self.low and index <= self.high:
            offset = self.jumpOffsets[index-self.low]
        else:
            offset = self.defaultOffset
        frame.jump(offset)


class LOOKUP_SWITCH(Instruction):
    def fetch_operand(self, reader):
        reader.skip_padding()
        self.defaultOffset = reader.read_int(4)
        self.npairs = reader.read_int(4)
        self.matchOffsets = {reader.read_int(
            4): reader.read_int(4) for _ in range(self.npairs)}

    def execute(self, frame):
        key = frame.pop_operand()
        if key in self.matchOffsets:
            offset = self.matchOffsets[key]
        else:
            offset = self.defaultOffset
        frame.jump(offset)


@unsafe_singleton
class RETURN(NoOperandInstruction):
    def execute(self, frame):
        frame.thread.pop_frame()


@unsafe_singleton
class IRETURN(NoOperandInstruction):
    def execute(self, frame):
        return_frame = frame.thread.pop_frame()
        cur_frame = frame.thread.current_frame()
        cur_frame.push_operand(return_frame.pop_operand())


@unsafe_singleton
class DRETURN(NoOperandInstruction):
    def execute(self, frame):
        return_frame = frame.thread.pop_frame()
        cur_frame = frame.thread.current_frame()
        cur_frame.push_operand_double(return_frame.pop_operand_double())


@unsafe_singleton
class LRETURN(NoOperandInstruction):
    def execute(self, frame):
        return_frame = frame.thread.pop_frame()
        cur_frame = frame.thread.current_frame()
        cur_frame.push_operand_long(return_frame.pop_operand_long())
