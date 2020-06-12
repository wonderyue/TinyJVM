from runtime_data.heap.string import intern


def intern(frame):
    this = frame.get_this()
    frame.push_operand(intern(this))
