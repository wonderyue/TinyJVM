from runtime_data.heap.string import new_string, python_string


def get_primitive_class(frame):
    """
    public final class Integer extends Number implements Comparable<Integer> {
        ...
        public static final Class<Integer> TYPE = (Class<Integer>) Class.getPrimitiveClass("int");
        ...
    }
    static native Class<?> getPrimitiveClass(String name);
    """
    name_obj = frame.get_local(0)
    name = python_string(name_obj).replace(".", "/")
    loader = frame.method.clazz.loader
    class_obj = loader.load_class(name).class_obj
    frame.push_operand(class_obj)


def get_name_0(frame):
    """
    private native String getName0()
    """
    this = frame.get_this()
    clazz = this.extra
    name_obj = new_string(clazz.loader, clazz.java_name)
    frame.push_operand(name_obj)


def desired_assertion_status_0(frame):
    """
    private static native boolean desiredAssertionStatus0(Class<?> clazz);
    """
    frame.push_operand(False)


# def for_name_0(frame):
#     """
#     private static native Class<?> forName0(String name, boolean initialize,
#                                             ClassLoader loader,
#                                             Class<?> caller)
#     """
#     get_primitive_class(frame)
