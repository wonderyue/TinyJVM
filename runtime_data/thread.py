
class Thread:

    def __init__(self):
        self._pc = 0
        self._stack_frames = []

    @property
    def pc(self):
        return self._pc

    @pc.setter
    def pc(self, pc):
        self._pc = pc

    def push_frame(self, frame):
        self._stack_frames.append(frame)

    def pop_frame(self):
        return self._stack_frames.pop()

    def current_frame(self):
        return self._stack_frames[-1]

    def is_stack_empty(self):
        return len(self._stack_frames) == 0
