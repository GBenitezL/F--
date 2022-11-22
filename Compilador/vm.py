import operator, statistics, random
from bisect import insort
from collections import deque
import matplotlib.pyplot as plt
from Compilador.parser import scopes, quadruples, constants_table
from Compilador.utils import print_error, data_type_values

class Memory:
    def __init__(self):
        self.dict = {}

mem_size = 1000
is_executing = True
global_mem = Memory()
current_mem = None
mem_stack = deque()
instruction_pointer = 0
instruction_pointer_stack = deque()
params_queue = deque()
func_call_IDs = deque()


##### MEMORY #####

def start_global_mem():
    global constants_table
    global global_mem
    global mem_size
    for index, (constant, value) in enumerate(constants_table.items()):
        global_mem.dict[value] = constant
    global_size = len(constants_table)
    global_size = global_size + scopes.get_size('program')
    check_mem(global_size)
    
def start_main_mem():
    global current_mem
    global mem_stack
    check_mem(scopes.get_size('main'))
    current_mem = Memory()

def check_mem(size):
    global mem_size
    if (mem_size < size):
        print_error('Insufficient Memory', 'EE-01')
    mem_size = mem_size - size

def save_mem_for_function(function_ID):
    global scopes
    if scopes.exists(function_ID):
        check_mem(scopes.get_size(function_ID))
    else:
        print_error(f'Function {function_ID} is yet to be defined', 'EE-02')
    
##### POINTERS #####

def arithmetic_operation(left_oper, right_oper, save_address, operation):
    save_pointer_value(save_address, operation(get_pointer_value(left_oper), get_pointer_value(right_oper)))

def assign_value(value_address, save_address):
    pointer = str(save_address)[0] == '5'
    if (pointer):
        save_address = find_address(save_address)
    save_pointer_value(save_address,get_pointer_value(value_address))

def get_pointer_value(address):
    global global_mem
    global current_mem
    pointer = str(address)[0] == '5'
    if (pointer):
        address = find_address(address)
    return find_address(address)

def save_pointer_value(address, value):
    global global_mem
    global current_mem
    mem_section = int(address / 10000)
    if mem_section == 1:
        global_mem.dict[address] = value
    else:
        current_mem.dict[address] = value
    
def update_instruction_pointer(new_pos = None):
    global instruction_pointer
    if new_pos is None:
        new_pos = instruction_pointer + 1
    inexistent = new_pos > len(quadruples)
    if inexistent:
        print_error('Cannot locate positon {new_pos}', 'EE-03')
    instruction_pointer = new_pos
    
def find_address(pointer):
    if pointer in current_mem.dict:
        value = current_mem.dict.get(pointer)
    elif pointer in global_mem.dict:
        value = global_mem.dict.get(pointer)
    else:
        print_error(f'Cannot locate value. {pointer} has not been assigned yet', 'EE-04')
        
    if (value == 'true'):
        value = True
    elif (value == 'false'):
        value = False
    return value

def save_pointer_value_on_input(save_address, type_to_read):
    input_value = input()
    try:
        match type_to_read:
            case 1:
                input_value = int(input_value)
            case 2:
                input_value = float(input_value)
            case 3:
                input_value = str(input_value)
                if len(input_value) > 1:
                    print_error(f'char should have a length of 1', 'EE-05')
            case 4:
                match input_value:
                    case 'true':
                        input_value = True
                    case 'false':
                        input_value = False
                    case _:
                        print_error(f'bool should have a value of either true or false', 'EE-06')
    except:
        print_error(f'Expected a value of type {data_type_values[type_to_read]}', 'EE-07')
    
    pointer = str(save_address)[0] == '5'    
    if (pointer):
        save_address = find_address(save_address)
    save_pointer_value(save_address, input_value)


##### FUNCTIONS #####

def go_to_function(function_ID, new_instruction_pointer):
    global mem_stack
    global instruction_pointer_stack
    global scopes
    global instruction_pointer
    global current_mem
    global func_call_IDs
    global params_queue
    param_IDs = scopes.get_parameter_IDs(function_ID)
    new_current_mem = Memory()
    if len(param_IDs) != 0:
        for param_ID in param_IDs:
            var_address = get_func_local_address(function_ID, param_ID)
            new_current_mem.dict[var_address] = get_pointer_value(params_queue.popleft())
    instruction_pointer_stack.append(instruction_pointer + 1)
    update_instruction_pointer(new_instruction_pointer)
    mem_stack.append(current_mem)
    current_mem = new_current_mem
    func_call_IDs.append(function_ID)

def on_function_end():
    global func_call_IDs
    global scopes
    global instruction_pointer_stack
    global current_mem
    global mem_stack
    global mem_size
    function_ID = func_call_IDs.pop()
    func_return_type = scopes.get_return_type(function_ID)
    if func_return_type != 'void':
        print_error(f'Function {function_ID} requires a return value of type {func_return_type}', 'EE-08')
    current_mem = mem_stack.pop()
    update_instruction_pointer(instruction_pointer_stack.pop())
    mem_size = mem_size + scopes.get_size(function_ID)

def on_function_end_with_return(return_value_address):
    global func_call_IDs
    global scopes
    global instruction_pointer_stack
    global current_mem
    global mem_stack
    global mem_size

    function_ID = func_call_IDs.pop()
    func_return_type = scopes.get_return_type(function_ID)
    if data_type_values[int(str(return_value_address)[1])] != func_return_type:
        print_error(f'Function {function_ID} requires a return value of type {func_return_type}', 'EE-08')
    save_pointer_value(get_func_global_address(function_ID), get_pointer_value(return_value_address))
    current_mem = mem_stack.pop()
    update_instruction_pointer(instruction_pointer_stack.pop())
    func_size = scopes.get_size(function_ID)
    mem_size = mem_size + func_size
    
def add_param_for_function_call(value_address):
    global params_queue
    params_queue.append(value_address)
    
def get_func_global_address(function_ID):
    global scopes
    directory_var = scopes.get_vars_table('program').get_one(function_ID)
    return directory_var.get('address')

def get_func_local_address(scope_ID, var_ID):
    global scopes
    directory_var = scopes.get_vars_table(scope_ID).get_one(var_ID)
    return directory_var.get('address')
        

##### ARRAYS #####

def verify_arr_access(access_value, arr_inferior_limit, arr_upp_limit):
    value = get_pointer_value(access_value)
    inferior_limit = get_pointer_value(arr_inferior_limit)
    upper_limit =  get_pointer_value(arr_upp_limit)
    if inferior_limit > value or upper_limit <= value:
        print_error(f'Out of bounds: {value} is not within the limits of {inferior_limit} and {upper_limit}', 'EE-09')

def get_array_as_list(starting_address, arr_size):
    numbers_list = []
    for x in range(arr_size):
        numbers_list.append(find_address(starting_address))
        starting_address += 1
    return numbers_list


##### STATISTICS #####

def calculate_mean(arr_size, array_var_address, save_address_pointer_value):
    sum_of_values = 0
    for x in range(arr_size):
        sum_of_values = sum_of_values + find_address(array_var_address)
    save_pointer_value(save_address_pointer_value, sum_of_values / arr_size)

def calculate_median(arr_size, array_var_address, save_address_pointer_value):
    numbers_list = []
    for x in range(arr_size):
        insort(numbers_list, find_address(array_var_address))
        array_var_address += 1
    save_pointer_value(save_address_pointer_value, statistics.median(numbers_list))

def calculate_variance_value(arr_size, array_var_address, save_address_pointer_value):
    numbers_list = get_array_as_list(array_var_address, arr_size)
    save_pointer_value(save_address_pointer_value, statistics.variance(numbers_list))

def calculate_std_value(arr_size, array_var_address, save_address_pointer_value):
    numbers_list = get_array_as_list(array_var_address, arr_size)
    save_pointer_value(save_address_pointer_value, statistics.stdev(numbers_list))

def create_random(lower_limit, upper_limit, save_address_pointer_value):
    save_pointer_value(save_address_pointer_value, random.randint(lower_limit, upper_limit))

def create_plot(x_array_var_address, y_array_var_address, arr_size):
    plt.plot(get_array_as_list(x_array_var_address, arr_size), get_array_as_list(y_array_var_address, arr_size), 'go')
    plt.show()


##### PRINTING #####

def print_value(value, multiple = False):
    is_address = type(value) is int
    if(is_address):
        value_to_print = get_pointer_value(value)
    else:
        value_to_print = value[1:-1]
    
    if multiple == False or value_to_print == '':
        print(value_to_print)
    else:
        print(value_to_print, end='')


# Print Global Memory
def print_global_mem():
    global global_mem
    for index, (address, value) in enumerate(global_mem.dict.items()):
        print(f'{index} \t\t {value} \t\t {address}')

# Print Current_Memory
def print_current_mem():
    global current_mem
    for index, (address, value) in enumerate(current_mem.dict.items()):
        print(f'{index} \t\t {value} \t\t {address}')


##### QUADRUPLES #####

def check_quadruples():
    global is_executing
    global instruction_pointer
    while is_executing:  
        operation = quadruples[instruction_pointer].get_operator()
        left_oper = quadruples[instruction_pointer].get_left_oper()
        right_oper = quadruples[instruction_pointer].get_right_oper()
        result = quadruples[instruction_pointer].get_result()
        
        match operation:
            case 28:
                is_executing = False
                print('\n\nProgram Executed Successfuly\n')
            case 1: 
                arithmetic_operation(left_oper, right_oper, result, operator.add)
                update_instruction_pointer()
            case 2:
                arithmetic_operation(left_oper, right_oper, result, operator.sub)
                update_instruction_pointer()
            case 3:
                if get_pointer_value(right_oper) == 0:
                    print_error(f'Cannot perform a division by 0', 'EE-10')
                arithmetic_operation(left_oper, right_oper, result, operator.truediv)
                update_instruction_pointer()
            case 4:
                arithmetic_operation(left_oper, right_oper, result, operator.mul)
                update_instruction_pointer()
            case 5:
                arithmetic_operation(left_oper, right_oper, result, operator.lt)
                update_instruction_pointer()
            case 6:
                arithmetic_operation(left_oper, right_oper, result, operator.le)
                update_instruction_pointer()
            case 7:
                arithmetic_operation(left_oper, right_oper, result, operator.gt)
                update_instruction_pointer()
            case 8:
                arithmetic_operation(left_oper, right_oper, result, operator.ge)
                update_instruction_pointer()
            case 9:
                arithmetic_operation(left_oper, right_oper, result, operator.eq)
                update_instruction_pointer()
            case 10:
                arithmetic_operation(left_oper, right_oper, result, operator.ne)
                update_instruction_pointer()
            case 11:
                arithmetic_operation(left_oper, right_oper, result, operator.and_)
                update_instruction_pointer()
            case 12:
                arithmetic_operation(left_oper, right_oper, result, operator.or_)
                update_instruction_pointer()
            case 13:
                assign_value(left_oper, result)
                update_instruction_pointer()
            case 20:
                update_instruction_pointer(result)
            case 21:
                if (get_pointer_value(left_oper)):
                    update_instruction_pointer(result)
                else:
                    update_instruction_pointer()
            case 22:
                if (get_pointer_value(left_oper)):
                    update_instruction_pointer()
                else:
                    update_instruction_pointer(result)
            case 23:
                go_to_function(left_oper, result)
            case 24:
                save_mem_for_function(result)
                update_instruction_pointer()
            case 25:
                verify_arr_access(left_oper, right_oper, result)
                update_instruction_pointer()
            case 26:
                add_param_for_function_call(left_oper)
                update_instruction_pointer()
            case 27:
                on_function_end()
            case 30:
                on_function_end_with_return(result)
            case 31:
                print_value(result)
                update_instruction_pointer()
            case 32:
                print_value(result, multiple= True)
                update_instruction_pointer()
            case 33:
                save_pointer_value_on_input(result, right_oper)
                update_instruction_pointer()
            case 34:
                calculate_mean(left_oper, right_oper, result)
                update_instruction_pointer()
            case 35:
                calculate_median(left_oper, right_oper, result)
                update_instruction_pointer()
            case 36:
                calculate_variance_value(left_oper, right_oper, result)
                update_instruction_pointer()
            case 37:
                calculate_std_value(left_oper, right_oper, result)
                update_instruction_pointer()
            case 38:
                create_random(left_oper, right_oper, result)
                update_instruction_pointer()
            case 39:
                create_plot(left_oper, right_oper, result)
                update_instruction_pointer()
            case _:
                instruction_pointer += 1


def start_vm():
    start_global_mem()
    start_main_mem()
    print('\nStarting Program Execution\n')
    check_quadruples()
    # print('Global Memory')
    # print_global_mem()
    # print('Last Memory')
    # print_current_mem()
 