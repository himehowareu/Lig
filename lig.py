# lig.py

from typing import Generator, List
from pprint import pprint as pp
import language


def loadfile(filename: str) -> str:
    with open(filename, "r") as file:
        return file.read()


def removeNewlines(text: str) -> List[str]:
    out: List[str] = []
    for x in text.splitlines():
        if x.replace(" ", "") != "":
            out.append(x)
    return out


def removeComments(text: str) -> str:
    outLines = []
    for line in text.splitlines():
        out = ""
        maybeComment = False
        for char in line:
            if char == "/":
                if maybeComment:
                    outLines.append(out)
                    out = ""
                    break
                else:
                    maybeComment = True
            if maybeComment:
                if char != "/":
                    out += "/"
                    out += char
                    maybeComment = False
            else:
                maybeComment = False
                out += char
        if out != "":
            outLines.append(out)
    return "\n".join(outLines)


def removeTabs(text: List[str]) -> List[str]:
    out: List[str] = []
    for x in text:
        out.append(x.lstrip(" "))
    return out


def tokenize(lines: List[str]) -> List[List[str]]:
    out = []
    for line in lines:
        string = False
        tokens = []
        current = ""
        for char in list(line):
            if string:
                if char == '"':
                    tokens.append(f'"{current}"')
                    current = ""
                    string = False
                else:
                    current += char
            else:
                if char == '"':
                    string = True
                    if current != "":
                        tokens.append(current)
                    current = ""
                elif char == " ":
                    if current != "":
                        tokens.append(current)
                    current = ""
                else:
                    current += char
        if current != "":
            tokens.append(current)
        if tokens != []:
            out.append(tokens)
    return out


def extractConst(tokens: list[str]) -> list[str]:
    out = []
    for token in tokens:
        if token.isnumeric():
            if token not in out:
                out.append(token)
        elif token.startswith('"'):
            if token not in out:
                out.append(token)
    return out


def flatten(lines: List[List[str]]) -> list[str]:
    out = []
    for line in lines:
        out.extend(line)
    return out


# def gen(lines: list[list[str]]) -> Generator[str, None, None]:
#     for line in lines:
#         for token in line:
#             yield token


def getDefined(tokens: list[str]) -> tuple[list[str], list[str], list[str]]:
    functions: list[str] = []
    structs: list[str] = []
    vars: list[str] = []
    next = 0
    for token in tokens:
        if token == "Func":
            next = 1
            continue
        elif token in language.types:
            next = 2
            continue
        elif token == "Struct":
            next = 3
            continue
        elif token in structs:
            next = 2
            continue

        if next == 1:
            functions.append(token)
            next = 0
        elif next == 2:
            vars.append(token)
            next = 0
        elif next == 3:
            structs.append(token)
            next = 0
    return (functions, structs, vars)


def basicCheck(tokens: list[str]) -> bool:
    """this is some checking not yet done right"""
    fun, stru, vars = getDefined(tokens)
    defined = fun + stru + vars
    cont = extractConst(tokens)

    knownTokens = language.lang + defined + cont

    for token in tokens:
        if token not in knownTokens:
            if "." in token:
                for part in token.split("."):
                    if part not in knownTokens:
                        print(token)
                        return False
            else:
                print(token)
                return False
    return True


def compile(tokens: list[str]) -> None:
    pass  # exit("not yet working")


if __name__ == "__main__":
    # program = loadfile("stage1.lig")
    program = loadfile("example.lig")
    temp = removeComments(program)
    stage1 = removeNewlines(temp)
    stage2 = removeTabs(stage1)
    stage3 = tokenize(stage2)

    # pp(stage3)

    tokens = flatten(stage3)
    if basicCheck(tokens):
        pp(stage3)

    # compile(tokens)
