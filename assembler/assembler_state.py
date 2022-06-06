import struct
from collections import defaultdict


class AssemblerState:
    def __init__(self) -> None:
        self.program = [0] * (2**16)  # there is memory to waste on my pc :D
        self.origin = 0
        self.labels = {}
        self.undeclared_labels = defaultdict(list)

    def handle_label(self, label, pc_offset, addr_offset_shorts):
        if label in self.labels:
            return self.labels[label]
        self.undeclared_labels[label].append((self.origin + pc_offset, addr_offset_shorts))
        return 0

    def program_as_bytearry(self):
        return struct.pack(f"{2**16}I", *self.program)

    def word_directive(self, val):
        self.program[self.origin] = val
        self.origin += 1

    def origin_directive(self, val):
        self.origin = val

    def add_label(self, label):
        self.labels[label] = self.origin
        if label in self.undeclared_labels:
            for pc, addr_offset_shorts in self.undeclared_labels.pop(label):
                self.program[pc] |= self.origin << (addr_offset_shorts * 16)

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
