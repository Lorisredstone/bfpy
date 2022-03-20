# code original de https://github.com/paulkaefer/bftoc


from sys import argv
from datetime import datetime
# for the timestamp
# timestamp reference: http://docs.python.org/library/datetime.html

script, bf_file = argv

temp = argv[1].split(".bf")

c_file = open(f'{temp[0]}.c', 'w')

with open(bf_file, 'r') as raw_bf_file:
    raw_bf_string  = raw_bf_file.read()

bf_string = ""

commands = ",.+-[]><"

# The necessary size of the tape/array will be figured out
possize = 1
negsize = 1

for char in raw_bf_string:
    if char in commands:
        bf_string += char
        if char == "<":
            negsize += 1
        elif char == ">":
            possize += 1

size = max(possize, negsize)

size = 30000

# INITIAL LINES OF C FILE #

c_file.write(
    f"/* This is a translation of {bf_file}"
    + ", generated by bftoc.py (by Paul Kaefer)\n"
)

timestamp = (datetime.now()).strftime("%A, %B %d, %Y at %I:%M%p")
c_file.write(f" * It was generated on {timestamp}" + "\n")
c_file.write(" */\n\n")

c_file.write("#include <stdio.h>\n\n")

c_file.write("void main(void)\n")
c_file.write("{\n")

c_file.write(f"    int size = {repr(size)}" + ";\n")
c_file.write("    int tape[size];\n")
c_file.write("    int i = 0;\n\n")
c_file.write("    /* Clearing the tape (array) */\n")
c_file.write("    for (i=0; i<size; i++)\n")
c_file.write("        tape[i] = 0;\n\n")

c_file.write("    int ptr = 0;\n\n")


tabwidth = 4

def printspaces(number_of_spaces):
    string = "".join(" " for _ in range(number_of_spaces))
    c_file.write(string)

i_plus  = 0
i_minus = 0
i_next  = 0
i_prev  = 0

for char in bf_string:
    if (char == "+"):
        i_plus += 1
        if (i_prev != 0):
            printspaces(tabwidth)
            c_file.write(f"ptr -= {repr(i_prev)}" + ";\n")
            i_prev = 0
        if (i_next != 0):
            printspaces(tabwidth)
            c_file.write(f"ptr += {repr(i_next)}" + ";\n")
            i_next = 0
        if (i_minus != 0):
            printspaces(tabwidth)
            c_file.write(f"tape[ptr] -= {repr(i_minus)}" + ";\n")
            i_minus = 0
    elif char == "-":
        i_minus += 1
        if (i_prev != 0):
            printspaces(tabwidth)
            c_file.write(f"ptr -= {repr(i_prev)}" + ";\n")
            i_prev = 0
        if (i_next != 0):
            printspaces(tabwidth)
            c_file.write(f"ptr += {repr(i_next)}" + ";\n")
            i_next = 0
        if (i_plus != 0):
            printspaces(tabwidth)
            c_file.write(f"tape[ptr] += {repr(i_plus)}" + ";\n")
            i_plus = 0
    elif char == ">":
        i_next += 1
        if (i_prev != 0):
            printspaces(tabwidth)
            c_file.write(f"ptr -= {repr(i_prev)}" + ";\n")
            i_prev = 0
        if (i_plus != 0):
            printspaces(tabwidth)
            c_file.write(f"tape[ptr] += {repr(i_plus)}" + ";\n")
            i_plus = 0
        if (i_minus != 0):
            printspaces(tabwidth)
            c_file.write(f"tape[ptr] -= {repr(i_minus)}" + ";\n")
            i_minus = 0
    elif char == "<":
        i_prev += 1
        if (i_next != 0):
            printspaces(tabwidth)
            c_file.write(f"ptr += {repr(i_next)}" + ";\n")
            i_next = 0
        if (i_plus != 0):
            printspaces(tabwidth)
            c_file.write(f"tape[ptr] += {repr(i_plus)}" + ";\n")
            i_plus = 0
        if (i_minus != 0):
            printspaces(tabwidth)
            c_file.write(f"tape[ptr] -= {repr(i_minus)}" + ";\n")
            i_minus = 0
    elif char == ",":
        if (i_prev != 0):
            printspaces(tabwidth)
            c_file.write(f"ptr -= {repr(i_prev)}" + ";\n")
            i_prev = 0
        if (i_next != 0):
            printspaces(tabwidth)
            c_file.write(f"ptr += {repr(i_next)}" + ";\n")
            i_next = 0
        if (i_plus != 0):
            printspaces(tabwidth)
            c_file.write(f"tape[ptr] += {repr(i_plus)}" + ";\n")
            i_plus = 0
        if (i_minus != 0):
            printspaces(tabwidth)
            c_file.write(f"tape[ptr] -= {repr(i_minus)}" + ";\n")
            i_minus = 0
        printspaces(tabwidth)
        c_file.write("tape[ptr] = getchar();\n")
    elif char == ".":
        if (i_prev != 0):
            printspaces(tabwidth)
            c_file.write(f"ptr -= {repr(i_prev)}" + ";\n")
            i_prev = 0
        if (i_next != 0):
            printspaces(tabwidth)
            c_file.write(f"ptr += {repr(i_next)}" + ";\n")
            i_next = 0
        if (i_plus != 0):
            printspaces(tabwidth)
            c_file.write(f"tape[ptr] += {repr(i_plus)}" + ";\n")
            i_plus = 0
        if (i_minus != 0):
            printspaces(tabwidth)
            c_file.write(f"tape[ptr] -= {repr(i_minus)}" + ";\n")
            i_minus = 0
        printspaces(tabwidth)
        c_file.write("printf(\"%c\",tape[ptr]);\n")
    elif char == '[':
        if (i_prev != 0):
            printspaces(tabwidth)
            c_file.write(f"ptr -= {repr(i_prev)}" + ";\n")
            i_prev = 0
        if (i_next != 0):
            printspaces(tabwidth)
            c_file.write(f"ptr += {repr(i_next)}" + ";\n")
            i_next = 0
        if (i_plus != 0):
            printspaces(tabwidth)
            c_file.write(f"tape[ptr] += {repr(i_plus)}" + ";\n")
            i_plus = 0
        if (i_minus != 0):
            printspaces(tabwidth)
            c_file.write(f"tape[ptr] -= {repr(i_minus)}" + ";\n")
            i_minus = 0
        printspaces(tabwidth)
        c_file.write("while (tape[ptr] != 0)\n")
        printspaces(tabwidth)
        c_file.write("{\n")
        tabwidth += 4
    elif char == ']':
        if (i_prev != 0):
            printspaces(tabwidth)
            c_file.write(f"ptr -= {repr(i_prev)}" + ";\n")
            i_prev = 0
        if (i_next != 0):
            printspaces(tabwidth)
            c_file.write(f"ptr += {repr(i_next)}" + ";\n")
            i_next = 0
        if (i_plus != 0):
            printspaces(tabwidth)
            c_file.write(f"tape[ptr] += {repr(i_plus)}" + ";\n")
            i_plus = 0
        if (i_minus != 0):
            printspaces(tabwidth)
            c_file.write(f"tape[ptr] -= {repr(i_minus)}" + ";\n")
            i_minus = 0
        tabwidth -= 4
        printspaces(tabwidth)
        c_file.write("}\n")
    else:
        print(f"Unidentified character: {char}")

c_file.write("\n}\n\n")

c_file.close()


