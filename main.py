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
    if len(argv) != 2:
        sys.exit("To run a program, type the following command structure: python main.py file_name.fmm")
    file = argv[1]

    if str(file)[-4:] != ".fmm":
        sys.exit("Only files with extension \".fmm\" can be executed")

    file = open(f"{argv[1]}", "r")
    print(parser.parse(file.read(), debug=False))
    
    # print_quadruples()
    # print_constants()
    # print_scopes()
    
    start_vm()
    
if __name__ == "__main__":
    main(sys.argv)
    
    
