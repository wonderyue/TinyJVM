class Interfaces:

    def __init__(self, reader, constant_pool):
        self._reader = reader
        self._constant_pool = constant_pool
        self._interfaces = []
        self.parse()

    def parse(self):
        count = self._reader.read_uint(2)
        for _ in range(count):
            self._interfaces.append(self._reader.read_uint(2))

    def get_interface_names(self):
        return [self._constant_pool.get_class_name(
            index) for index in self._interfaces]
