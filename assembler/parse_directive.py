from typing import List
from parse_common import *
from assembler_state import *


def parse_word_directive(args: List[str], state: AssemblerState):
    if len(args) != 1:
        print("wrong number of arguments expected 1 got", args)
        return True
    error, val = parse_constant(args[0])
    if error:
        return True
    state.word_directive(val)
    return False


def parse_origin_directive(args: List[str], state: AssemblerState):
    if len(args) != 1:
        print("wrong number of arguments expected 1 got", args)
        return True
    error, val = parse_constant(args[0])
    if error:
        return True
    state.origin_directive(val)
    return False


def parse_sp_directive(args: List[str], state: AssemblerState):
    if len(args) != 0:
        print("wrong number of arguments expected 0 got", args)
        return True
    state.sp_directive()
    return False


def parse_pc_directive(args: List[str], state: AssemblerState):
    if len(args) != 0:
        print("wrong number of arguments expected 0 got", args)
        return True
    state.pc_directive()
    return False


def parse_directive(state, directive):
    by_space = directive.split(" ")
    name = by_space[0].lower()
    args = by_space[1:]
    if name not in directives:
        print("directive", name, "not found")
        return True
    return directives[name](args, state)


directives = {
    "word": parse_word_directive,
    "origin": parse_origin_directive,
    "sp": parse_sp_directive,
    "pc": parse_pc_directive,
}
