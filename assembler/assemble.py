import argparse, pathlib

from assembler_state import *
from parse_common import *
from parse_directive import parse_directive
from parse_instruction import parse_instruction


def validate_label(label: str):
    valid_label_chars = "abcdefghijklmnopqrstuvxyzABCDEFGHIJKLMNOPQRSTUVXYZ0123456789_"
    if set(label) - set(valid_label_chars):
        print("Invalid char in label:", label, "Valid chars are", valid_label_chars)
        return True, ""
    return False, label


def parse_label(state: AssemblerState, val: str):
    error, label = validate_label(val)
    if error:
        return True
    state.add_label(label)
    return False


def strip_comments(line):
    return line.split(";")[0].strip()


def assemble(input_path: pathlib.Path, output_path: pathlib.Path):
    state = AssemblerState()
    with input_path.open() as f:
        lines = f.readlines()

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

    print(state.program[0:10])
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
