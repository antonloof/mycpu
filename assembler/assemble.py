import argparse, pathlib

from assembler.assembler_state import *
from assembler.parse_common import *
from assembler.parse_directive import parse_directive
from assembler.parse_instruction import parse_instruction
from assembler.parse_label import parse_label
from typing import List


def strip_comments(line):
    return line.split(";")[0].strip()


def text_to_program(lines: List[str], state: AssemblerState):
    for lineno, line in enumerate(lines):
        no_comments = strip_comments(line)
        error = False
        if not no_comments:
            continue
        if no_comments[0] == ".":
            # directive
            directive = no_comments[1:]
            error = parse_directive(state, directive)
        elif no_comments[-1] == ":":
            # label
            label = no_comments[:-1]
            error = parse_label(state, label)
        else:
            # instruction
            error = parse_instruction(state, no_comments)
        if error:
            print("got error at line", lineno, ":", line)
            return True
    if state.undeclared_labels:
        print("Some labels were not declared:", *list(state.undeclared_labels.keys()))
    return False


def assemble(input_path: pathlib.Path, output_path: pathlib.Path):
    state = AssemblerState()
    with input_path.open() as f:
        lines = f.readlines()
    text_to_program(lines, state)
    with output_path.open("wb") as f:
        f.write(state.program_as_bytearry())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=pathlib.Path)
    parser.add_argument("-o", "--output", type=pathlib.Path)
    args = parser.parse_args()
    assemble(args.file, args.output)


if __name__ == "__main__":
    main()
