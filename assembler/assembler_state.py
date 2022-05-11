class AssemblerState:
    def __init__(self) -> None:
        self.program = [0] * (2**16)  # there is memory to waste on my pc :D
        self.sp = 0
        self.pc = 0
        self.origin = 0
        self.labels = {}

    def word_directive(self, val):
        self.program[self.origin] = val
        self.origin += 1

    def origin_directive(self, val):
        self.origin = val

    def sp_directive(self):
        self.sp = self.origin

    def pc_directive(self):
        self.pc = self.origin

    def add_label(self, label):
        self.labels[label] = self.origin
