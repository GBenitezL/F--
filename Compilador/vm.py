import operator, statistics, random, bisect
from collections import deque
import matplotlib.pyplot as plt
from utils import print_error, data_type_values
from parser import scopes, quadruples, constants_table

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


def print_global_mem():
    global global_mem
    for index, (address, value) in enumerate(global_mem.dict.items()):
        print(f'{index} \t\t {value} \t\t {address}')

def print_current_mem():
    global current_mem
    for index, (address, value) in enumerate(current_mem.dict.items()):
        print(f'{index} \t\t {value} \t\t {address}')

def check_mem(size):
    global mem_size
    if (mem_size < size):
        print_error('Insufficient Memory', '')
    mem_size = mem_size - size

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
    
def find_address(pointer):
    if pointer in current_mem.dict:
        value = current_mem.dict.get(pointer)
    elif pointer in global_mem.dict:
        value = global_mem.dict.get(pointer)
    else:
        print_error(f'Cannot locate value. {pointer} has not been assigned yet', '')
        
    if (value == 'true'):
        value = True
    elif (value == 'false'):
        value = False
    return value

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
        print_error('Instruction pointer cannot locate positon {new_pos}', '')
    instruction_pointer = new_pos
    
def arithmetic_operation(left_oper, right_oper, save_address, operation):
    save_pointer_value(save_address, operation(get_pointer_value(left_oper), get_pointer_value(right_oper)))

def assign_value(value_address, save_address):
    pointer = str(save_address)[0] == '5'
    if (pointer):
        save_address = find_address(save_address)
    
    save_pointer_value(save_address,get_pointer_value(value_address))

def print_value(value, jump_line = False):
    is_address = type(value) is int
    if(is_address):
        value_to_print = get_pointer_value(value)
    else:
        value_to_print = value[1:-1]
    
    if jump_line == False:
        print(value_to_print, end='')
    else:
        print(value_to_print)


def check_quadruples():
    global is_executing
    global instruction_pointer

    while is_executing:
        
        operation = quadruples[instruction_pointer].get_operator()
        left_oper = quadruples[instruction_pointer].get_left_oper()
        right_oper = quadruples[instruction_pointer].get_right_oper()
        result = quadruples[instruction_pointer].get_result()
        
        match operation:
            case 27:
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
                    print_error(f'Cannot perform a division by 0', '')
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
            case _:
                instruction_pointer += 1


def execute():
    start_global_mem()
    start_main_mem()
    print('\nStarting Program Execution\n')
    check_quadruples()
    # print('Global Memory')
    # print_global_mem()
    # print('Last Memory')
    # print_current_mem()
 