import ply.lex as lex

tokens = [
    'ID', 'CTEF', 'CTEI', 'CTEC', 'CTESTRING', 'COMMA', 'COLON', 'SCOLON',
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET','LBRACE', 'RBRACE',
    'EQUALS', 'LT', 'LE', 'GT', 'GE', 'EQ', 'NE', 'OR', 'AND',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE'
]

keywords={
    'program': 'PROGRAM',
    'var': 'VAR',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'bool': 'BOOL',
    'true': 'TRUE',
    'false': 'FALSE',
    'function': 'FUNCTION',
    'main': 'MAIN',
    'void': 'VOID',
    'return': 'RETURN',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'print': 'PRINT',
    'println': 'PRINTLN',
    'read': 'READ',
    'mean': 'MEAN',
    'median': 'MEDIAN',
    'variance': 'VARIANCE',
    'std': 'STD',
    'rand': 'RAND',
    'plot': 'PLOT'
}

tokens += list(keywords.values())

t_ignore = ' \t'
t_COMMA = r','
t_COLON = r':'
t_SCOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='
t_EQUALS = r'='
t_OR = r'\|\|'
t_AND = r'&&'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_CTESTRING = r'\".*\"'
t_CTEC = r'\'(.{1})\''

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_ID(t):
    r'[A-Za-z]([A-Za-z]|[0-9])*'
    t.type = keywords.get(t.value, 'ID')
    return t

def t_CTEF(t):
    r'[0-9]+(\.[0-9]+)'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Error (Float Value):", t.value)
        t.value = 0
    return t

def t_CTEI(t):
    r'[0-9]+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Error (Int Value):", t.value)
        t.value = 0
    return t

def t_error(t):
    print("Invalid character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()