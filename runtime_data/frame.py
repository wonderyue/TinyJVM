import struct


class Frame:
    def __init__(self, thread, method):
        self._thread = thread
        self._method = method
        self._local_vars = [None] * method.max_locals
        self._operand_stack = []
        self._next_pc = 0

    @property
    def thread(self):
        return self._thread

    @property
    def method(self):
        return self._method

    @property
    def next_pc(self):
        return self._next_pc

    @next_pc.setter
    def next_pc(self, next_pc):
        self._next_pc = next_pc

    def revert_next_pc(self):
        self._next_pc = self.thread.pc

    def jump(self, offset):
        self.next_pc = self.thread.pc + offset

    def set_local(self, index, val):
        self._local_vars[index] = val

    def get_local(self, index):
        return self._local_vars[index]

    def set_local_long(self, index, val):
        self._local_vars[index : index + 2] = struct.unpack("ii", struct.pack("l", val))

    def get_local_long(self, index):
        return struct.unpack(
            "l", struct.pack("ii", self._local_vars[index], self._local_vars[index + 1])
        )[0]

    def set_local_double(self, index, val):
        self._local_vars[index : index + 2] = struct.unpack("ii", struct.pack("d", val))

    def get_local_double(self, index):
        return struct.unpack(
            "d", struct.pack("ii", self._local_vars[index], self._local_vars[index + 1])
        )[0]

    def push_operand(self, val):
        self._operand_stack.append(val)

    def pop_operand(self):
        return self._operand_stack.pop()

    def push_operand_long(self, val):
        t = struct.unpack("ii", struct.pack("l", val))
        self._operand_stack.append(t[0])
        self._operand_stack.append(t[1])

    def pop_operand_long(self):
        val2 = self._operand_stack.pop()
        val1 = self._operand_stack.pop()
        return struct.unpack("l", struct.pack("ii", val1, val2))[0]

    def push_operand_double(self, val):
        t = struct.unpack("ii", struct.pack("d", val))
        self._operand_stack.append(t[0])
        self._operand_stack.append(t[1])

    def pop_operand_double(self):
        val2 = self._operand_stack.pop()
        val1 = self._operand_stack.pop()
        return struct.unpack("d", struct.pack("ii", val1, val2))[0]

    def push_args(self, pre_frame):
        for i in range(self.method.arg_index):
            self.set_local(self.method.arg_index - i - 1, pre_frame.pop_operand())

    def get_operand_from_top(self, index):
        "start from 1"
        return self._operand_stack[-index]

    def get_this(self):
        return self.get_local(0)
