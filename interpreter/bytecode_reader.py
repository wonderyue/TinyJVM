
import struct
from utils.reader_mixin import ReaderMixin
from utils.singleton import unsafe_singleton


@unsafe_singleton
class BytecodeReader(ReaderMixin):

    def reset(self, code, pc):
        self._code = code
        self._pc = pc
        return self

    @property
    def pc(self):
        return self._pc

    @pc.setter
    def pc(self, pc):
        self._pc = pc

    def read_byte(self, n):
        res = self._code[self._pc:self._pc+n]
        self.pc += n
        return res

    def skip_padding(self):
        if self._pc % 4 != 0:
            self.read_byte(4 - (self._pc % 4))
