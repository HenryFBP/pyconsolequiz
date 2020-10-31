from enum import Enum

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

class QuestionType(Enum):
    FREE_RESPONSE = 0
    MULTIPLE_CHOICE = 1
    MATCHING = 2
    UNKNOWN = 3


def reversedDict(d: dict) -> dict:
    return {v: k for k, v in d.items()}
def createObjectList(size=10, fillWith=False):
    l = []
    for i in range(size):
        l.append(fillWith)
    return l


def shuffledRange(*args, **kwargs):
    l = list(range(*args, **kwargs))
    random.shuffle(l)
    return l


def countMatchingElements(l1, l2) -> int:
    assert(len(l1) == len(l2))

    matches = 0
    for i in range(0, len(l1)):
        if(l1[i] == l2[i]):
            matches += 1

    return matches


assert(countMatchingElements([1, 2, 3], [1, 2, 4]) == 2)


def alphaToNumeric(c: str) -> int:
    """Given a character, return its numerical position. A=1, etc."""
    char = c[0].lower()
    return (ord(char) - ord('a')) + 1


assert(alphaToNumeric('a') == 1)
assert(alphaToNumeric('b') == 2)


def numericToAlpha(i: int) -> str:
    return chr(i + ord('a') - 1)


assert(numericToAlpha(1) == 'a')
assert(numericToAlpha(3) == 'c')
assert(alphaToNumeric(numericToAlpha(20)) == 20)
assert(numericToAlpha(alphaToNumeric('x')) == 'x')


def validateIntegerResponse(s: str) -> bool:
    """Return true if input looks like '1', '20', etc"""
    # string
    if(type(s) != str):
        return False

    #  string is numeric
    try:
        int(s)
    except ValueError:
        return False

    # int part must be less than 0 and not equal to 0
    if int(s) <= 0:
        return False

    return True


def validateMatchingResponse(s: str) -> bool:
    """Return true if input looks like 'A1', 'b2', etc"""

    # string
    if(type(s) != str):
        return False

    # not empty
    if(len(s) == 0):
        return False

    # 1st char is alphabetic
    if(s[0].upper() not in ALPHABET.upper()):
        return False

    # rest of string is numeric
    try:
        int(s[1:])
    except ValueError:
        return False

    # int part must be less than 0 and not equal to 0
    if int(s[1:]) <= 0:
        return False

    return True


assert(validateMatchingResponse('A2'))
assert not validateMatchingResponse('b0')
assert(validateMatchingResponse('x10'))


def parseMatchingResponse(s: str, offset=0) -> List[int]:
    """Given a matching response input (A3, B20, etc), return
    that response input as 2 ints in a tuple."""

    lhs, rhs = s[0], s[1:]

    ret = [alphaToNumeric(lhs), int(rhs)]

    ret[0] = ret[0]+offset
    ret[1] = ret[1]+offset

    return ret


assert(parseMatchingResponse('A3') == [1, 3])
assert(parseMatchingResponse('b4') == [2, 4])
assert(parseMatchingResponse('X20') == [24, 20])


def promptMatchingResponse(offset=0) -> Tuple[int]:
    """Get a matching response input from stdin."""
    while True:
        answer = input('[a-zA-Z][1-9]+ (ex. "b10")\n > ')

        if validateMatchingResponse(answer):
            return parseMatchingResponse(answer, offset)


def promptIntegerResponse(offset=0) -> Tuple[int]:
    """Get an integer response input from stdin."""
    while True:
        answer = input('[1-9]+ (ex. "20")\n > ')

        if validateIntegerResponse(answer):
            return int(answer)


def promptYN() -> bool:
    """Get y/n from a user."""
    while True:
        answer = input('[Yy]es/[Nn]o \n > ')

        if answer[0].capitalize() == 'Y':
            return True
        if answer[0].capitalize() == 'N':
            return False

