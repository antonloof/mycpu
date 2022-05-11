from assembler_state import AssemblerState
from typing import List


def parse_st(state: AssemblerState, args: List[str]):
    pass


def parse_add(state: AssemblerState, args: List[str]):
    pass


def parse_sub(state: AssemblerState, args: List[str]):
    pass


def parse_mul(state: AssemblerState, args: List[str]):
    pass


def parse_or(state: AssemblerState, args: List[str]):
    pass


def parse_xor(state: AssemblerState, args: List[str]):
    pass


def parse_inv(state: AssemblerState, args: List[str]):
    pass


def parse_shr(state: AssemblerState, args: List[str]):
    pass


def parse_shl(state: AssemblerState, args: List[str]):
    pass


def parse_mac(state: AssemblerState, args: List[str]):
    pass


def parse_jmp(state: AssemblerState, args: List[str]):
    pass


def parse_br(state: AssemblerState, args: List[str]):
    pass


def parse_brs(state: AssemblerState, args: List[str]):
    pass


def parse_psh(state: AssemblerState, args: List[str]):
    pass


def parse_nop(state: AssemblerState, args: List[str]):
    pass


def parse_hlt(state: AssemblerState, args: List[str]):
    pass


def parse_pop(state: AssemblerState, args: List[str]):
    pass


instructions = {
    "st": parse_st,
    "add": parse_add,
    "sub": parse_sub,
    "mul": parse_mul,
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
    instruction = by_space[0]
    args = by_space[1:]
    if instruction not in instructions:
        print("instruction", instruction, "not found")
        return True
    return instructions[instruction](state, args)
