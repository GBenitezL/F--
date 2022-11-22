import sys
from Compilador.parser import parser, scopes, quadruples, constants_table
from Compilador.vm import start_vm

def print_quadruples():
    print('Quadruples\n')
    for index, quad in enumerate(quadruples):
        print(index, end='') 
        quad.print()

def print_scopes():
    print('Scopes Directory\n')
    scopes.print_directory()

def print_constants():
    print('Constants Directory\n')
    for index, const in enumerate(constants_table):
        print(index, '\t\t', const, '\t\t', constants_table[const])

def main(argv):
    f = open(f"{argv[1]}", "r")
    print(parser.parse(f.read(), debug=False))
    
    # print_quadruples()
    # print_constants()
    # print_scopes()
    
    # Start intermediate code execution on virtual_machine
    start_vm()
    
if __name__ == "__main__":
    main(sys.argv)
    
    
