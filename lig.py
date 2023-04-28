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
                        knownTokens.append(token)
            else:
                print(token)
                return False
    return True


def is_number(s: str) -> bool:
    if s.replace(".", "").isnumeric():
        return True
    else:
        return False


# this needs a lot of work POC
def compile(tokens: list[list[str]]) -> None:
    vars = {}
    lines = iter(tokens)
    for line in lines:
        words = iter(line)
        for word in words:
            if word == "println":
                nextToken = next(words)
                if nextToken.startswith('"'):
                    print(nextToken.strip('"'))
                elif is_number(nextToken):
                    print(nextToken)
                else:
                    if nextToken in vars.keys():
                        nextToken = vars[nextToken]
                        print(str(nextToken))
            elif word == "print":
                nextToken = next(words)
                if nextToken.startswith('"'):
                    print(nextToken.strip('"'), end="")
                elif is_number(nextToken):
                    print(nextToken, end="")
                else:
                    if nextToken in vars.keys():
                        nextToken = vars[nextToken]
                        print(str(nextToken), end="")
            elif word == "int":
                restofToken = list(words)
                if len(restofToken) == 1:
                    vars[restofToken[0]] = 0
                else:
                    if is_number(restofToken[0]):
                        if "." in restofToken[1]:
                            vars[restofToken[1]] = float(restofToken[0])
                        else:
                            vars[restofToken[1]] = int(restofToken[0])
                    else:
                        if restofToken[0] in vars.keys():
                            vars[restofToken[1]] = vars[restofToken[0]]
            elif word == "str":
                restofToken = list(words)
                if len(restofToken) == 1:
                    vars[restofToken[0]] = ""
                else:
                    vars[restofToken[1]] = restofToken[0].strip('"')
            elif word == "input":
                restofToken = list(words)
                if restofToken[1] not in vars:
                    exit(f"error {restofToken[1]} not defined") 
                if restofToken[0].startswith('"'):
                    vars[restofToken[1]] = input(restofToken[0])
                elif restofToken[0] in vars:
                    vars[restofToken[1]] = input(vars[restofToken[0]])

                    

    # pp(vars)


if __name__ == "__main__":
    # program = loadfile("stage1.lig")
    program = loadfile("test.lig")
    temp = removeComments(program)
    stage1 = removeNewlines(temp)
    stage2 = removeTabs(stage1)
    stage3 = tokenize(stage2)

    # pp(stage3)

    # tokens = flatten(stage3)
    # if not basicCheck(tokens):
    #     pp(stage3)

    compile(stage3)
