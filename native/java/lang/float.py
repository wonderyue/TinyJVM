import struct


def float_to_raw_int_bits(frame):
    """
    public static native int floatToRawIntBits(float value);
    """
    value = frame.get_local(0)
    b = struct.pack("f", value)
    i = struct.unpack("i", b)[0]
    frame.push_operand(i)


def int_bits_to_float(frame):
    """
    public static native float intBitsToFloat(int bits);
    """
    i = frame.get_local(0)
    b = struct.pack("i", i)
    value = struct.unpack("f", b)[0]
    frame.push_operand(value)
