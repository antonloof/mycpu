from assembler.assemble import text_to_program
import unittest

from assembler.assembler_state import AssemblerState


def to_int_4x8(a, b, c, d):
    return (a << 24) + (b << 16) + (c << 8) + d


def to_int_2x8_1x16(a, b, c):
    return (a << 24) + (b << 16) + c


class TestDirectives(unittest.TestCase):
    def test_origin_set_location_of_instruction(self):
        state = AssemblerState()
        text_to_program([".origin #100", "NOP", "NOP", "NOP"], state)
        self.assertEqual(state.program[100], to_int_4x8(0b11000010, 0, 0, 0))
        self.assertEqual(state.program[101], to_int_4x8(0b11000010, 0, 0, 0))
        self.assertEqual(state.program[102], to_int_4x8(0b11000010, 0, 0, 0))

    def test_word_sets_word(self):
        state = AssemblerState()
        text_to_program([".word #100"], state)
        self.assertEqual(state.program[0], 100)


class TestInstructions(unittest.TestCase):
    def help_test_one_instruction(self, instruction, *expected):
        state = AssemblerState()
        text_to_program([instruction], state)
        for i, e in enumerate(expected):
            self.assertEqual(state.program[i], e)

    def test_store_to_sp(self):
        self.help_test_one_instruction("ST SP #1000", to_int_4x8(0b00000011, 255, 0, 0), 1000)

    def test_st0(self):
        self.help_test_one_instruction("ST R11 R1", to_int_4x8(0b00000000, 11, 1, 0))

    def test_st1(self):
        self.help_test_one_instruction("ST R14 $23", to_int_2x8_1x16(0b00000001, 14, 23))

    def test_st2(self):
        self.help_test_one_instruction("ST $123 R10", to_int_2x8_1x16(0b00000010, 10, 123))

    def test_st3(self):
        self.help_test_one_instruction("ST R34 #10000", to_int_4x8(0b00000011, 34, 0, 0), 10000)

    def test_st4(self):
        self.help_test_one_instruction("ST $R45 R67", to_int_4x8(0b00000100, 45, 67, 0))

    def test_st5(self):
        self.help_test_one_instruction("ST R1 $R0", to_int_4x8(0b00000101, 1, 0, 0))

    def test_add0(self):
        self.help_test_one_instruction("ADD R10 R45", to_int_4x8(0b01000000, 10, 45, 0))

    def test_add1(self):
        self.help_test_one_instruction("ADD R10 #100", to_int_2x8_1x16(0b01000001, 10, 100))

    def test_sub0(self):
        self.help_test_one_instruction("SUB R10 R45", to_int_4x8(0b01000010, 10, 45, 0))

    def test_sub1(self):
        self.help_test_one_instruction("SUB R10 #100", to_int_2x8_1x16(0b01000011, 10, 100))

    def test_mul0(self):
        self.help_test_one_instruction("MUL R10 R45", to_int_4x8(0b01000100, 10, 45, 0))

    def test_mul1(self):
        self.help_test_one_instruction("MUL R10 #100", to_int_2x8_1x16(0b01000101, 10, 100))

    def test_and0(self):
        self.help_test_one_instruction("AND R10 R45", to_int_4x8(0b01000110, 10, 45, 0))

    def test_and1(self):
        self.help_test_one_instruction("AND R10 #100", to_int_2x8_1x16(0b01000111, 10, 100))

    def test_or0(self):
        self.help_test_one_instruction("OR R10 R45", to_int_4x8(0b01001000, 10, 45, 0))

    def test_or1(self):
        self.help_test_one_instruction("OR R10 #100", to_int_2x8_1x16(0b01001001, 10, 100))

    def test_xor0(self):
        self.help_test_one_instruction("XOR R10 R45", to_int_4x8(0b01001010, 10, 45, 0))

    def test_xor1(self):
        self.help_test_one_instruction("XOR R10 #100", to_int_2x8_1x16(0b01001011, 10, 100))

    def test_inv(self):
        self.help_test_one_instruction("INV R254", to_int_4x8(0b01001100, 254, 0, 0))

    def test_shr0(self):
        self.help_test_one_instruction("SHR R10 R45", to_int_4x8(0b01001101, 10, 45, 0))

    def test_shr1(self):
        self.help_test_one_instruction("SHR R10 #100", to_int_2x8_1x16(0b01001110, 10, 100))

    def test_shl0(self):
        self.help_test_one_instruction("SHL R10 R45", to_int_4x8(0b01001111, 10, 45, 0))

    def test_shl1(self):
        self.help_test_one_instruction("SHL R10 #100", to_int_2x8_1x16(0b01010000, 10, 100))

    def test_mac(self):
        self.help_test_one_instruction("MAC R12 R123 R213", to_int_4x8(0b01010001, 12, 123, 213))

    def test_jmp(self):
        self.help_test_one_instruction("JMP $2", to_int_4x8(0b10000000, 0, 0, 0), 2)

    def test_br_eq0(self):
        self.help_test_one_instruction("BR R34 == R23 $12341234", to_int_4x8(0b10000001, 34, 23, 0), 12341234)

    def test_br_eq1(self):
        self.help_test_one_instruction("BR R34 == #1234 $12341234", to_int_2x8_1x16(0b10000010, 34, 1234), 12341234)

    def test_br_neq0(self):
        self.help_test_one_instruction("BR R34 != R23 $12341234", to_int_4x8(0b10000011, 34, 23, 0), 12341234)

    def test_br_neq1(self):
        self.help_test_one_instruction("BR R34 != #1234 $12341234", to_int_2x8_1x16(0b10000100, 34, 1234), 12341234)

    def test_br_lt0(self):
        self.help_test_one_instruction("BR R34 < R23 $12341234", to_int_4x8(0b10000101, 34, 23, 0), 12341234)

    def test_br_lt1(self):
        self.help_test_one_instruction("BR R34 < #1234 $12341234", to_int_2x8_1x16(0b10000110, 34, 1234), 12341234)

    def test_br_gt0(self):
        self.help_test_one_instruction("BR R34 > R23 $12341234", to_int_4x8(0b10000111, 34, 23, 0), 12341234)

    def test_br_gt1(self):
        self.help_test_one_instruction("BR R34 > #1234 $12341234", to_int_2x8_1x16(0b10001000, 34, 1234), 12341234)

    def test_brs_lt0(self):
        self.help_test_one_instruction("BRs R34 < R23 $12341234", to_int_4x8(0b10001001, 34, 23, 0), 12341234)

    def test_brs_lt1(self):
        self.help_test_one_instruction("BRs R34 < #1234 $12341234", to_int_2x8_1x16(0b10001010, 34, 1234), 12341234)

    def test_brs_gt0(self):
        self.help_test_one_instruction("BRs R34 > R23 $12341234", to_int_4x8(0b10001011, 34, 23, 0), 12341234)

    def test_brs_gt1(self):
        self.help_test_one_instruction("BRs R34 > #1234 $12341234", to_int_2x8_1x16(0b10001100, 34, 1234), 12341234)

    def test_psh(self):
        self.help_test_one_instruction("PSH R1", to_int_4x8(0b11000000, 1, 0, 0))

    def test_pop(self):
        self.help_test_one_instruction("POP R1", to_int_4x8(0b11000001, 1, 0, 0))

    def test_nop(self):
        self.help_test_one_instruction("NOP", to_int_4x8(0b11000010, 0, 0, 0))

    def test_hlt(self):
        self.help_test_one_instruction("HLT", to_int_4x8(0b11000011, 0, 0, 0))


if __name__ == "__main__":
    unittest.main()
