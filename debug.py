import traceback

DEBUG = True


def print_stack():
    traceback.print_stack()


def log_frames(thread):
    while not thread.is_stack_empty():
        frame = thread.pop_frame()
        print(
            ">> pc:{0} {1}.{2}{3}".format(
                frame.next_pc,
                frame.method.clazz.class_name,
                frame.method.name,
                frame.method.descriptor,
            )
        )


def log_instruction(frame, opcode, instruction):
    if DEBUG:
        print(
            "{0}.{1}() pc:{2} opcode:{3} inst:{4}".format(
                frame.method.clazz.class_name,
                frame.method.name,
                frame.thread.pc,
                hex(opcode),
                instruction,
            )
        )
