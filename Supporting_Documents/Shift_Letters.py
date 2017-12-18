import string

#allows for us to type with a shift 
def findShift(letter):
    if letter == "`":
        return "`"
    elif letter == "1":
        return "!"
    elif letter == "2":
        return "@"
    elif letter == "3":
        return "#"
    elif letter == "4":
        return "$"
    elif letter == "5":
        return "%"
    elif letter == "6":
        return "^"
    elif letter == "7":
        return "&"
    elif letter == "8":
        return "*"
    elif letter == "9":
        return "("
    elif letter == "0":
        return ")"
    elif letter == "-":
        return "_"
    elif letter == "=":
        return "+"
    elif letter == "[":
        return "{"
    elif letter == "]":
        return "}"
    elif letter == "\\":
        return "|"
    elif letter == ";":
        return ":"
    elif letter == "'":
        return "\""
    elif letter == ",":
        return "<"
    elif letter == ".":
        return ">"
    elif letter == "/":
        return "?"
    elif letter in string.ascii_lowercase:
        return letter.upper()
    