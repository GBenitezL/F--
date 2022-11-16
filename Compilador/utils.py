import sys

data_types = {
    'INTEGER': 'int',
    'FLOAT': 'float',
    'CHAR': 'char',
    'BOOLEAN': 'bool',
    'VOID': 'void',
}

data_type_IDs = {
    data_types['INTEGER']: 1, 
    data_types['FLOAT']: 2, 
    data_types['CHAR']: 3, 
    data_types['BOOLEAN']: 4, 
}

logical_operators = {
    'SUM': '+',
    'MINUS': '-',
    'DIVISION' : '/',
    'TIMES' : '*',
    'LESSTHAN' : '<',
    'LESSEQUALTHAN' : '<=',
    'GREATERTHAN' : '>',
    'GREATEREQUALTHAN' : '>=',
    'EQUAL' : '==',
    'DIFFERENT' : '!=',
    'AND' : '&&',
    'OR' : '||',
    'EQUALS' : '='
}

def print_error(message, id=''):
    print(f'\nError ID:{id}')
    print(f'Description:', message, '\n')
    sys.exit()