import sys
import ply.yacc as yacc
from lexer import tokens
from semantic_cube import Semantic_Cube
from directory import Scopes_Directory, Vars
from utils import data_type_IDs, operator_IDs, print_error
from quadruples import Quadruple
from memory import Memory
from collections import deque

# Parser

def p_program(p):
    '''program : PROGRAM np_global_scope ID SCOLON program_2 np_end_program
        | PROGRAM ID np_global_scope SCOLON vars program_2 np_end_program'''
    p[0] = 'Parsed Succesfully'

def p_program_2(p):
    '''program_2 : function program_2
        | main_block'''
    p[0] = None

def p_main_block(p):
    '''main_block : MAIN np_main_scope LPAREN RPAREN block np_end_main
        | MAIN np_main_scope LPAREN RPAREN vars block np_end_main'''

def p_block(p):
    '''block : LBRACE statements RBRACE
        | LBRACE RBRACE'''

def p_vars(p):
    '''vars : vars_2'''
    p[0] = ('var', p[1])

def p_vars_2(p):
    '''vars_2 : VAR vars_3 vars_2
        | VAR vars_3'''

def p_vars_3(p):
    '''vars_3 : ID COLON type np_add_vars SCOLON
        |  ID np_append_vars COMMA vars_3'''

def p_type(p):
    '''type : INT array
        | FLOAT array
        | CHAR array
        | BOOL array'''
    p[0] = p[1]

def p_array(p):
    '''array : LBRACKET CTEI RBRACKET
        | epsilon'''

def p_function(p):
    '''function : FUNCTION ID COLON return_type np_new_scope LPAREN params RPAREN block
        | FUNCTION ID COLON return_type np_new_scope LPAREN params RPAREN vars block
        | FUNCTION ID COLON return_type np_new_scope LPAREN RPAREN block
        | FUNCTION ID COLON return_type np_new_scope LPAREN RPAREN vars block'''
    p[0] = None

def p_return_type(p):
    '''return_type : VOID
        | type'''
    p[0] = p[1]

def p_params(p):
    '''params : ID COLON type np_add_vars COMMA params
        | ID COLON type np_add_vars'''

def p_function_call_return(p):
    '''function_call_return : ID LPAREN RPAREN
        | ID LPAREN function_params RPAREN'''

def p_function_call_void(p):
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
    p[0] = (p[1], p[2])

def p_statistics(p):
    '''statistics : mean
        | median
        | variance
        | standard_deviation
        | rand'''

def p_statements_2(p):
    '''statements_2 : statements
        | epsilon'''
    p[0] = p[1]

def p_assignment(p):
    '''assignment : ID np_add_id EQUALS np_add_operator expression np_set_expression SCOLON
        | ID np_add_id LBRACKET expression RBRACKET EQUALS np_add_operator expression np_set_expression SCOLON'''

def p_condition(p):
    '''condition : IF LPAREN np_open_paren expression RPAREN block
        |  IF LPAREN expression RPAREN block ELSE block'''

def p_expression(p):
    '''expression : exp
        | comparison
        | logical
    '''
    p[0] = p[1]

def p_comparison(p):
    '''comparison : exp LT exp
        | exp LE exp
        | exp GT exp
        | exp GE exp
        | exp EQ exp
        | exp NE exp'''
    p[0] = (p[1], p[2], p[3])

def p_logical(p):
    '''logical : expression AND np_add_operator expression
        | expression OR np_add_operator expression'''

def p_exp(p):
    '''exp : term np_quad_plus_minus
        | term np_quad_plus_minus exp_2'''

def p_exp_2(p):
    '''exp_2 : PLUS np_add_operator exp
        | MINUS np_add_operator exp'''

def p_term(p):
    '''term : factor
        | factor term_2'''

def p_term_2(p):
    '''term_2 : TIMES term
        | DIVIDE term'''

def p_factor(p):
    '''factor : LPAREN np_open_paren expression RPAREN np_close_paren
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





# Variables

scopes = Scopes_Directory()
current_scope = ''

variables = deque()
operators = deque()
operands = deque()
types = deque()
jumps = deque()
quadruples = [];
temps_count = 0

is_array = False
arr_size = 0

# Functions

def evaluate(p):
    print('Evaluate:', p)

def create_scope(scope_id, return_type):
      # Create the global scope
    global scopes, current_scope
    scopes.add_new_scope(scope_id, return_type, Vars(scope_id))
    current_scope = scope_id

def create_quad(operator_to_check):
    global quadruples, operands, operators, types, scopes, current_scope, temps_count
    if len(operators) > 0 and (operators[-1] in operator_to_check):
        operator = operators.pop()
        right_oper = operands.pop()
        right_type = types.pop()
        left_oper = operands.pop()
        left_type = types.pop()
        res_type = Semantic_Cube.getType(operator, right_type, left_type)
        
        if res_type == 'Error':
            print_error(f'Invalid operation, type mismatch on {right_type} and {left_type} with a {operator}', 'C-16')
        current_scope_vars = scopes.get_vars_table(current_scope)
        temp_var_name = f"_temp{temps_count}"
        temps_count += 1
        current_scope_vars.add_var(temp_var_name, res_type)
        set_quad(operator, left_oper, right_oper, temp_var_name)
        operands.append(temp_var_name)
        types.append(res_type)

def set_quad(first, second, third, fourth):
    operator_id = operator_IDs[first]
    new_quadruple = Quadruple(operator_id, second, third, fourth)
    quadruples.append(new_quadruple)
    
def get_var(var_id):
    global scopes, current_scope
    scope_vars = scopes.get_vars_table(current_scope)
    directory_var = scope_vars.get_one(var_id)
    if (directory_var == 'not_in_directory'):
        program_vars = scopes.get_vars_table('program')
        directory_var = program_vars.get_one(var_id)
        print_error(f'Error: Variable {var_id} not found in current or global scope', '')

    return directory_var





# Neuralgic Points

def p_np_global_scope(p):
    '''np_global_scope : '''
    global scopes, current_scope, jumps
    create_scope('program', 'void')
    set_quad('GOTO', -1, -1, -1)
    jumps.append(len(quadruples) - 1)


def p_np_main_scope(p):
    '''np_main_scope : '''
    global jumps
    create_scope('main', 'void')
    main_quadruple_position = jumps.pop()
    old_main_goto_quadruple = quadruples[main_quadruple_position]
    old_main_goto_quadruple.set_result(len(quadruples))


def p_np_new_scope(p):
    '''np_new_scope : '''
    global scopes, current_scope
    function_id = p[-3]
    return_type = p[-1]
    create_scope(function_id, return_type)
    if return_type != 'void':
        global_scope_vars = scopes.get_vars_table('program')
        global_scope_vars.add_var(function_id, return_type)
        global_scope_vars.set_arrray_values(function_id, is_array, arr_size)


def p_np_append_vars (p):
    '''np_append_vars : '''
    global variables
    variables.append(p[-1])

def p_np_add_vars(p):
    '''np_add_vars : '''
    global scopes, current_scope, variables
    var_id = p[-3]
    variables.append(p[-3])
    vars_type = p[-1]

    while variables:
        current_scope_vars = scopes.get_vars_table(current_scope)
        current_scope_vars.add_var(variables[0], vars_type)
        variables.popleft()

def p_np_add_id(p):
    '''np_add_id : '''
    global operands, types
    # Get var instance from vars table
    current_var = get_var(p[-1])
    var_type = current_var['type']
    operands.append([-1])
    types.append(var_type)


def p_np_add_int(p):
    '''np_add_int : '''
    global operands, types
    operands.append(p[-1])
    types.append('int')


def p_np_add_float(p):
    '''np_add_float : '''
    global operands, types
    operands.append(p[-1])
    types.append('float')


def p_np_add_char(p):
    '''np_add_char : '''
    global operands, types
    operands.append(p[-1])
    types.append('char')


def p_np_add_bool(p):
    '''np_add_bool : '''
    global scopes, current_scope
    operands.append(p[-1])
    types.append('bool')
    

def p_np_add_operator(p):
    '''np_add_operator : '''
    global operators
    operators.append(p[-1])

def p_np_open_paren(p):
    '''np_open_paren : '''
    global operators
    operators.append(p[-1])

def p_np_close_paren(p):
    '''np_close_paren : '''
    global operators
    if operators[-1] != '(':
        print_error('Error: \'(\' not found in operators stack ', '')
    operators.pop()


def p_np_quad_plus_minus(p):
    '''np_quad_plus_minus : '''
    create_quad(['+', '-'])

def p_np_quad_times_div(p):
    '''np_quad_times_div : '''
    create_quad(['*', '/'])

def p_np_quad_comparison(p):
    '''np_quad_comparison : '''
    create_quad(['<', '<=', '>', '>=', '==', '!='])

def p_np_quad_logical(p):
    '''np_quad_logical : '''
    create_quad(['||', '&&'])

def p_np_set_expression(p):
    '''np_set_expression : '''
    global operators, operands, types
    operator = operators.pop()          # = 
    right_oper = operands.pop()
    right_type = types.pop()
    left_oper = operands.pop()
    left_type = types.pop()
    if Semantic_Cube.getType(operator, right_type, left_type) != 'Error':
        set_quad(operator, right_oper, -1, left_oper)
    else:
        print_error(f'Cannot perform operation {operator} to {left_type} and {right_type}', '')

def p_np_if_gotof(p):
    '''np_if_gotof : '''
    global operands, types, quadruples, jumps
    res_if_type = types.pop()
    if res_if_type == 'bool':
        set_quad('GOTOF', operands.pop(), -1, -1)
        jumps.append(len(quadruples) - 1)
    else:
        print_error(f'Conditional statement must be of type bool', '')

def p_np_if_end_gotof(p):
    '''np_if_end_gotof : '''
    global jumps, quadruples
    old_quadruple = quadruples[jumps.pop()]
    old_quadruple.set_result(len(quadruples))


def p_np_else_goto(p):
    '''np_else_goto : '''
    set_quad('GOTO', -1, -1, -1)
    old_quadruple = quadruples[jumps.pop()]
    jumps.append(len(quadruples) - 1)
    old_quadruple.set_result(len(quadruples))

def p_np_end_main(p):
    '''np_end_main : '''
    global scopes, current_scope
    scopes.set_size(current_scope)
    scopes.set_size('program')

def p_np_end_program(p):
    '''np_end_program : '''
    set_quad('END', -1, -1, -1)