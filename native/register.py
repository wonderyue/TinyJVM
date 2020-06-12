from native.java.lang.object import hash_code, get_class, clone
from native.java.lang.clazz import (
    get_primitive_class,
    get_name_0,
    desired_assertion_status_0,
)
from native.sun.reflect.reflection import get_caller_class
from native.java.lang.system import array_copy
from native.java.lang.float import float_to_raw_int_bits, int_bits_to_float
from native.java.lang.double import double_to_raw_long_bits, long_bits_to_double
from native.java.lang.string import intern
from native.sun.misc.vm import initialize


def _empty_native_method(frame):
    pass


def _empty_native_method_with_return(frame):
    frame.push_operand(None)


_native_method = {
    "java/lang/Object@getClass@()Ljava/lang/Class;": get_class,
    "java/lang/Object@hashCode@()I": hash_code,
    "java/lang/Object@clone@()Ljava/lang/Object;": clone,
    "java/lang/Class@getPrimitiveClass@(Ljava/lang/String;)Ljava/lang/Class;": get_primitive_class,
    "java/lang/Class@getName0@()Ljava/lang/String;": get_name_0,
    "java/lang/Class@desiredAssertionStatus0@(Ljava/lang/Class;)Z": desired_assertion_status_0,
    "sun/reflect/Reflection@getCallerClass@()Ljava/lang/Class;": get_caller_class,
    "java/lang/Class@forName0@(Ljava/lang/String;ZLjava/lang/ClassLoader;Ljava/lang/Class;)Ljava/lang/Class;": get_primitive_class,
    "java/security/AccessController@doPrivileged@(Ljava/security/PrivilegedAction;)Ljava/lang/Object;": _empty_native_method_with_return,
    "java/lang/System@arraycopy@(Ljava/lang/Object;ILjava/lang/Object;II)V": array_copy,
    "java/lang/Float@floatToRawIntBits@(F)I": float_to_raw_int_bits,
    "java/lang/Float@intBitsToFloat@(I)F": int_bits_to_float,
    "java/lang/Double@doubleToRawLongBits@(D)J": double_to_raw_long_bits,
    "java/lang/Double@longBitsToDouble@(J)D": long_bits_to_double,
    "java/lang/String@intern@()Ljava/lang/String;": intern,
    "sun/misc/VM@initialize@()V": initialize,
}


def register(class_name, method_name, method_descripter, native_method):
    _native_method[
        class_name + "@" + method_name + "@" + method_descripter
    ] = native_method


def find_native_method(class_name, method_name, method_descripter):
    if method_name == "registerNatives":
        return _empty_native_method
    return _native_method.get(class_name + "@" + method_name + "@" + method_descripter)
