from runtime_data.heap.object import Object


def array_copy(frame):
    src = frame.get_local(0)
    src_pos = frame.get_local(1)
    dest = frame.get_local(2)
    dest_pos = frame.get_local(3)
    length = frame.get_local(4)
    if src is None and dest is None:
        raise RuntimeError("java.lang.NullPointerException")
    if not check_array_copy(src, dest):
        raise RuntimeError("java.lang.ArrayStoreException")
    if (
        src_pos < 0
        or dest_pos < 0
        or length < 0
        or src_pos + length > src.length
        or dest_pos + length > dest.length
    ):
        raise RuntimeError("java.lang.IndexOutOfBoundsException")
    Object.array_copy(src, dest, src_pos, dest_pos, length)


def check_array_copy(src, dest) -> bool:
    if not src.clazz.is_array() or not dest.clazz.is_array():
        return False
    if (
        src.clazz.get_component_class().is_primitive()
        or dest.clazz.get_component_class().is_primitive()
    ):
        return src.clazz == dest.clazz
    return True
