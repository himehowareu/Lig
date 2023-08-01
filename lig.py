# lig.py

# need to make the same state mechine 

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
    numbers = []
    strings=[]
    for token in tokens:
        if token.isnumeric():
            if token not in out:
                out.append(token)
        elif token.startswith('"'):
            if token not in out:
                out.append(token)
    return(numbers,strings)


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
    numbers , strings = extractConst(tokens)
    cont = numbers + strings

    knownTokens = language.lang + defined + cont

    for token in tokens:
        if token not in knownTokens:
            if "." in token:
                for part in token.split("."):
                    if part not in knownTokens:
                        print("BASIC CHECK: ",token)
                        return False
                    else:
                        knownTokens.append(token)
            else:
                print("BASIC CHECK: ",token)
                return False
    return True


def is_number(s: str) -> bool:
    if s.replace(".", "").isnumeric():
        return True
    else:
        return False


def printFlat(lines: List[List[str]])-> None:
    indent = 0
    for line in lines:
        if line[0] in language.indent:
            print("  "*indent," ".join(line))
            indent+=1
            continue
        elif line[0] in language.unindent:
            indent-=1
        if line[0] == "Else":
            print("  "*(indent-1)," ".join(line))
            continue
        print("  "*indent," ".join(line))


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

                    

def compile_test(tokens: list[list[str]])->None:
    vars={}
    lines = iter(tokens)
    for line in lines:
        match line:
            case ["print"|"println",statement] if statement.startswith('"'):
                ending =""
                if line[0] == "print":
                    ending ="\n"
                print(statement.strip('"'),end=ending)

            case ["print"|"println",statement] if is_number(statement):
                ending =""
                if line[0] == "print":
                    ending ="\n"
                print(statement,end=ending)

            case ["print"|"println",statement] if statement in vars.keys():
                ending =""
                if line[0] == "print":
                    ending ="\n"
                statement = vars[statement]
                print(str(statement),end=ending)
            
            case ["int" ,name,value] if is_number(value):
                    if "." in value:
                        print("can not asign float to int varible")
                        # vars[name] = float(value)
                    else:
                        vars[name] = int(value)
            case ["int" ,name,value] if name in vars.keys():
                    vars[name] = vars[value]
            case ["int" ,name]:
                    vars[name] = 0
            case ["str",name,value]:
                vars[name] = value.strip('"')
            case ["str",name]:
                vars[name] = ""
            case ["input",prompt,store] if prompt.startswith('"'):
                if store not in vars:
                    exit(f"error {store} not defined") 
                vars[store] = input(prompt.strip('"'))
            case ["input",prompt,store] if prompt in vars:
                if store not in vars:
                    exit(f"error {store} not defined") 
                vars[store] = input(vars[prompt])
            case _:
                print("unknown token : "+ " ".join(line))

    # pp(vars)


if __name__ == "__main__":
    # program = loadfile("example.lig")
    program = loadfile("test.lig")
    temp = removeComments(program)
    stage1 = removeNewlines(temp)
    stage2 = removeTabs(stage1)
    stage3 = tokenize(stage2)

    # pp(stage3)
    tokens = flatten(stage3)
    if not basicCheck(tokens):
        pp(stage3)
    
    # printFlat(stage3)

    # compile(stage3)
    compile_test(stage3)
