# lig.py

from typing import Generator, List
from pprint import pprint as pp


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


def compileTokens(tokens: List[List[str]]):
    indent = 0
    for line in tokens:
        if line[0] == "compile":
            if line[1] == "raw":
                print(line[2].strip('"'))
        if line[0] == "def":
            if line[1] == "string":
                print(len(line), line)
                if len(line) == 3:
                    print("  " * indent + line[2] + "= ''")
                elif len(line) == 4:
                    print("  " * indent + line[2] + "=" + line[3])
                else:
                    exit("error in: " + " ".join(line))
            indent += 1


if __name__ == "__main__":
    # program = loadfile("stage1.lig")
    program = loadfile("example.lig")
    temp = removeComments(program)
    stage1 = removeNewlines(temp)
    stage2 = removeTabs(stage1)
    stage3 = tokenize(stage2)
    # compileTokens(stage3)
    pp(stage3)
