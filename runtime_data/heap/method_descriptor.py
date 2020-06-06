
class MethodDescriptor:
    def __init__(self):
        self.parameter_types = []
        self.return_type = ""

    def add_parameter_type(self, t):
        self.parameter_types.append(t)


class MethodDescriptorParser:
    def __init__(self):
        self.raw = ""
        self.offset = 0
        self.parsed = None

    @staticmethod
    def parse(raw_descriptor):
        parser = MethodDescriptorParser()
        return parser._parse(raw_descriptor)

    def _parse(self, raw_descriptor):
        self.raw = raw_descriptor
        self.parsed = MethodDescriptor()
        self._start_params()
        self._parse_param_types()
        self._end_params()
        self._parse_return_type()
        self._finish()
        return self.parsed

    def _start_params(self):
        if self._read_uint8() != '(':
            self._error()

    def _end_params(self):
        if self._read_uint8() != ')':
            self._error()

    def _finish(self):
        if self.offset != len(self.raw):
            self._error()

    def _error(self):
        raise RuntimeError("BAD descriptor: {0}".format(self.raw))

    def _read_uint8(self):
        b = self.raw[self.offset]
        self.offset += 1
        return b

    def _unread_uint8(self):
        self.offset -= 1

    def _parse_param_types(self):
        while True:
            t = self._parse_field_type()
            if t != "":
                self.parsed.add_parameter_type(t)
            else:
                break

    def _parse_return_type(self):
        if self._read_uint8() == 'V':
            self.parsed.return_type = "V"
            return
        self._unread_uint8()
        t = self._parse_field_type()
        if t != "":
            self.parsed.return_type = t
            return
        self._error()

    def _parse_field_type(self):
        field_type = self._read_uint8()
        if field_type in {'B', 'C', 'D', 'F', 'I', 'J', 'S', 'Z'}:
            return field_type
        elif field_type == 'L':
            return self._parse_object_type()
        elif field_type == '[':
            return self._parse_array_type()
        else:
            self._unread_uint8()
            return ""

    def _parse_object_type(self):
        unread = self.raw[self.offset:]
        semicolon_index = unread.find(";")
        if semicolon_index == -1:
            self._error()
            return ""
        else:
            obj_start = self.offset - 1
            obj_end = self.offset + semicolon_index + 1
            self.offset = obj_end
            descriptor = self.raw[obj_start:obj_end]
            return descriptor

    def _parse_array_type(self):
        arr_start = self.offset - 1
        self._parse_field_type()
        arr_end = self.offset
        descriptor = self.raw[arr_start:arr_end]
        return descriptor
