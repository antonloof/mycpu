CONSTANT_ID = "#"
ADDRESS_ID = "$"


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
