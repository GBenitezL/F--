import sys
from lexer import lexer
from parser import parser


def main(argv):
    file = open(f"{argv[1]}", "r")
    program = file.read()
    print(parser.parse(program))

if __name__ == "__main__":
    main(sys.argv)