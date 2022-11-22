import sys
import ply.yacc as yacc
from Compilador.lexer import tokens
from Compilador.semantic_cube import Semantic_Cube
from Compilador.directory import Scopes_Directory, Vars
from Compilador.utils import data_type_IDs, operator_IDs, print_error
from Compilador.quadruples import Quadruple
from Compilador.memory import Memory
from collections import deque

##### Parser #####

def p_program(p):
    '''program : PROGRAM ID np_global_scope SCOLON program_2 np_end_program
        | PROGRAM ID np_global_scope SCOLON vars program_2 np_end_program'''
    p[0] = 'Parsed Succesfully'

def p_program_2(p):
    '''program_2 : main_block
        | function program_2'''
    p[0] = None

def p_main_block(p):
    '''main_block : MAIN np_main_scope LPAREN RPAREN vars block np_end_main
        | MAIN np_main_scope LPAREN RPAREN block np_end_main'''

def p_block(p):
    '''block : LBRACE statements RBRACE
        | LBRACE RBRACE'''

def p_vars(p):
    '''vars : vars_2'''
    p[0] = ('var', p[1])

def p_vars_2(p):
    '''vars_2 : VAR vars_3 
        | VAR vars_3 vars_2'''

def p_vars_3(p):
    '''vars_3 : ID np_append_vars COMMA vars_3
        | ID COLON type np_add_vars SCOLON'''

def p_type(p):
    '''type : INT array
        | CHAR array
        | FLOAT array
        | BOOL array'''
    p[0] = p[1]

def p_array(p):
    '''array : LBRACKET CTEI RBRACKET
        | epsilon'''
    global operands, types, mem_count, is_array, arr_size
    if (p[1] != '['):
        is_array = False
        arr_size = None
    else:
        is_array = True
        arr_size = p[2]
        
        if arr_size >= 1:
            create_cteint_address(arr_size)
        else:
            print_error(f'Array size should be greater than 1', '')

def p_function(p):
    '''function : FUNCTION ID COLON return_type np_new_scope LPAREN RPAREN np_func_start block np_func_end
        | FUNCTION ID COLON return_type np_new_scope LPAREN parameters RPAREN np_func_start block np_func_end
        | FUNCTION ID COLON return_type np_new_scope LPAREN RPAREN vars np_func_start block np_func_end
        | FUNCTION ID COLON return_type np_new_scope LPAREN parameters RPAREN vars np_func_start block np_func_end'''
    p[0] = None

def p_return_type(p):
    '''return_type : type
        | VOID'''
    p[0] = p[1]

def p_parameters(p):
    '''parameters : ID COLON type np_add_vars np_add_params_type
        | ID COLON type np_add_vars np_add_params_type COMMA parameters'''

def p_function_call_return(p):
    '''function_call_return : ID LPAREN np_check_func_call np_func_end_params RPAREN
        | ID LPAREN np_check_func_call function_parameters np_func_end_params RPAREN'''

def p_function_call_void(p):
    '''function_call_void :  ID LPAREN np_check_func_call np_func_end_params RPAREN SCOLON
        | ID LPAREN np_check_func_call function_parameters np_func_end_params RPAREN SCOLON'''

def p_function_parameters(p):
    '''function_parameters : expression np_add_func_call_param
        | expression np_add_func_call_param COMMA function_parameters'''

def p_return(p):
    '''return : RETURN expression np_set_return_quad SCOLON'''

def p_statements(p):
    '''statements : return statements_2
        | assignment statements_2
        | condition statements_2
        | loop statements_2
        | read statements_2
        | write statements_2
        | plot statements_2
        | function_call_void statements_2'''
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
        | ID np_add_id LBRACKET np_check_is_array expression np_verify_array_dim RBRACKET np_get_array_address EQUALS np_add_operator expression np_set_expression SCOLON'''

def p_condition(p):
    '''condition : IF LPAREN expression RPAREN np_if_gotof block ELSE np_else_goto block np_if_end_gotof
        | IF LPAREN expression RPAREN np_if_gotof block np_if_end_gotof'''

def p_expression(p):
    '''expression : exp
        | logical np_quad_logical
        | comparison np_quad_comparison
    '''
    p[0] = p[1]

def p_comparison(p):
    '''comparison : exp EQ np_add_operator exp
        | exp NE np_add_operator exp
        | exp LT np_add_operator exp
        | exp GT np_add_operator exp
        | exp LE np_add_operator exp
        | exp GE np_add_operator exp'''
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
    '''term : factor np_quad_times_div
        | factor np_quad_times_div term_2'''

def p_term_2(p):
    '''term_2 : TIMES np_add_operator term
        | DIVIDE np_add_operator term'''

def p_factor(p):
    '''factor : LPAREN np_open_paren expression RPAREN np_close_paren 
        | ID np_add_id LBRACKET np_check_is_array expression np_verify_array_dim RBRACKET np_get_array_address
        | factor_2
        | function_call_return
        | statistics'''

def p_factor_2(p):
    '''factor_2 : PLUS constant
        | MINUS np_set_as_negative constant
        | constant'''

def p_constant(p):
    '''constant : ID np_add_id
        | CTEI np_add_int
        | CTEF np_add_float
        | CTEC np_add_char
        | TRUE np_add_bool
        | FALSE np_add_bool'''
    p[0] = p[1]

def p_loop(p):
    '''loop : for_loop
        | while_loop'''

def p_while_loop(p):
    '''while_loop : WHILE np_while_start LPAREN expression RPAREN np_while_expression block np_while_end'''

def p_for_loop(p):
    '''for_loop : FOR LPAREN ID np_add_id EQUALS np_add_operator expression np_for_expression SCOLON expression np_for_limit SCOLON expression RPAREN block np_for_end'''

def p_write(p):
    '''write : PRINT LPAREN write_2 RPAREN SCOLON'''

def p_write_2(p):
    '''write_2 : expression np_set_print_quad_exp COMMA write_2_multiple
        | expression np_set_print_quad_exp
        | CTESTRING  np_set_print_quad_str COMMA write_2_multiple
        | CTESTRING np_set_print_quad_str'''

def p_write_2_multiple(p):
    '''write_2_multiple : expression np_set_print_same_line_quad_exp COMMA write_2_multiple
        | expression np_set_print_same_line_quad_exp
        | CTESTRING  np_set_print_same_line_quad_str COMMA write_2_multiple
        | CTESTRING np_set_print_same_line_quad_str'''

def p_read(p):
    '''read : READ LPAREN read_2 RPAREN np_set_read_quad SCOLON'''

def p_read_2(p):
    '''read_2 : ID np_add_id LBRACKET np_check_is_array expression np_verify_array_dim RBRACKET np_get_array_address
        | ID np_add_id'''

def p_mean(p):
    '''mean : MEAN LPAREN ID RPAREN np_set_mean_quad'''

def p_median(p):
    '''median : MEDIAN LPAREN ID RPAREN np_set_median_quad'''

def p_variance(p):
    '''variance : VARIANCE LPAREN ID RPAREN np_set_variance_quad'''

def p_standard_deviation(p):
    '''standard_deviation : STD LPAREN ID RPAREN np_set_std_quad'''

def p_rand(p):
    '''rand : RAND LPAREN CTEI COMMA CTEI RPAREN np_set_rand_quad'''

def p_plot(p):
    '''plot : PLOT LPAREN ID COMMA ID RPAREN np_set_plot_quad SCOLON'''

def p_epsilon(p):
    '''epsilon : '''
    p[0] = None

def p_error(token):
    print(f"Syntax Error: {token.value!r}", token)
    token.lexer.skip(1)
    sys.exit()


##### Variables #####

scopes = Scopes_Directory()
current_scope = ''

variables = deque()
operators = deque()
operands = deque()
types = deque()
jumps = deque()
quadruples = [];

params_count = 0
params_stack = deque()
func_call_IDs = deque()
current_func_call_ID = None

is_array = False
arr_size = 0

constants_table = {}
mem_count = Memory()
temps_count = 0


###### Utility Functions #####

def evaluate(p):
    print('Evaluate:', p)

def create_scope(scope_ID, return_type):
    global scopes, current_scope
    scopes.add_new_scope(scope_ID, return_type, Vars(scope_ID))
    current_scope = scope_ID

def create_quad(operator_to_check):
    global operands, operators, types, scopes, current_scope, temps_count
    if len(operators) > 0 and (operators[-1] in operator_to_check):
        operator = operators.pop()
        right_oper = operands.pop()
        right_type = types.pop()
        left_oper = operands.pop()
        left_type = types.pop()
        res_type = Semantic_Cube.getType(operator, right_type, left_type)
        
        if res_type != 'Error':  
            current_scope_vars = scopes.get_vars_table(current_scope)
            temp_var_name = "_temp" + f"{temps_count}"
            temps_count += 1
            current_scope_vars.add_var(temp_var_name, res_type)
            new_address = get_vars_new_address(res_type, True)
            current_scope_vars.set_var_address(temp_var_name, new_address)
            set_quad(operator, left_oper, right_oper, new_address)
            operands.append(new_address)
            types.append(res_type)
        else:
            print_error(f'Cannot perform operation {operator} to {left_type} and {right_type}', '')

def set_quad(oper_ID, left_oper, right_oper, result):
    quadruples.append(Quadruple(operator_IDs[oper_ID] , left_oper, right_oper, result))

def create_cteint_address(value):
    global mem_count, constants_table
    if value in constants_table:
        return constants_table[value]
    else:
        new_mem_address = mem_count.count_const_int
        constants_table[value] = new_mem_address
        mem_count.set_count('const', 'int')
        return new_mem_address

def create_new_pointer_address():
    global mem_count
    new_pointer_address = mem_count.count_pointers
    mem_count.set_count('pointer', None)
    return new_pointer_address
    
   
def get_vars_new_address(var_type, is_temp = False, space = 1, other_scope = None):
    global current_scope
    global mem_count
    if other_scope is not None:
        scope = other_scope
    else:
        scope = current_scope
    if is_temp:
        mem_count.set_count('temp', var_type, space)
        return get_temporal_types_map(mem_count)[var_type]
    if(scope == 'program'):
        global_types_map = get_global_types_map(mem_count)
        mem_count.set_count('global', var_type, space)
        return global_types_map[var_type]
    local_types_map = get_local_types_map(mem_count)
    mem_count.set_count('local', var_type, space)
    return local_types_map[var_type]


def get_var_directory(var_ID):
    global scopes
    global current_scope
    directory_var = scopes.get_vars_table(current_scope).get_one(var_ID)
    if (directory_var == None):
        directory_var = scopes.get_vars_table('program').get_one(var_ID)
        if (directory_var == None):
            print_error(f'Variable {var_ID} not found in current or global scope', '')
    return directory_var


def create_quad_statistics(arr_ID, quadruple_str):
    current_var = get_var_directory(arr_ID)
    if (current_var['is_array']) or (current_var['type'] in ['int', 'float']):    
        result_address = create_temp_address('float')
        operands.append(result_address)
        types.append('float')
        set_quad(quadruple_str, current_var['arr_size'], current_var['address'], result_address)
    else:
        print_error('The {quadruple_str} function only accepts an array of floats or integers.', '')

def create_temp_address(type):
    global scopes, temps_count, current_scope
    current_scope_vars = scopes.get_vars_table(current_scope)
    temp_var_name = f"_temp{temps_count}"
    temps_count += 1
    current_scope_vars.add_var(temp_var_name, 'float')
    new_address = get_vars_new_address(type, True)
    current_scope_vars.set_var_address(temp_var_name, new_address)
    return new_address

def get_global_types_map(mem_count):
    global_types_map = {
        'int': mem_count.count_global_int,
        'float': mem_count.count_global_float,
        'char': mem_count.count_global_char,
        'bool': mem_count.count_global_bool,
    }
    return global_types_map


def get_local_types_map(mem_count):
    local_types_map = {
        'int': mem_count.count_local_int,
        'float': mem_count.count_local_float,
        'char': mem_count.count_local_char,
        'bool': mem_count.count_local_bool,
    }
    return local_types_map

def get_temporal_types_map(mem_count):
    local_types_map = {
        'int': mem_count.count_temp_int,
        'float': mem_count.count_temp_float,
        'char': mem_count.count_temp_char,
        'bool': mem_count.count_temp_bool,
    }
    return local_types_map



##### Neuralgic Points #####

##### Linear Statements #####

def p_np_global_scope(p):
    '''np_global_scope : '''
    global jumps
    create_scope('program', 'void')
    set_quad('GOTO', -1, -1, -1)
    jumps.append(len(quadruples) - 1)
    create_cteint_address(0)

def p_np_main_scope(p):
    '''np_main_scope : '''
    global jumps
    create_scope('main', 'void')
    quadruples[jumps.pop()].set_result(len(quadruples))

def p_np_new_scope(p):
    '''np_new_scope : '''
    global scopes
    func_ID = p[-3]
    return_type = p[-1]
    create_scope(func_ID, return_type)
    if return_type != 'void':
        global_scope_vars = scopes.get_vars_table('program')
        global_scope_vars.add_var(func_ID, return_type)
        global_scope_vars.set_var_address(func_ID, get_vars_new_address(return_type, False, 1, 'program'))
        global_scope_vars.set_arrray_values(func_ID, is_array, arr_size)


def p_np_append_vars (p):
    '''np_append_vars : '''
    global variables
    var_ID = p[-1]
    variables.append(var_ID)

def p_np_add_vars(p):
    '''np_add_vars : '''
    global scopes, current_scope, is_array, arr_size, variables

    variables.append(p[-3])
    vars_type = p[-1]
    memory_space = 1 if arr_size is None else arr_size
    while variables:
        current_scope_vars = scopes.get_vars_table(current_scope)
        current_scope_vars.add_var(variables[0], vars_type)
        current_scope_vars.set_var_address(variables[0], get_vars_new_address(vars_type, False, memory_space))
        current_scope_vars.set_arrray_values(variables[0], is_array, arr_size)
        variables.popleft()

def p_np_add_id(p):
    '''np_add_id : '''
    global operands, types
    var_ID = p[-1]
    current_var = get_var_directory(var_ID)
    operands.append(current_var['address'])
    types.append(current_var['type'])

def p_np_add_int(p):
    '''np_add_int : '''
    global operands, types, mem_count, constants_table
    if p[-1] not in constants_table:    
        constants_table[p[-1]] = mem_count.count_const_int
        mem_count.set_count('const', 'int')
    operands.append(constants_table[p[-1]])
    types.append('int')

def p_np_add_float(p):
    '''np_add_float : '''
    global operands, types, mem_count, constants_table
    if p[-1] not in constants_table:    
        constants_table[p[-1]] = mem_count.count_const_float
        mem_count.set_count('const', 'float')
    operands.append(constants_table[p[-1]])
    types.append('float')

def p_np_add_char(p):
    '''np_add_char : '''
    global operands, types, mem_count, constants_table
    if p[-1] not in constants_table:    
        constants_table[p[-1]] = mem_count.count_const_char
        mem_count.set_count('const', 'char')
    operands.append(constants_table[p[-1]])
    types.append('char')

def p_np_add_bool(p):
    '''np_add_bool : '''
    global scopes, current_scope, mem_count, constants_table, operands, types
    if p[-1] not in constants_table:    
        constants_table[p[-1]] = mem_count.count_const_bool
        mem_count.set_count('const', 'bool')
    operands.append(constants_table[p[-1]])
    types.append('bool')
    
def p_np_set_as_negative(p):
    '''np_set_as_negative : '''
    global mem_count, constants_table, operands, types, operators
    if -1 not in constants_table:    
        constants_table[-1] = mem_count.count_const_int
        mem_count.set_count('const', 'int')
    operands.append(constants_table[-1])
    types.append('int')
    operators.append('*')

def p_np_add_operator(p):
    '''np_add_operator : '''
    global operators
    oper = p[-1]
    operators.append(oper)

def p_np_open_paren(p):
    '''np_open_paren : '''
    global operators
    paren = p[-1]
    operators.append(paren)

def p_np_close_paren(p):
    '''np_close_paren : '''
    global operators
    if operators[-1] == '(':
        operators.pop()
    else:
        print_error('Cannot find opening parenthesis', '')
    
def p_np_quad_plus_minus(p):
    '''np_quad_plus_minus : '''
    oper_list = ['+', '-']
    create_quad(oper_list)

def p_np_quad_times_div(p):
    '''np_quad_times_div : '''
    oper_list = ['*', '/']
    create_quad(oper_list)

def p_np_quad_comparison(p):
    '''np_quad_comparison : '''
    oper_list = ['<', '<=', '>', '>=', '==', '!=']
    create_quad(oper_list)

def p_np_quad_logical(p):
    '''np_quad_logical : '''
    oper_list = ['||', '&&']
    create_quad(oper_list)

def p_np_set_expression(p):
    '''np_set_expression : '''
    global operators, operands, types
    operator = operators.pop()
    right_oper = operands.pop()
    right_type = types.pop()
    left_oper = operands.pop()
    left_type = types.pop()
    if Semantic_Cube.getType(operator, right_type, left_type) != 'Error':
        set_quad(operator, right_oper, -1, left_oper)
    else:
        print_error(f'Cannot perform operation {operator} to {left_type} and {right_type}', '')


# Non-Linear Statements

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
    old_quad = quadruples[jumps.pop()]
    old_quad.set_result(len(quadruples))


def p_np_else_goto(p):
    '''np_else_goto : '''
    set_quad('GOTO', -1, -1, -1)
    old_quad = quadruples[jumps.pop()]
    jumps.append(len(quadruples) - 1)
    old_quad.set_result(len(quadruples))

def p_np_for_expression(p):
    '''np_for_expression : '''
    global operators, operands, types, quadruples, jumps
    operator = operators.pop()
    right_oper = operands.pop()
    right_type = types.pop()
    left_oper = operands.pop()
    left_type = types.pop()
    if right_type == 'int' and left_type == 'int' :
        set_quad(operator, right_oper, -1, left_oper)
        jumps.append(len(quadruples))
        operands.append(left_oper)
        types.append('int')
    else:
        print_error(f'"For" loop requires limits of type int', '')

def p_np_for_limit(p):
    ''' np_for_limit : '''
    global operands, types, quadruples, jumps
    result = operands.pop()
    op_type = types.pop()

    if op_type == 'bool':
        set_quad('GOTOV', result, -1, -1)
        jumps.append(len(quadruples) - 1)
    else:
        print_error(f'"For" loop requires condition of type bool', '')

def p_np_for_end(p):
    '''np_for_end : '''
    global operands, types, quadruples
    for_length = operands.pop()
    if types.pop() == 'int':
        for_value = operands.pop()
        for_var_type = types.pop()
    else:
        print_error('Value for "For" loop update variable should be int', '')
    
    if Semantic_Cube.getType('+', for_var_type, 'int') == 'int':
        set_quad('+', for_value, for_length, for_value)
        end_pos = jumps.pop()
        set_quad('GOTO', -1, -1, jumps.pop())
        quadruples[end_pos].set_result(len(quadruples))
    else:
        print_error(f'Type mismatch: Cannot perform operation + on {for_var_type} and int', '')


def p_np_while_start (p):
    '''np_while_start : '''
    jumps.append(len(quadruples))

def p_np_while_expression (p):
    '''np_while_expression : '''
    exp_type = types.pop()
    if exp_type == 'bool': 
        set_quad('GOTOF', operands.pop(), -1, -1)
        jumps.append(len(quadruples) - 1)
    else:
        print_error(f'Conditional statement must be of type bool', '')

def p_np_while_end (p):
    '''np_while_end : '''
    end_pos = jumps.pop()
    set_quad('GOTO', -1, -1, jumps.pop())
    quadruples[end_pos].set_result(len(quadruples))


# Functions

def p_np_end_main(p):
    '''np_end_main : '''
    global scopes, current_scope
    scopes.set_size(current_scope)
    scopes.set_size('program')

def p_np_end_program(p):
    '''np_end_program : '''
    set_quad('END', -1, -1, -1)

def p_np_set_read_quad(p):
    '''np_set_read_quad : '''
    global operands, types
    var = operands.pop()
    set_quad('READ', -1, data_type_IDs[types.pop()], var)

def p_np_set_print_quad_str(p):
    '''np_set_print_quad_str : '''
    set_quad('PRINT_MULTIPLE', -1, -1, p[-1])

def p_np_set_print_quad_exp(p):
    '''np_set_print_quad_exp : '''
    global operands, types
    types.pop()
    set_quad('PRINT_MULTIPLE', -1, -1, operands.pop())

def p_np_set_print_same_line_quad_str(p):
    '''np_set_print_same_line_quad_str : '''
    set_quad('PRINT', -1, -1, p[-1])

def p_np_set_print_same_line_quad_exp(p):
    '''np_set_print_same_line_quad_exp : '''
    global operands, types
    types.pop()
    set_quad('PRINT', -1, -1, operands.pop())


def p_np_func_start(p):
    '''np_func_start : '''
    global scopes, current_scope, quadruples
    scopes.set_quad_count(current_scope, len(quadruples))

def p_np_add_params_type(p):
    '''np_add_params_type : '''
    global scopes, current_scope
    param_ID = p[-4]
    param_type = p[-2]
    current_scope_params = scopes.get_parameters(current_scope)
    current_scope_IDs_params = scopes.get_parameter_IDs(current_scope)
    current_scope_IDs_params.append(param_ID)
    current_scope_params.append(param_type)

def p_np_func_end(p):
    '''np_func_end : '''
    global scopes, current_scope, mem_count
    set_quad('ENDFUNC', -1, -1, -1)
    scopes.set_size(current_scope)
    mem_count.reset_local_counters()
    mem_count.reset_temp_counters()

def p_np_check_func_call(p):
    '''np_check_func_call : '''
    global scopes, params_stack, current_func_call_ID, func_call_IDs, operators
    current_func_call_ID = p[-2]
    if scopes.exists(current_func_call_ID):    
        params_stack.append(0)
        func_call_IDs.append(current_func_call_ID)
        set_quad('ERA', -1, -1, current_func_call_ID)
        operators.append('~')
    else:
        print_error(f'Function {current_func_call_ID} is not defined', '')

def p_np_add_func_call_param(p):
    '''np_add_func_call_param : '''
    global types, params_stack, func_call_IDs, scopes
    param_type = types.pop()
    params_count = params_stack.pop()
    current_func_call_ID = func_call_IDs[-1]
    function_call_params = scopes.get_parameters(current_func_call_ID)
    
    if(function_call_params[params_count] == param_type):
        set_quad('PARAM', operands.pop(), -1, f'_param_{params_count}')
        params_count += 1
        params_stack.append(params_count)
    else:
        print_error(f'The {params_count + 1}º argument of function {current_func_call_ID} should be of type {function_call_params[params_count]}', '')
    
def p_np_func_end_params(p):
    '''np_func_end_params : '''
    global params_stack, scopes, current_scope, temps_count, func_call_IDs, operators
    current_func_call_ID = func_call_IDs.pop()
    size_of_params = len(scopes.get_parameters(current_func_call_ID))
    operators.pop()
    if size_of_params == params_stack.pop():
        initial_function_addres = scopes.get_quad_count(current_func_call_ID)
        set_quad('GOSUB', current_func_call_ID, -1, initial_function_addres)
    else:
        print_error(f'''Function {current_func_call_ID}, requires {size_of_params} arguments''', '')
    
    fun_return_type = scopes.get_return_type(current_func_call_ID)
    if fun_return_type != 'void':
        current_scope_vars = scopes.get_vars_table(current_scope)
        temp_var_name = f"_temp{temps_count}"
        temps_count += 1
        current_scope_vars.add_var(temp_var_name, fun_return_type)
        new_address = get_vars_new_address(fun_return_type, True)
        current_scope_vars.set_var_address(temp_var_name, new_address)
        directory_var = scopes.get_vars_table('program').get_one(current_func_call_ID)
        set_quad('=', directory_var['address'], -1, new_address)
        operands.append(new_address)
        types.append(fun_return_type)

def p_np_set_return_quad(p):
    '''np_set_return_quad : '''
    global current_scope, scopes, operands, types
    func_return_type = scopes.get_return_type(current_scope)
    if (func_return_type == types.pop()):
        set_quad('RETURN', -1, -1, operands.pop())
    else:
        print_error(f'Function {current_scope} must return a value of type {func_return_type}', '')


##### Statistical Functions #####

def p_np_set_rand_quad(p):
    '''np_set_rand_quad : '''
    result_address = create_temp_address('int')
    lower_limit = p[-4]
    upper_limit = p[-2]
    operands.append(result_address)
    types.append('int')
    set_quad('RAND', lower_limit, upper_limit, result_address)

def p_np_set_mean_quad(p):
    '''np_set_mean_quad : '''
    arr_ID = p[-2]
    create_quad_statistics(arr_ID, 'MEAN')

def p_np_set_median_quad(p):
    '''np_set_median_quad : '''
    arr_ID = p[-2]
    create_quad_statistics(arr_ID, 'MEDIAN')
    
def p_np_set_variance_quad(p):
    '''np_set_variance_quad : '''
    arr_ID = p[-2]
    create_quad_statistics(arr_ID, 'VARIANCE')
    
def p_np_set_std_quad(p):
    '''np_set_std_quad : '''
    arr_ID = p[-2]
    create_quad_statistics(arr_ID, 'STD')

def p_np_set_plot_quad(p):
    '''np_set_plot_quad : '''
    
    x_array_var = get_var_directory(p[-4])
    y_array_var = get_var_directory(p[-2])

    if x_array_var['is_array'] and y_array_var['is_array']:
        if (x_array_var['type'] == 'int' or x_array_var['type'] == 'float') and (y_array_var['type'] == 'int' or y_array_var['type'] == 'float'):
                if x_array_var['arr_size'] == y_array_var['arr_size']:
                    set_quad('PLOT', x_array_var['address'], y_array_var['address'], x_array_var['arr_size'])
                else:
                    print_error(f'Arrays{p[-4]} and {p[-2]} must be of equal length', '')
        else:
            print_error('The plot function requires 2 arrays of type int or float', '')
    else:
        print_error('The plot function requires 2 arrays of type int or float', '')

##### Arrays #####

def p_np_check_is_array(p):
    '''np_check_is_array : '''
    global operands, types, operators
    operands.pop()   
    types.pop()
    
    arr_ID = p[-2]
    if(arr_ID is None):
        arr_ID = p[-3]
    
    current_var = get_var_directory(arr_ID)
    if (current_var['is_array']):
        operands.append(current_var['address'])
        types.append(current_var['type'])
        operators.append('|')
    else:
        print_error(f'Array {arr_ID} is not defined.', '')
    

def p_np_get_array_address(p):
    '''np_get_array_address : '''
    global operands, types, constants_table
    accessing_array_value = operands.pop()
    types.pop()
    array_init_address_const_address = create_cteint_address(operands.pop())
    pointer_address = create_new_pointer_address()
    
    set_quad('+', accessing_array_value, array_init_address_const_address, pointer_address)
    operators.pop()

    operands.append(pointer_address)

def p_np_verify_array_dim(p):
    '''np_verify_array_dim : '''
    global operands, constants_table, types
    accessing_array_type = types[-1]
    arr_ID = p[-4]
    if (arr_ID is None): 
        arr_ID = p[-5]
    if (accessing_array_type == 'int'):
        set_quad('VERIFY', operands[-1], constants_table[0], constants_table[get_var_directory(arr_ID)['arr_size']])
    else:
        print_error(f'Array {arr_ID} must be accesed using an int value', '')

parser = yacc.yacc()