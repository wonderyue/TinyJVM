from runtime_data.heap.utils import invoke_method


def do_privileged(frame):
    "public static native <T> T doPrivileged(PrivilegedAction<T> action)"
    action = frame.get_local(0)
    frame.push_operand(action)
    method = action.clazz.get_instance_method("run", "()Ljava/lang/Object;")
    invoke_method(frame, method)


def get_stack_access_control_context(frame):
    "private static native AccessControlContext getStackAccessControlContext()"
    frame.push_operand(None)
