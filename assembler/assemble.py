import argparse, pathlib
import imp
from os import stat
from turtle import st
from typing import List

from black import err
from assembler_state import *
from parse_common import *
from parse_directive import parse_directive


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
    return line.split(";")[0].trim()


def assemble(input_path: pathlib.Path):
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
