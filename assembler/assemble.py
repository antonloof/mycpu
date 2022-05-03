import argparse, pathlib
from typing import List


CONSTANT_ID = "#"
ADDRESS_ID = "$"


class AssemblerState:
    def __init__(self) -> None:
        self.program = [0] * (2**16)  # there is memory to waste on my pc :D
        self.sp = 0
        self.pc = 0
        self.origin = 0

    def word_directive(self, val):
        self.program[self.origin] = val
        self.origin += 1


def parse_word_directive(args: List[str], state: AssemblerState):
    if len(args) != 1:
        print("wrong number of arguments expected 1 got", args)
    error, val = parse_constant(args[0])
    if error:
        return True
    state.word_directive(val)
    return False


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


directives = {"word": parse_word_directive}


def strip_comments(line):
    return line.split(";")[0]


def parse_directive(state, directive):
    by_space = directive.split(" ")
    name = by_space[0]
    args = by_space[1:]
    return directives[name](args, state)


def assemble(input_path: pathlib.Path):
    state = AssemblerState()
    with input_path.open() as f:
        lines = f.readlines()

    for lineno, line in enumerate(lines):
        no_comments = strip_comments(line)
        error = False
        if no_comments[0] == ".":
            # directive
            directive = no_comments[1:]
            error = parse_directive(state, directive)
        elif no_comments[-1] == ":":
            # label
            pass
        else:
            # instruction
            pass
        if error:
            return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=pathlib.Path)
    args = parser.parse_args()
    assemble(args.file)


if __name__ == "__main__":
    main()
