import sys
import ply.yacc as yacc
from lexer import tokens
from semantic_cube import Semantic_Cube
from directory import Scopes_Directory, Vars
from utils import data_type_IDs , print_error
from quadruples import Quadruple
from collections import deque

scopes = Scopes_Directory()
current_scope = ''

variables = deque()
variable_parameters = deque()

operators = deque()
operands = deque()
types = deque()
jumps = deque()
quadruples = [];
temps_count = 0

bool_arr = False
arr_size = 0


def p_program(p):
    '''program : PROGRAM ID SCOLON program_2
        | PROGRAM ID SCOLON vars program_2'''
    p[0] = 'Parsed Succesfully'

def p_program_2(p):
    '''program_2 : function program_2
        | main_block'''

def p_main_block(p):
    '''main_block : MAIN LPAREN RPAREN block
        | MAIN LPAREN RPAREN vars block'''

def p_block(p):
    '''block : LBRACE statements RBRACE
        | LBRACE RBRACE'''

def p_vars(p):
    '''vars : vars_2'''

def p_vars_2(p):
    '''vars_2 : VAR vars_3 vars_2
        | VAR vars_3'''

def p_vars_3(p):
    '''vars_3 : ID COLON type SCOLON
        |  ID COMMA vars_3'''

def p_type(p):
    '''type : INT array
        | FLOAT array
        | CHAR array
        | BOOL array'''

def p_array(p):
    '''array : LBRACKET CTEI RBRACKET
        | epsilon'''

def p_function(p):
    '''function : FUNCTION ID COLON return_type LPAREN params RPAREN block
        | FUNCTION ID COLON return_type LPAREN params RPAREN vars block
        | FUNCTION ID COLON return_type LPAREN RPAREN block
        | FUNCTION ID COLON return_type LPAREN RPAREN vars block'''

def p_return_type(p):
    '''return_type : VOID
        | type'''

def p_params(p):
    '''params : ID COLON type COMMA params
        | ID COLON type'''

def p_function_call(p):
    '''function_call_return : ID LPAREN RPAREN
        | ID LPAREN function_params RPAREN'''

def p_void_function_call(p):
    '''function_call_void : ID LPAREN RPAREN SCOLON
        | ID LPAREN function_params RPAREN SCOLON'''

def p_function_params(p):
    '''function_params : expression
        | expression COMMA function_params'''

def p_return(p):
    '''return : RETURN expression SCOLON'''

def p_statements(p):
    '''statements : assignment statements_2
        | condition statements_2
        | write statements_2
        | read statements_2
        | loop statements_2
        | return statements_2
        | function_call_void statements_2
        | plot statements_2'''

def p_statistics(p):
    '''statistics : mean
        | median
        | variance
        | standard_deviation
        | rand'''

def p_statements_2(p):
    '''statements_2 : statements
        | epsilon'''

def p_assignment(p):
    '''assignment : ID EQUALS expression SCOLON
        | ID LBRACKET expression RBRACKET EQUALS expression SCOLON'''

def p_condition(p):
    '''condition : IF LPAREN expression RPAREN block
        |  IF LPAREN expression RPAREN block ELSE block'''

def p_expression(p):
    '''expression : exp
        | comparison
        | logical
    '''

def p_comparison(p):
    '''comparison : exp LT exp
        | exp LE exp
        | exp GT exp
        | exp GE exp
        | exp EQ exp
        | exp NE exp'''

def p_logical(p):
    '''logical : expression AND expression
        | expression OR expression'''

def p_exp(p):
    '''exp : term
        | term exp_2'''

def p_exp_2(p):
    '''exp_2 : PLUS exp
        | MINUS exp'''

def p_term(p):
    '''term : factor
        | factor term_2'''

def p_term_2(p):
    '''term_2 : TIMES term
        | DIVIDE term'''

def p_factor(p):
    '''factor : LPAREN expression RPAREN
        | ID LBRACKET expression RBRACKET
        | function_call_return
        | factor_2
        | statistics'''

def p_factor_2(p):
    '''factor_2 : PLUS constant
        | MINUS constant
        | constant'''

def p_constant(p):
    '''constant : ID
        | CTEI
        | CTEF
        | CTEC
        | TRUE
        | FALSE'''

def p_loop(p):
    '''loop : for_loop
        | while_loop'''

def p_while_loop(p):
    '''while_loop : WHILE LPAREN expression RPAREN block'''

def p_for_loop(p):
    '''for_loop : FOR LPAREN ID EQUALS expression SCOLON expression SCOLON expression RPAREN block'''

def p_write(p):
    '''write : PRINT LPAREN write_2 RPAREN SCOLON'''

def p_write_2(p):
    '''write_2 : expression COMMA write_2
        | CTESTRING COMMA write_2
        | expression
        | CTESTRING'''

def p_read(p):
    '''read : READ LPAREN read_2 RPAREN SCOLON'''

def p_read_2(p):
    '''read_2 : ID
        | ID LBRACKET expression RBRACKET'''

def p_mean(p):
    '''mean : MEAN LPAREN ID RPAREN'''

def p_median(p):
    '''median : MEDIAN LPAREN ID RPAREN'''

def p_variance(p):
    '''variance : VARIANCE LPAREN ID RPAREN'''

def p_standard_deviation(p):
    '''standard_deviation : STD LPAREN ID RPAREN'''

def p_rand(p):
    '''rand : RAND LPAREN CTEI COMMA CTEI RPAREN'''

def p_plot(p):
    '''plot : PLOT LPAREN ID COMMA ID RPAREN SCOLON'''

def p_epsilon(p):
    '''epsilon : '''
    p[0] = None

def p_error(token):
    print(f"Syntax Error: {token.value!r}", token)
    token.lexer.skip(1)
    sys.exit()

parser = yacc.yacc()

def evaluate(p):
    print('Evaluate:', p)