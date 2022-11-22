import sys

data_type_IDs = {
    'int': 1, 
    'float': 2, 
    'char': 3, 
    'bool': 4, 
}

data_type_values = {
    1: 'int',
    2: 'float',
    3: 'char',
    4: 'bool',
}

operator_IDs = {
    '+': 1,
    '-': 2,
    '/': 3,
    '*': 4,
    '<': 5,
    '<=': 6,
    '>': 7,
    '>=': 8,
    '==': 9,
    '!=': 10,
    '&&': 11,
    '||': 12,
    '=': 13,
    
    'GOTO': 20,
    'GOTOV': 21,
    'GOTOF': 22,
    'GOSUB': 23,
    'ERA': 24,
    'VERIFY': 25,
    'PARAM': 26,
    'ENDFUNC': 27,
    'END': 28,

    'RETURN': 30,
    'PRINT': 31,
    'PRINT_MULTIPLE': 32,
    'READ': 33,
    'MEAN': 34,
    'MEDIAN': 35,
    'VARIANCE': 36,
    'STD': 37,
    'RAND': 38,
    'PLOT': 39,
}

def print_error(message, id=''):
    print(f'Error ID:{id}\n', f'Description: {message}', '\n')
    sys.exit()