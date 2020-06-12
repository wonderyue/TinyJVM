from instructions.base import (
    Instruction,
    ConstantPoolIndexOperandMixin,
    NoOperandInstruction,
)
from utils.singleton import unsafe_singleton
from runtime_data.heap.utils import lookup_method_in_class
from runtime_data.heap import string
from native import register
from runtime_data.heap.utils import invoke_method


class NEW(ConstantPoolIndexOperandMixin, Instruction):
    def execute(self, frame):
        runtime_cp = frame.method.clazz.constant_pool
        class_ref = runtime_cp.get_constant_value(self.index)
        resolved_clazz = class_ref.resolved_class()
        if resolved_clazz.is_interface() or resolved_clazz.is_abstract():
            raise RuntimeError(
                "java.lang.InstantiationError: " + resolved_clazz.class_name
            )
        # try invoke clinit
        if not resolved_clazz.is_clinit_started:
            frame.revert_next_pc()
            resolved_clazz.clinit(frame.thread)
            return

        frame.push_operand(resolved_clazz.new_object())


class PUT_STATIC(ConstantPoolIndexOperandMixin, Instruction):
    def execute(self, frame):
        runtime_cp = frame.method.clazz.constant_pool
        field_ref = runtime_cp.get_constant_value(self.index)
        resolved_field = field_ref.resolved_member()
        clazz = resolved_field.clazz
        if not resolved_field.is_static():
            raise RuntimeError(
                "java.lang.IncompatibleClassChangeError: {0}.{1}".format(
                    clazz.class_name, resolved_field.name
                )
            )
        if resolved_field.is_final():
            if frame.method.clazz != clazz or frame.method.name != "<clinit>":
                raise RuntimeError(
                    "java.lang.IllegalAccessError: {0}.{1}".format(
                        clazz.class_name, resolved_field.name
                    )
                )
        # try invoke clinit
        if not clazz.is_clinit_started:
            frame.revert_next_pc()
            clazz.clinit(frame.thread)
            return

        initial = resolved_field.descriptor[0]
        val = None
        if initial == "J":
            val = frame.pop_operand_long()
        elif initial == "D":
            val = frame.pop_operand_double()
        else:
            val = frame.pop_operand()
        clazz.static_fields[resolved_field.index] = val


class GET_STATIC(ConstantPoolIndexOperandMixin, Instruction):
    def execute(self, frame):
        runtime_cp = frame.method.clazz.constant_pool
        field_ref = runtime_cp.get_constant_value(self.index)
        resolved_field = field_ref.resolved_member()
        clazz = resolved_field.clazz
        if not resolved_field.is_static():
            raise RuntimeError(
                "java.lang.IncompatibleClassChangeError: {0}.{1}".format(
                    clazz.class_name, resolved_field.name
                )
            )
        # try invoke clinit
        if not clazz.is_clinit_started:
            frame.revert_next_pc()
            clazz.clinit(frame.thread)
            return
        initial = resolved_field.descriptor[0]
        val = clazz.static_fields[resolved_field.index]
        if initial == "J":
            frame.push_operand_long(val)
        elif initial == "D":
            frame.push_operand_double(val)
        else:
            frame.push_operand(val)


class PUT_FIELD(ConstantPoolIndexOperandMixin, Instruction):
    def execute(self, frame):
        runtime_cp = frame.method.clazz.constant_pool
        field_ref = runtime_cp.get_constant_value(self.index)
        field = field_ref.resolved_member()
        clazz = field.clazz
        if field.is_static():
            raise RuntimeError(
                "java.lang.IncompatibleClassChangeError: {0}.{1}".format(
                    clazz.class_name, field.name
                )
            )
        if field.is_final():
            if frame.method.clazz != clazz or frame.method.name != "<init>":
                raise RuntimeError(
                    "java.lang.IllegalAccessError: {0}.{1}".format(
                        clazz.class_name, field.name
                    )
                )
        initial = field.descriptor[0]
        val = None
        if initial == "J":
            val = frame.pop_operand_long()
        elif initial == "D":
            val = frame.pop_operand_double()
        else:
            val = frame.pop_operand()
        obj = frame.pop_operand()
        if obj is None:
            raise RuntimeError("java.lang.NullPointerException")
        obj[field.index] = val


class GET_FIELD(ConstantPoolIndexOperandMixin, Instruction):
    def execute(self, frame):
        runtime_cp = frame.method.clazz.constant_pool
        field_ref = runtime_cp.get_constant_value(self.index)
        field = field_ref.resolved_member()
        clazz = field.clazz
        if field.is_static():
            raise RuntimeError(
                "java.lang.IncompatibleClassChangeError: {0}.{1}".format(
                    clazz.class_name, field.name
                )
            )
        obj = frame.pop_operand()
        if obj is None:
            raise RuntimeError("java.lang.NullPointerException")
        val = obj[field.index]
        initial = field.descriptor[0]
        if initial == "J":
            frame.push_operand_long(val)
        elif initial == "D":
            frame.push_operand_double(val)
        else:
            frame.push_operand(val)


class INSTANCE_OF(ConstantPoolIndexOperandMixin, Instruction):
    def execute(self, frame):
        obj = frame.pop_operand()
        if obj is None:
            frame.push_operand(0)
            return
        runtime_cp = frame.method.clazz.constant_pool
        class_ref = runtime_cp.get_constant_value(self.index)
        clazz = class_ref.resolved_class()
        if obj.is_instance_of(clazz):
            frame.push_operand(1)
        else:
            frame.push_operand(0)


class CHECK_CAST(ConstantPoolIndexOperandMixin, Instruction):
    def execute(self, frame):
        obj = frame.pop_operand()
        frame.push_operand(obj)
        if obj is None:
            frame.push_operand(0)
            return
        runtime_cp = frame.method.clazz.constant_pool
        class_ref = runtime_cp.get_constant_value(self.index)
        clazz = class_ref.resolved_class()
        if not obj.is_instance_of(clazz):
            raise RuntimeError("java.lang.ClassCastException")


class INVOKE_STATIC(ConstantPoolIndexOperandMixin, Instruction):
    def execute(self, frame):
        runtime_cp = frame.method.clazz.constant_pool
        method_ref = runtime_cp.get_constant_value(self.index)
        resolved_method = method_ref.resolved_member()
        if not resolved_method.is_static():
            raise RuntimeError(
                "java.lang.IncompatibleClassChangeError: {0}.{1}".format(
                    resolved_method.clazz.class_name, resolved_method.name
                )
            )
        # try invoke clinit
        if not resolved_method.clazz.is_clinit_started:
            frame.revert_next_pc()
            resolved_method.clazz.clinit(frame.thread)
            return
        invoke_method(frame, resolved_method)


class INVOKE_INTERFACE(ConstantPoolIndexOperandMixin, Instruction):
    def fetch_operand(self, reader):
        self.index = reader.read_uint(2)
        reader.read_uint(1)  # count
        reader.read_uint(1)  # must be 0

    def execute(self, frame):
        cur_class = frame.method.clazz
        runtime_cp = cur_class.constant_pool
        method_ref = runtime_cp.get_constant_value(self.index)
        resolved_clazz = method_ref.resolved_class()
        resolved_method = method_ref.resolved_member()

        if resolved_method.is_static() or resolved_method.is_private():
            raise RuntimeError(
                "java.lang.IncompatibleClassChangeError: {0}.{1}".format(
                    resolved_clazz.class_name, resolved_method.name
                )
            )

        this_ref = frame.get_operand_from_top(resolved_method.arg_index)
        if this_ref is None:
            raise RuntimeError(
                "java.lang.NullPointerException {0}.{1}".format(
                    resolved_clazz.class_name, resolved_method.name
                )
            )

        if not this_ref.clazz.is_implements(resolved_method.clazz):
            raise RuntimeError(
                "java.lang.IncompatibleClassChangeError: {0}.{1}".format(
                    resolved_clazz.class_name, resolved_method.name
                )
            )

        resolved_method = lookup_method_in_class(
            this_ref.clazz, method_ref.name, method_ref.descriptor
        )
        if resolved_method.is_abstract():
            raise RuntimeError(
                "java.lang.AbstractMethodError {0}.{1}".format(
                    resolved_clazz.class_name, resolved_method.name
                )
            )

        if not resolved_method.is_public():
            raise RuntimeError(
                "java.lang.IllegalAccessError {0}.{1}".format(
                    resolved_clazz.class_name, resolved_method.name
                )
            )

        invoke_method(frame, resolved_method)


class INVOKE_SPECIAL(ConstantPoolIndexOperandMixin, Instruction):
    "Invoke instance method without dynamic binding"

    def execute(self, frame):
        cur_class = frame.method.clazz
        runtime_cp = cur_class.constant_pool
        method_ref = runtime_cp.get_constant_value(self.index)
        resolved_clazz = method_ref.resolved_class()
        resolved_method = method_ref.resolved_member()

        if resolved_method.is_static():
            raise RuntimeError(
                "java.lang.IncompatibleClassChangeError: {0}.{1}".format(
                    resolved_clazz.class_name, resolved_method.name
                )
            )
        # init cannot be called by a derived class
        if resolved_method.name == "<init>" and resolved_method.clazz != resolved_clazz:
            raise RuntimeError(
                "java.lang.NoSuchMethodError: {0}.{1}".format(
                    resolved_clazz.class_name, resolved_method.name
                )
            )

        this_ref = frame.get_operand_from_top(resolved_method.arg_index)
        if this_ref is None:
            raise RuntimeError(
                "java.lang.NullPointerException {0}.{1}".format(
                    resolved_clazz.class_name, resolved_method.name
                )
            )

        if (
            resolved_method.is_protected()
            and resolved_method.clazz.is_super_class_of(cur_class)
            and resolved_method.clazz.get_package_name() != cur_class.get_package_name()
            and this_ref.clazz != cur_class
            and not this_ref.clazz.is_sub_class_of(cur_class)
        ):
            raise RuntimeError(
                "java.lang.IllegalAccessError {0}.{1}".format(
                    resolved_clazz.class_name, resolved_method.name
                )
            )

        if (
            cur_class.is_super()
            and resolved_clazz.is_super_class_of(cur_class)
            and resolved_method.name != "<init>"
        ):
            resolved_method = lookup_method_in_class(
                cur_class.super_class, method_ref.name, method_ref.descriptor
            )

        if resolved_method.is_abstract():
            raise RuntimeError(
                "java.lang.AbstractMethodError {0}.{1}".format(
                    resolved_clazz.class_name, resolved_method.name
                )
            )

        invoke_method(frame, resolved_method)


class INVOKE_VIRTUAL(ConstantPoolIndexOperandMixin, Instruction):
    def execute(self, frame):
        """
        Example:

        public class Test {
            public static void main(String[] args) {
                System.out.println("Hello World");
            }
        }

        INVOKE_VIRTUAL of println:
        cur_class: Test
        cur_method: main
        resolved_clazz: PrintStream (System.out)
        resolved_method: println 
        """
        cur_class = frame.method.clazz
        runtime_cp = cur_class.constant_pool
        method_ref = runtime_cp.get_constant_value(self.index)
        resolved_clazz = method_ref.resolved_class()
        resolved_method = method_ref.resolved_member()

        if resolved_method.is_static():
            raise RuntimeError(
                "java.lang.IncompatibleClassChangeError: {0}.{1}".format(
                    resolved_clazz.class_name, resolved_method.name
                )
            )

        this_ref = frame.get_operand_from_top(resolved_method.arg_index)
        if this_ref is None:
            if method_ref.name == "println":
                self._println(frame, method_ref.descriptor)
                return
            raise RuntimeError(
                "java.lang.NullPointerException {0}.{1}".format(
                    resolved_clazz.class_name, resolved_method.name
                )
            )

        if (
            resolved_method.is_protected()
            and resolved_method.clazz.is_super_class_of(cur_class)
            and resolved_method.clazz.get_package_name() != cur_class.get_package_name()
            and this_ref.clazz != cur_class
            and not this_ref.clazz.is_sub_class_of(cur_class)
        ):
            raise RuntimeError(
                "java.lang.IllegalAccessError {0}.{1}".format(
                    resolved_clazz.class_name, resolved_method.name
                )
            )

        resolved_method = lookup_method_in_class(
            this_ref.clazz, method_ref.name, method_ref.descriptor
        )
        if resolved_method.is_abstract():
            raise RuntimeError(
                "java.lang.AbstractMethodError {0}.{1}".format(
                    resolved_clazz.class_name, resolved_method.name
                )
            )

        invoke_method(frame, resolved_method)

    def _println(self, frame, descriptor):
        if descriptor == "(Z)V":
            print("{0}".format(frame.pop_operand() != 0))
        elif descriptor == "(J)V":
            print("{0}".format(frame.pop_operand_long()))
        elif descriptor == "(D)V":
            print("{0}".format(frame.pop_operand_double()))
        elif descriptor in {"(C)V", "(B)V", "(S)V", "(I)V", "(F)V"}:
            print("{0}".format(frame.pop_operand()))
        elif descriptor == "(Ljava/lang/String;)V":
            print(string.python_string(frame.pop_operand()))
        else:
            raise RuntimeError("println: " + descriptor)
        frame.pop_operand()


class NEW_ARRAY(Instruction):
    def fetch_operand(self, reader):
        self.atype = reader.read_uint(1)

    def execute(self, frame):
        count = frame.pop_operand()
        if count < 0:
            raise RuntimeError("java.lang.NegativeArraySizeException")
        class_loader = frame.method.clazz.loader
        arr_class = class_loader.load_array(self.atype)
        arr_obj = arr_class.new_array_object(count)
        frame.push_operand(arr_obj)


class ANEW_ARRAY(ConstantPoolIndexOperandMixin, Instruction):
    def execute(self, frame):
        cur_class = frame.method.clazz
        runtime_cp = cur_class.constant_pool
        class_ref = runtime_cp.get_constant_value(self.index)
        resolved_clazz = class_ref.resolved_class()
        count = frame.pop_operand()
        if count < 0:
            raise RuntimeError("java.lang.NegativeArraySizeException")
        arr_class = resolved_clazz.get_array_class()
        arr_obj = arr_class.new_array_object(count)
        frame.push_operand(arr_obj)


@unsafe_singleton
class ARRAY_LENGTH(NoOperandInstruction):
    def execute(self, frame):
        arr_obj = frame.pop_operand()
        if arr_obj is None:
            raise RuntimeError("java.lang.NullPointerException")
        frame.push_operand(arr_obj.length)


@unsafe_singleton
class INVOKE_NATIVE(NoOperandInstruction):
    def execute(self, frame):
        native_method = register.find_native_method(
            frame.method.clazz.class_name, frame.method.name, frame.method.descriptor
        )
        if native_method is None:
            raise RuntimeError(
                "java.lang.UnsatisfiedLinkError: {0}.{1}{2}".format(
                    frame.method.clazz.class_name,
                    frame.method.name,
                    frame.method.descriptor,
                )
            )
        native_method(frame)
