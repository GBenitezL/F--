import sys

data_type_IDs = {
    'int': 1, 
    'float': 2, 
    'char': 3, 
    'bool': 4, 
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
    'READ': 32,
    'MEAN': 33,
    'MEDIAN': 34,
    'VARIANCE': 35,
    'STD': 36,
    'RAND': 37,
    'PLOT': 38,
}

def print_error(message, id=''):
    print(f'Error ID:{id}\n', f'Description: {message}', '\n')
    sys.exit()