from runtime_data.thread import Thread
from runtime_data.frame import Frame
from interpreter.bytecode_reader import BytecodeReader
from instructions.opcode_map import opcode2instruction
from debug import log_frames, log_instruction


class Interpreter:
    def __init__(self, class_method):
        thread = Thread()
        thread.push_frame(Frame(thread, class_method))
        try:
            self.run(thread, class_method.code)
        except Exception as e:
            print(e)
            log_frames(thread)

    def run(self, thread, code):
        reader = BytecodeReader()
        while not thread.is_stack_empty():
            frame = thread.current_frame()
            pc = frame.next_pc
            thread.pc = pc
            reader.reset(frame.method.code, pc)
            opcode = reader.read_uint(1)
            if opcode not in opcode2instruction:
                raise RuntimeError("Unsupported opcode: {0}".format(hex(opcode)))
            instruction = opcode2instruction[opcode]
            instruction.fetch_operand(reader)
            frame.next_pc = reader.pc
            log_instruction(frame, opcode, instruction)
            instruction.execute(frame)
