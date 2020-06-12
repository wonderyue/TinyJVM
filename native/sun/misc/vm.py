from runtime_data.heap.string import new_string
from runtime_data.heap.utils import invoke_method


def initialize(frame):
    vm_class = frame.method.clazz
    saved_props = vm_class.get_static_field("savedProps", "Ljava/util/Properties;")
    key = new_string(vm_class.loader, "foo")
    val = new_string(vm_class.loader, "bar")
    frame.push_operand(saved_props)
    frame.push_operand(key)
    frame.push_operand(val)
    props_class = vm_class.loader.load_class("java/util/Properties")
    set_prop_method = props_class.get_instance_method(
        "setProperty", "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/Object;"
    )
    invoke_method(frame, set_prop_method)
