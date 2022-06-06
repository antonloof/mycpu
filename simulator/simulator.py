def get_byte_i(n, i):
    return (n & (0xFF << (8 * i))) >> (8 * i)


def get_short_i(n, i):
    return (n & (0xFFFF << (16 * i))) >> (16 * i)


def parse_as_signed(a):
    return -(a & (1 << 31)) + (a & 0x7FFFFFFF)


ALU_MASK = 0xFFFFFFFF
SP = 255


class CpuState:
    def __init__(self, memory) -> None:
        self.pc = 0
        self.regs = [0] * 256
        self.memory = memory
        self.halted = False

    def next_opcode(self):
        return get_byte_i(self.memory[self.pc], 3)

    def run_next_instruction(self):
        instruction = getattr(self, f"run_instruction_{self.next_opcode():#010b}")
        instruction()

    def alu_2_reg(self, op):
        rx = get_byte_i(self.memory[self.pc], 2)
        ry = get_byte_i(self.memory[self.pc], 1)
        self.regs[rx] = op(self.regs[rx], self.regs[ry]) & ALU_MASK
        self.pc += 1

    def alu_1_reg_1_const(self, op):
        rx = get_byte_i(self.memory[self.pc], 2)
        num = get_short_i(self.memory[self.pc], 0)
        self.regs[rx] = op(self.regs[rx], num) & ALU_MASK
        self.pc += 1

    def run_instruction_0b00000000(self):
        # ST Rxx Ryy
        rx = get_byte_i(self.memory[self.pc], 2)
        ry = get_byte_i(self.memory[self.pc], 1)
        self.regs[rx] = self.regs[ry]
        self.pc += 1

    def run_instruction_0b00000001(self):
        # ST Rxx $num
        rx = get_byte_i(self.memory[self.pc], 2)
        num = get_short_i(self.memory[self.pc], 0)
        self.regs[rx] = self.memory[num]
        self.pc += 1

    def run_instruction_0b00000010(self):
        # ST $num Rxx
        rx = get_byte_i(self.memory[self.pc], 2)
        num = get_short_i(self.memory[self.pc], 0)
        self.memory[num] = self.regs[rx]
        self.pc += 1

    def run_instruction_0b00000011(self):
        # ST Rxx #num
        rx = get_byte_i(self.memory[self.pc], 2)
        self.pc += 1
        self.regs[rx] = self.memory[self.pc]
        self.pc += 1

    def run_instruction_0b00000100(self):
        # ST $Rxx Ryy
        rx = get_byte_i(self.memory[self.pc], 2)
        ry = get_byte_i(self.memory[self.pc], 1)
        self.memory[self.regs[rx]] = self.regs[ry]
        self.pc += 1

    def run_instruction_0b00000101(self):
        # ST Rxx $Ryy
        rx = get_byte_i(self.memory[self.pc], 2)
        ry = get_byte_i(self.memory[self.pc], 1)
        self.regs[rx] = self.memory[self.regs[ry]]
        self.pc += 1

    def run_instruction_0b01000000(self):
        # ADD Rxx Ryy
        self.alu_2_reg(lambda x, y: x + y)

    def run_instruction_0b01000001(self):
        # ADD Rxx #num
        self.alu_1_reg_1_const(lambda x, y: x + y)

    def run_instruction_0b01000010(self):
        # SUB Rxx Ryy
        self.alu_2_reg(lambda x, y: x - y)

    def run_instruction_0b01000011(self):
        # SUB Rxx #num
        self.alu_1_reg_1_const(lambda x, y: x - y)

    def run_instruction_0b01000100(self):
        # MUL Rxx Ryy
        self.alu_2_reg(lambda x, y: x * y)

    def run_instruction_0b01000101(self):
        # MUL Rxx #num
        self.alu_1_reg_1_const(lambda x, y: x * y)

    def run_instruction_0b01000110(self):
        # AND Rxx Ryy
        self.alu_2_reg(lambda x, y: x & y)

    def run_instruction_0b01000111(self):
        # AND Rxx #num
        self.alu_1_reg_1_const(lambda x, y: x & y)

    def run_instruction_0b01001000(self):
        # OR Rxx Ryy
        self.alu_2_reg(lambda x, y: x | y)

    def run_instruction_0b01001001(self):
        # OR Rxx #num
        self.alu_1_reg_1_const(lambda x, y: x | y)

    def run_instruction_0b01001010(self):
        # XOR Rxx Ryy
        self.alu_2_reg(lambda x, y: x ^ y)

    def run_instruction_0b01001011(self):
        # XOR Rxx #num
        self.alu_1_reg_1_const(lambda x, y: x ^ y)

    def run_instruction_0b01001101(self):
        # SHR Rxx Ryy
        self.alu_2_reg(lambda x, y: x >> y)

    def run_instruction_0b01001110(self):
        # SHR Rxx #num
        self.alu_1_reg_1_const(lambda x, y: x >> y)

    def run_instruction_0b01001111(self):
        # SHL Rxx Ryy
        self.alu_2_reg(lambda x, y: x << y)

    def run_instruction_0b01010000(self):
        # SHLR Rxx #num
        self.alu_1_reg_1_const(lambda x, y: x << y)

    def run_instruction_0b01001100(self):
        # INV Rxx
        rx = get_byte_i(self.memory[self.pc], 2)
        self.regs[rx] = (~self.regs[rx]) & ALU_MASK
        self.pc += 1

    def run_instruction_0b01010001(self):
        # MAC Rxx Ryy Rzz
        rx = get_byte_i(self.memory[self.pc], 2)
        ry = get_byte_i(self.memory[self.pc], 1)
        rz = get_byte_i(self.memory[self.pc], 0)
        self.regs[rx] = (self.regs[rx] + self.regs[ry] * self.regs[rz]) & ALU_MASK
        self.pc += 1

    def run_instruction_0b11000000(self):
        # PSH Rxx
        rx = get_byte_i(self.memory[self.pc], 2)
        self.memory[self.regs[SP]] = self.regs[rx]
        self.regs[SP] += 1
        self.pc += 1

    def run_instruction_0b11000001(self):
        # POP Rxx
        rx = get_byte_i(self.memory[self.pc], 2)
        self.regs[rx] = self.memory[self.regs[SP]]
        self.regs[SP] -= 1
        self.pc += 1

    def run_instruction_0b11000010(self):
        # NOP
        self.pc += 1

    def run_instruction_0b11000011(self):
        # HLT
        self.pc += 1
        self.halted = True

    def branch_2_reg(self, cmp):
        rx = get_byte_i(self.memory[self.pc], 2)
        ry = get_byte_i(self.memory[self.pc], 1)
        self.pc += 1
        if cmp(self.regs[rx], self.regs[ry]):
            self.pc = get_short_i(self.memory[self.pc], 0)
        else:
            self.pc += 1

    def branch_1_reg_1_const(self, cmp):
        rx = get_byte_i(self.memory[self.pc], 2)
        num = get_short_i(self.memory[self.pc], 0)
        self.pc += 1
        if cmp(self.regs[rx], num):
            self.pc = get_short_i(self.memory[self.pc], 0)
        else:
            self.pc += 1

    def run_instruction_0b10000000(self):
        # JMP $num
        self.pc = get_short_i(self.memory[self.pc + 1], 0)

    def run_instruction_0b10000001(self):
        # BR Rxx==Ryy $num
        self.branch_2_reg(lambda x, y: x == y)

    def run_instruction_0b10000010(self):
        # BR Rxx==#num2 $num1
        self.branch_1_reg_1_const(lambda x, y: x == y)

    def run_instruction_0b10000011(self):
        # BR Rxx!=Ryy $num
        self.branch_2_reg(lambda x, y: x != y)

    def run_instruction_0b10000100(self):
        # BR Rxx!=#num2 $num1
        self.branch_1_reg_1_const(lambda x, y: x != y)

    def run_instruction_0b10000101(self):
        # BR Rxx<Ryy $num
        self.branch_2_reg(lambda x, y: x < y)

    def run_instruction_0b10000110(self):
        # BR Rxx<#num2 $num1
        self.branch_1_reg_1_const(lambda x, y: x < y)

    def run_instruction_0b10000111(self):
        # BR Rxx>Ryy $num
        self.branch_2_reg(lambda x, y: x > y)

    def run_instruction_0b10001000(self):
        # BR Rxx>#num2 $num1
        self.branch_1_reg_1_const(lambda x, y: x > y)

    def run_instruction_0b10001001(self):
        # BRs Rxx<Ryy $num
        self.branch_2_reg(lambda x, y: parse_as_signed(x) < parse_as_signed(y))

    def run_instruction_0b10001010(self):
        # BRs Rxx<#num2 $num1
        self.branch_1_reg_1_const(lambda x, y: parse_as_signed(x) < parse_as_signed(y))

    def run_instruction_0b10001011(self):
        # BRs Rxx>Ryy $num
        self.branch_2_reg(lambda x, y: parse_as_signed(x) > parse_as_signed(y))

    def run_instruction_0b10001100(self):
        # BRs Rxx>#num2 $num1
        self.branch_1_reg_1_const(lambda x, y: parse_as_signed(x) > parse_as_signed(y))


class SimulationTimeoutException(Exception):
    pass


def simulate(program, max_instructions=10000):
    state = CpuState(program)
    instruction = 0
    while not state.halted:
        instruction += 1
        state.run_next_instruction()
        if instruction > max_instructions:
            raise SimulationTimeoutException(f"Timeout after {max_instructions} instructions")
    return state
