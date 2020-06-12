
def get_caller_class(frame):
    frame.push_operand(frame.method.clazz.class_obj)
