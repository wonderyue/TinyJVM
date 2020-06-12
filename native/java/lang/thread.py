def current_thread(frame):
    "public static native Thread currentThread()"
    class_loader = frame.method.clazz.loader
    thread_obj = class_loader.load_class("java/lang/Thread").new_object()
    group_obj = class_loader.load_class("java/lang/ThreadGroup").new_object()
    thread_obj.set_field_value("group", "Ljava/lang/ThreadGroup;", group_obj)
    thread_obj.set_field_value("priority", "I", 1)
    frame.push_operand(thread_obj)


def is_alive(frame):
    "public final native boolean isAlive()"
    frame.push_operand(False)
