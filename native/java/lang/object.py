
def hash_code(frame):
    frame.push_operand(hash(frame.get_this()))


def get_class(frame):
    this = frame.get_this()
    frame.push_operand(this.clazz.class_obj)


def clone(frame):
    this = frame.get_this()
    cloneable = this.clazz.loader.load_class("java/lang/Cloneable")
    if not this.clazz.is_implements(cloneable):
        raise RuntimeError("java.lang.CloneNotSupportedException")
    frame.push_operand(this.clone())
