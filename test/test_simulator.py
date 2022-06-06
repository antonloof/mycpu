from assembler.assemble import text_to_program, AssemblerState
from simulator.simulator import simulate

from typing import List
import unittest


class SimulatorTestBase(unittest.TestCase):
    def assemble_and_run(self, *lines: str):
        state = AssemblerState()
        error = text_to_program(lines, state)
        self.assertFalse(error, "error during assembly")
        return simulate(state.program, max_instructions=1000)


class TestSTInstructions(SimulatorTestBase):
    def test_st_to_reg(self):
        state = self.assemble_and_run("ST R0 #1", "ST R1 R0", "HLT")
        self.assertEqual(state.regs[1], 1)

    def test_st_to_mem(self):
        state = self.assemble_and_run("ST R0 #1", "ST $100 R0", "HLT")
        self.assertEqual(state.memory[100], 1)

    def test_st_from_mem(self):
        state = self.assemble_and_run("ST R0 #1", "ST $1000 R0", "ST R1 $1000", "HLT")
        self.assertEqual(state.regs[1], 1)

    def test_st_to_reg_from_const(self):
        state = self.assemble_and_run("ST R0 #1", "HLT")
        self.assertEqual(state.regs[0], 1)

    def test_st_to_mem_with_addr_from_reg(self):
        state = self.assemble_and_run("ST R0 #100", "ST R1 #10", "ST $R0 R1", "HLT")
        self.assertEqual(state.memory[100], 10)

    def test_st_from_mem_with_addr_from_reg(self):
        state = self.assemble_and_run("ST R0 #1", "ST $10 R0", "ST R1 #10", "ST R0 $R1", "HLT")
        self.assertEqual(state.regs[0], 1)

    def test_st_label_addr_to_reg(self):
        state = self.assemble_and_run("ST R0 var", "HLT", "var:")
        self.assertEqual(state.regs[0], 2)


class TestALUInstructions(SimulatorTestBase):
    def test_add_regs(self):
        state = self.assemble_and_run("ST R0 #1", "ST R1 #2", "ADD R0 R1", "HLT")
        self.assertEqual(state.regs[0], 3)

    def test_add_constant(self):
        state = self.assemble_and_run("ST R0 #1", "ADD R0 #2", "HLT")
        self.assertEqual(state.regs[0], 3)

    def test_add_overflow(self):
        state = self.assemble_and_run("ST R0 #0xFFFFFFFF", "ADD R0 #2", "HLT")
        self.assertEqual(state.regs[0], 1)

    def test_sub_regs(self):
        state = self.assemble_and_run("ST R0 #1", "ST R1 #2", "SUB R1 R0", "HLT")
        self.assertEqual(state.regs[1], 1)

    def test_sub_regs_overflow(self):
        state = self.assemble_and_run("ST R0 #1", "ST R1 #2", "SUB R0 R1", "HLT")
        self.assertEqual(state.regs[0], 2**32 - 1)

    def test_sub_constant(self):
        state = self.assemble_and_run("ST R0 #3", "SUB R0 #2", "HLT")
        self.assertEqual(state.regs[0], 1)

    def test_mul_regs(self):
        state = self.assemble_and_run("ST R0 #3", "ST R1 #2", "MUL R0 R1", "HLT")
        self.assertEqual(state.regs[0], 6)

    def test_mul_overflow(self):
        state = self.assemble_and_run("ST R0 #0x10000", "ST R1 #0x10000", "MUL R0 R1", "HLT")
        self.assertEqual(state.regs[0], 0)

    def test_mul_const(self):
        state = self.assemble_and_run("ST R0 #0x10000", "MUL R0 #0", "HLT")
        self.assertEqual(state.regs[0], 0)

    def test_and_regs(self):
        state = self.assemble_and_run("ST R0 #0xBA", "ST R1 #0xAB", "AND R0 R1", "HLT")
        self.assertEqual(state.regs[0], 0xAB & 0xBA)

    def test_and_const(self):
        state = self.assemble_and_run("ST R0 #0xDDC", "AND R0 #0xDEF", "HLT")
        self.assertEqual(state.regs[0], 0xDEF & 0xDDC)

    def test_or_regs(self):
        state = self.assemble_and_run("ST R0 #0xBA", "ST R1 #0xAB", "OR R0 R1", "HLT")
        self.assertEqual(state.regs[0], 0xAB | 0xBA)

    def test_or_const(self):
        state = self.assemble_and_run("ST R0 #0xDDC", "OR R0 #0xDEF", "HLT")
        self.assertEqual(state.regs[0], 0xDEF | 0xDDC)

    def test_xor_regs(self):
        state = self.assemble_and_run("ST R0 #0xBA", "ST R1 #0xAB", "XOR R0 R1", "HLT")
        self.assertEqual(state.regs[0], 0xAB ^ 0xBA)

    def test_xor_const(self):
        state = self.assemble_and_run("ST R0 #0xDDC", "XOR R0 #0xDEF", "HLT")
        self.assertEqual(state.regs[0], 0xDEF ^ 0xDDC)

    def test_inv(self):
        state = self.assemble_and_run("ST R0 #0xDDC", "INV R0", "HLT")
        self.assertEqual(state.regs[0], (~0xDDC) & 0xFFFFFFFF)

    def test_mac(self):
        state = self.assemble_and_run("ST R0 #10", "ST R1 #20", "ST R2 #30", "MAC R0 R1 R2", "HLT")
        self.assertEqual(state.regs[0], 10 + 20 * 30)


class TestBranch(SimulatorTestBase):
    def test_jmp(self):
        # failes with exception (too many instructions in simulation) if jmp does not work
        self.assemble_and_run("JMP $10999", ".origin #11000", "HLT")

    def test_br_eq_positive(self):
        state = self.assemble_and_run(
            "ST R0 #1", "ST R1 #1", "BR R0 == R1 here", "ST R2 #2", "HLT", "here:", "ST R2 #1", "HLT"
        )
        self.assertEqual(state.regs[2], 1)

    def test_br_eq_negative(self):
        state = self.assemble_and_run(
            "ST R0 #2", "ST R1 #1", "BR R0 == R1 here", "ST R2 #2", "HLT", "here:", "ST R2 #1", "HLT"
        )
        self.assertEqual(state.regs[2], 2)

    def test_br_neq_positive(self):
        state = self.assemble_and_run(
            "ST R0 #1", "ST R1 #2", "BR R0 != R1 here", "ST R2 #2", "HLT", "here:", "ST R2 #1", "HLT"
        )
        self.assertEqual(state.regs[2], 1)

    def test_br_neq_negative(self):
        state = self.assemble_and_run(
            "ST R0 #2", "ST R1 #2", "BR R0 != R1 here", "ST R2 #2", "HLT", "here:", "ST R2 #1", "HLT"
        )
        self.assertEqual(state.regs[2], 2)


class TestShortPrograms(SimulatorTestBase):
    def test_fib(self):
        state = self.assemble_and_run(
            "ST R0 #1",
            "ST R1 #1",
            "ST R2 #10",
            "loop:",
            "ADD R0 R1",
            "ADD R1 R0",
            "SUB R2 #1",
            "BR R2 != #0 loop",
            "HLT",
        )
        # 21th and 22th fibnumber
        self.assertEqual(state.regs[0], 10946)
        self.assertEqual(state.regs[1], 17711)
