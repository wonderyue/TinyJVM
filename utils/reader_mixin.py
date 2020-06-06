import struct


class ReaderMixin:

    def read_byte(self, n):
        raise NotImplementedError

    def read_uint(self, n):
        return int.from_bytes(self.read_byte(n), byteorder='big', signed=False)

    def read_int(self, n):
        return int.from_bytes(self.read_byte(n), byteorder='big', signed=True)

    def read_float(self):
        return struct.unpack('>f', self.read_byte(4))[0]

    def read_double(self):
        return struct.unpack('>d', self.read_byte(8))[0]

    def read_string(self, n):
        return self.read_byte(n).decode("utf-8")
