from ast import arg
from os import stat

from black import err
from assembler_state import AssemblerState
from typing import List
from parse_common import *


def parse_st(state: AssemblerState, args: List[str]):
    if len(args) != 2:
        print("Wrong number of arguments for ST:", args)
        return True

    e0, s0 = characterize_symbol(args[0])
    e1, s1 = characterize_symbol(args[1])
    if e0 or e1:
        return True
    error = True
    if s0 == SYMBOL_REG:
        error, r0 = parse_register(args[0])
        if error:
            return True
        if s1 == SYMBOL_REG:
            error, r1 = parse_register(args[1])
            state.insert_8_8_8_8(0b00000000, r0.number, r1.number, 0)
        if s1 == SYMBOL_CONST_ADDR:
            error, c1 = parse_address(args[1])
            state.insert_8_8_16(0b00000001, r0.number, c1)
        if s1 == SYMBOL_CONST:
            error, c1 = parse_constant(args[1])
            state.insert_8_8_8_8_32(0b00000011, r0.number, 0, 0, c1)
        if s1 == SYMBOL_REG_ADDR:
            error, r1 = parse_constant(args[1])
            state.insert_8_8_8_8(0b00000101, r0.number, r1.number, 0)
    if s0 == SYMBOL_CONST_ADDR:
        error, c0 = parse_address(args[0])
        if error:
            return True
        if s1 == SYMBOL_REG:
            error, r1 = parse_register(args[1])
            state.insert_8_8_16(0b00000010, r1.number, c0)
    if s0 == SYMBOL_REG_ADDR:
        error, r0 = parse_register(args[0])
        if error:
            return True
        if s1 == SYMBOL_REG:
            error, r1 = parse_register(args[1])
            state.insert_8_8_8_8(0b00000100, r0.number, r1.number, 0)
    return error


def parse_alu(state, args, accumelate_reg_opcode, accumelate_const_opcode, name):
    if len(args) != 2:
        print(f"Wrong number of arguments for {name}:", args)
        return True
    s0 = characterize_symbol(args[0])
    s1 = characterize_symbol(args[1])
    error = False
    if s0 == SYMBOL_REG:
        error, r0 = parse_register(args[0])
        if error:
            return True
        if s1 == SYMBOL_CONST:
            error, c1 = parse_constant(args[1])
            state.insert_8_8_16(accumelate_const_opcode, r0.number, c1)
        if s1 == SYMBOL_REG:
            error, r1 = parse_register(args[1])
            state.insert_8_8_8_8(accumelate_reg_opcode, r0.number, r1.number, 0)
    return error


def parse_add(state: AssemblerState, args: List[str]):
    return parse_alu(state, args, 0b01000000, 0b01000001, "ADD")


def parse_sub(state: AssemblerState, args: List[str]):
    return parse_alu(state, args, 0b01000010, 0b01000011, "SUB")


def parse_mul(state: AssemblerState, args: List[str]):
    return parse_alu(state, args, 0b01000100, 0b01000101, "MUL")


def parse_and(state: AssemblerState, args: List[str]):
    return parse_alu(state, args, 0b01000110, 0b01000111, "AND")


def parse_or(state: AssemblerState, args: List[str]):
    return parse_alu(state, args, 0b01001000, 0b01001001, "OR")


def parse_xor(state: AssemblerState, args: List[str]):
    return parse_alu(state, args, 0b01001010, 0b01001011, "XOR")


def parse_inv(state: AssemblerState, args: List[str]):
    if len(args) != 1:
        print(f"Wrong number of arguments for INV:", args)
        return True
    error, r0 = parse_register(args[0])
    if error:
        return True
    state.insert_8_8_8_8(0b01001100, r0.number, 0, 0)
    return error


def parse_shr(state: AssemblerState, args: List[str]):
    return parse_alu(state, args, 0b01001101, 0b01001110, "SHR")


def parse_shl(state: AssemblerState, args: List[str]):
    return parse_alu(state, args, 0b01001111, 0b01010000, "SHL")


def parse_mac(state: AssemblerState, args: List[str]):
    if len(args) != 3:
        print(f"Wrong number of arguments for MAC:", args)
        return True

    error0, r0 = parse_register(args[0])
    error1, r1 = parse_register(args[0])
    error2, r2 = parse_register(args[0])
    if error0 or error1 or error2:
        return True
    state.insert_8_8_8_8(0b01010001, r0.number, r1.number, r2.number)


def parse_jmp(state: AssemblerState, args: List[str]):
    if len(args) != 1:
        print(f"Wrong number of arguments for JMp:", args)
        return True
    error, c0 = parse_constant(args[0])
    if error:
        return True
    state.insert_8_8_8_8_16(0b10000000, 0, 0, 0, c0)


def parse_branching(state, args, mode_to_opcodes, name):
    if len(args) != 4:
        print(f"Wrong number of arguments for {name}:", args)
        return True
    if args[1] not in mode_to_opcodes:
        print("comparisson", args[1], "does not exist")
        return True
    error0, r0 = parse_register(args[0])
    error1, c0 = parse_constant(args[3])
    if error0 or error1:
        return True
    s1 = characterize_symbol(args[2])
    if s1 == SYMBOL_CONST:
        error, c1 = parse_constant(args[2])
        state.insert_8_8_16_16(mode_to_opcodes[args[1]], r0.number, c1, c0)
    if s1 == SYMBOL_REG:
        error, r1 = parse_register(args[2])
        state.insert_8_8_8_8_16(mode_to_opcodes[args[1]], r0.number, r1.number, 0, c0)
    return error


def parse_br(state: AssemblerState, args: List[str]):
    mode_to_opcodes = {
        "==": (0b10000001, 0b10000010),
        "!=": (0b10000011, 0b10000100),
        "<": (0b10000101, 0b10000110),
        ">": (0b10000111, 0b10001000),
    }
    return parse_branching(state, args, mode_to_opcodes, "BR")


def parse_brs(state: AssemblerState, args: List[str]):
    mode_to_opcodes = {
        "<": (0b10001001, 0b10001010),
        ">": (0b10001011, 0b10001100),
    }
    return parse_branching(state, args, mode_to_opcodes, "BRS")


def parse_psh(state: AssemblerState, args: List[str]):
    if len(args) != 1:
        print(f"Wrong number of arguments for PSH:", args)
        return True
    error, r0 = parse_register(args[0])
    if error:
        return True
    state.insert_8_8_8_8(0b11000000, r0.number, 0, 0)
    return error


def parse_nop(state: AssemblerState, args: List[str]):
    state.insert_8_8_8_8(0b10000010, 0, 0, 0)


def parse_hlt(state: AssemblerState, args: List[str]):
    state.insert_8_8_8_8(0b10000011, 0, 0, 0)


def parse_pop(state: AssemblerState, args: List[str]):
    if len(args) != 1:
        print(f"Wrong number of arguments for POP:", args)
        return True
    error, r0 = parse_register(args[0])
    if error:
        return True
    state.insert_8_8_8_8(0b11000001, r0.number, 0, 0)
    return error


instructions = {
    "st": parse_st,
    "add": parse_add,
    "sub": parse_sub,
    "mul": parse_mul,
    "and": parse_and,
    "or": parse_or,
    "xor": parse_xor,
    "inv": parse_inv,
    "shr": parse_shr,
    "shl": parse_shl,
    "mac": parse_mac,
    "jmp": parse_jmp,
    "br": parse_br,
    "brs": parse_brs,
    "psh": parse_psh,
    "pop": parse_pop,
    "hlt": parse_hlt,
    "nop": parse_nop,
}


def parse_instruction(state: AssemblerState, line: str):
    by_space = line.split(" ")
    instruction = by_space[0].lower()
    args = by_space[1:]
    for i in range(len(args)):
        if args[i] in state.labels:
            args[i] = f"${state.labels[args[i]]}"
    if instruction not in instructions:
        print("instruction", instruction, "not found")
        return True
    return instructions[instruction](state, args)
