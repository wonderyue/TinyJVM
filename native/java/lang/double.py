import struct


def double_to_raw_long_bits(frame):
    """
    public static native long doubleToRawLongBits(double value);
    """
    value = frame.get_local_double(0)
    b = struct.pack("d", value)
    i = struct.unpack("l", b)[0]
    frame.push_operand_long(i)


def long_bits_to_double(frame):
    """
    public static native double longBitsToDouble(long bits);
    """
    i = frame.get_local_long(0)
    b = struct.pack("l", i)
    value = struct.unpack("d", b)[0]
    frame.push_operand_double(value)
