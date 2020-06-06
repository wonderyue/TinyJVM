from abc import ABCMeta, abstractmethod


class Instruction(metaclass=ABCMeta):
    @abstractmethod
    def fetch_operand(self, reader):
        pass

    @abstractmethod
    def execute(self, frame):
        pass


class NoOperandInstruction(metaclass=ABCMeta):

    def fetch_operand(self, reader):
        pass

    @abstractmethod
    def execute(self, frame):
        pass


class BranchOperandMixin:

    def fetch_operand(self, reader):
        self.offset = reader.read_int(2)


class LocalIndexOperandMixin:
    "read uint8 as index of frame.local_vars"

    def fetch_operand(self, reader):
        self.index = reader.read_uint(1)


class ConstantPoolIndexOperandMixin:
    "read uint16 as index of classfile.constant_pool.constant_infos"

    def fetch_operand(self, reader):
        self.index = reader.read_uint(2)


class LoadLocalMixin:

    def execute(self, frame):
        frame.push_operand(frame.get_local(self.index))


class LoadLocalLongMixin:

    def execute(self, frame):
        frame.push_operand_long(frame.get_local_long(self.index))


class LoadLocalDoubleMixin:

    def execute(self, frame):
        frame.push_operand_double(frame.get_local_double(self.index))


class StoreLocalMixin:

    def execute(self, frame):
        frame.set_local(self.index, frame.pop_operand())


class StoreLocalLongMixin:

    def execute(self, frame):
        frame.set_local_long(self.index, frame.pop_operand_long())


class StoreLocalDoubleMixin:

    def execute(self, frame):
        frame.set_local_double(self.index, frame.pop_operand_double())
