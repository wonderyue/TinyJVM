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


def new_multi_dimensions_array(counts, level, arr_class):
    arr_obj = arr_class.new_array_object(counts[-level])
    if level < len(counts):
        for i in range(arr_obj.length):
            arr_obj[i] = new_multi_dimensions_array(
                counts, level+1, arr_class.get_component_class())
    return arr_obj


class MULTI_ANEW_ARRAY(Instruction):

    def fetch_operand(self, reader):
        self.index = reader.read_uint(2)
        self.dimensions = reader.read_uint(1)

    def execute(self, frame):
        cur_class = frame.method.clazz
        runtime_cp = cur_class.constant_pool
        class_ref = runtime_cp.get_constant_value(self.index)
        resolved_clazz = class_ref.resolved_class()
        counts = []
        for _ in range(self.dimensions):
            count = frame.pop_operand()
            if count < 0:
                raise RuntimeError("java.lang.NegativeArraySizeException")
            counts.append(count)
        arr_obj = new_multi_dimensions_array(counts, 1, resolved_clazz)
        frame.push_operand(arr_obj)
