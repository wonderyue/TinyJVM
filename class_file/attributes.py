
def name_attribute_parser(name, reader, constant_pool):
    return {"name": name}


def name_value_attribute_parser(name, reader, constant_pool):
    return {"name": name, "val": constant_pool.get_constant_value(reader.read_int(2))}


def code_attribute_parser(name, reader, constant_pool):
    """
    Code_attribute {
        u2 attribute_name_index; 
        u4 attribute_length;
        u2 max_stack;
        u2 max_locals;
        u4 code_length;
        u1 code[code_length];
        u2 exception_table_length; 
        {   u2 start_pc;
            u2 end_pc;
            u2 handler_pc; 
            u2 catch_type;
        } exception_table[exception_table_length]; 
        u2 attributes_count;
        attribute_info attributes[attributes_count];
    }
    """
    return {
        "name": name,
        "max_stack": reader.read_int(2),
        "max_locals": reader.read_int(2),
        "code": reader.read_byte(reader.read_int(4)),
        "exception_table": code_exception_parser(reader, constant_pool),
        "attributes": Attributes(reader, constant_pool)
    }


def code_exception_parser(reader, constant_pool):
    count = reader.read_int(2)
    table = []
    for _ in range(count):
        table.append({
            "start_pc": reader.read_int(2),
            "end_pc": reader.read_int(2),
            "handler_pc": reader.read_int(2),
            "catch_type": reader.read_int(2),
        })
    return table


class Attributes:

    _name2parser = {
        "Deprecated": name_attribute_parser,
        "Synthetic": name_attribute_parser,
        "SourceFile": name_value_attribute_parser,
        "ConstantValue": name_value_attribute_parser,
        "Code": code_attribute_parser,
    }

    def __init__(self, reader, constant_pool):
        self._reader = reader
        self._constant_pool = constant_pool
        self._attribute_infos = []
        self._parse()

    @property
    def attribute_infos(self):
        return self._attribute_infos

    def _parse(self):
        count = self._reader.read_int(2)
        for _ in range(count):
            attribute_name_index = self._reader.read_int(2)
            attribute_length = self._reader.read_int(4)
            name = self._constant_pool.get_constant_value(attribute_name_index)
            if (attribute:=self._parse_attribute_info(name, attribute_length)) is not None:
                self._attribute_infos.append(attribute)

    def _parse_attribute_info(self, name, length):
        if name not in self._name2parser:
            self._reader.read_int(length)
            return None
        return self._name2parser[name](name, self._reader, self._constant_pool)
