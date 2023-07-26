keywords = [
    "print",
    "println",
    "Func",
    "endFunc",
    "Struct",
    "endStruct",
    "If",
    "Then",
    "Else",
    "endIf",
    "return",
    "input",
    "While",
    "Do",
    "endWhile",
    "new",
    "True",
    "False",
]

indent = [
    "Func",
    "Struct",
    "If",
    "While"
]
unindent=[
    "endFunc",
    "endStruct",
    "endIf",
    "endWhile"
]

# ops = ["+", "-", "*", "/", "^", "=", "->"]
ops = ["add","sub","mul","div", "pow","->"]

cpm = [">", "<", ">=", "<=", "==", "!="]

types = ["str", "int", "bol"]

lang = keywords + ops + cpm + types
