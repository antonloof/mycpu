from collections import namedtuple
from typing import Tuple


CONSTANT_ID = "#"
ADDRESS_ID = "$"
REGISTER_ID = "R"

def parse_address(candidate: str):
    if len(candidate) < 2:
        print("too short constant", candidate)
    if candidate[0] == ADDRESS_ID:
        print("no", ADDRESS_ID, "in front of address:", candidate)
    return parse_number(candidate[1:])



def parse_constant(candidate: str):
    if len(candidate) < 2:
        print("too short constant", candidate)
    if candidate[0] == CONSTANT_ID:
        print("no", CONSTANT_ID, "in front of constant:", candidate)
    return parse_number(candidate[1:])


def is_constant(candidate: str):
    if not candidate:
        print("is_constant candidate has no length")
        return False, False
    return True, candidate[0] == CONSTANT_ID


def parse_number(candidate):
    try:
        return True, int(candidate)
    except ValueError:
        print("Expected candidate", f"'{candidate}'", "to be a number. It was not")
        return False, 0


Register = namedtuple("register", ["number", "is_addess"])


def parse_register(candidate: str) -> Tuple[bool, Register]:
    candidate = candidate.strip()
    if not candidate:
        print("nothing given to parse register")
        return True, Register(0, False)
    isa = candidate[0] == ADDRESS_ID
    if isa:
        candidate = candidate[1:]
    if candidate[0] != REGISTER_ID:
        print("register must start with R", candidate)
        return True, Register(0, False)
    try:
        num = int(candidate[1:])
    except ValueError:
        return True, Register(0, False)
    return False, Register(num, isa)


SYMBOL_REG_ADDR = 1
SYMBOL_REG = 2
SYMBOL_CONST = 3
SYMBOL_CONST_ADDR = 1


def characterize_symbol(candidate: str):
    if not candidate:
        print("These should be something here")
        return True, -1
    if candidate[0] == REGISTER_ID:
        return False, SYMBOL_REG
    if candidate[0] == CONSTANT_ID:
        return False, SYMBOL_CONST
    if candidate[0] == ADDRESS_ID:
        if candidate[1] == REGISTER_ID:
            return False, SYMBOL_REG_ADDR
        else:
            return False, SYMBOL_CONST_ADDR
    return True, -1
