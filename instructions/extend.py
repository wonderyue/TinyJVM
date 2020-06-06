from instructions.base import Instruction, NoOperandInstruction, BranchOperandMixin
from instructions.controls import GOTO


class WIDE(Instruction):

    def fetch_operand(self, reader):
        from instructions.opcode_map import opcode2instruction
        opcode = reader.read_uint(1)
        self.modifiedInstruction = opcode2instruction[opcode]
        if opcode == 0x84:  # IINC
            self.modifiedInstruction.index = reader.read_uint(2)
            self.modifiedInstruction.const = reader.read_int(2)
        else:
            self.modifiedInstruction.index = reader.read_uint(2)

    def execute(self, frame):
        self.modifiedInstruction.execute(frame)


class IFNULL(BranchOperandMixin, Instruction):
    def execute(self, frame):
        val = frame.pop_operand()
        if val is None:
            frame.jump(self.offset)


class IFNONNULL(BranchOperandMixin, Instruction):
    def execute(self, frame):
        val = frame.pop_operand()
        if val is not None:
            frame.jump(self.offset)


class GOTO_W(GOTO):
    def fetch_operand(self, reader):
        self.offset = reader.read_int(4)
