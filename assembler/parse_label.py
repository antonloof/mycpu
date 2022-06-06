from assembler.assembler_state import AssemblerState

valid_label_chars = "abcdefghijklmnopqrstuvxyzABCDEFGHIJKLMNOPQRSTUVXYZ0123456789_"


def is_label(candidate: str):
    return not bool(set(candidate) - set(valid_label_chars))


def validate_label(label: str):
    if not is_label(label):
        print("Invalid char in label:", label, "Valid chars are", valid_label_chars)
        return True, ""
    return False, label


def parse_label(state: AssemblerState, val: str):
    error, label = validate_label(val)
    if error:
        return True
    state.add_label(label)
    return False
