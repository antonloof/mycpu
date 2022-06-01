class AssemblerState:
    def __init__(self) -> None:
        self.program = [0] * (2 ** 16)  # there is memory to waste on my pc :D
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

    def insert_8_8_8_8(self, a, b, c, d):
        self.insert_to_program((a << 24) + (b << 16) + (c << 8) + (d))

    def insert_8_8_16(self, a, b, c):
        self.insert_to_program((a << 24) + (b << 16) + (c))

    def insert_8_8_8_8_32(self, a, b, c, d, e):
        self.insert_8_8_8_8(a, b, c, d)
        self.insert_to_program(e)

    def insert_8_8_8_8_16(self, a, b, c, d, e):
        self.insert_8_8_8_8(a, b, c, d)
        self.insert_to_program(e)

    def insert_8_8_16_16(self, a, b, c, d):
        self.insert_8_8_16(a, b, c)
        self.insert_to_program(d)

    def insert_to_program(self, val):
        self.program[self.origin] = val
        self.origin += 1
