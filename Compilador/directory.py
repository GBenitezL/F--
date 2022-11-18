from utils import print_error

types_enum = {
    'int': 0,
    'float': 1,
    'bool': 2,
    'char': 3,
}


class Directory():
    def __init__(self):
        self.directory = {}

    def exists(self, id):
        return id in self.directory

    def get_one(self, id):
        if id not in self.directory:
            return 'Not Found'
        return self.directory[id]
    
    def print_directory(self):
        for key, value in self.directory.items():
            print(f'{key}: {value}')


class Scopes_Directory(Directory):
    def add_new_scope(self, id, return_type, vars_table):
        if self.exists(id):
            print_error(f'{id} already exists in this scope', '')
        if return_type not in ['int', 'float', 'char', 'bool', 'void']:
            print_error(f'{id} does not have a return type {return_type}', '')
        parameters = []
        params_IDs = []
        self.directory[id] = { 'vars_table': vars_table, 'return_type': return_type, 'parameters': parameters, 
            'params_IDs': params_IDs,  'count': None }

    def get_vars_table(self, id):
        return self.directory[id]['vars_table']

    def get_parameters(self, id):
        return self.directory[id]['parameters']
    
    def get_parameter_IDs(self, id):
        return self.directory[id]['params_IDs']

    def get_return_type(self, id):
        return self.directory[id]['return_type']

    def set_quad_count(self, id, count):
        self.directory[id]['count'] = count

    def get_quad_count(self, id):
        return self.directory[id]['count']
    
    def set_size(self, id):
        vars_table = self.directory[id]['vars_table'].directory
        parameters = self.directory[id]['parameters']
        types_counter = [0] * 4 # Starts array with 0's
        total_size = 0
        for key, value in vars_table.items():
            var_type = value['type']
            item_size = 1
            if ('bool_array' in value.keys() and value['bool_array']):
                item_size = value['arr_size']
            data_type = types_enum[var_type]
            types_counter[data_type] += item_size
            total_size += item_size

        self.directory[id]['types_counter'] = types_counter
        self.directory[id]['total_vars'] = total_size
        
    def get_size(self, id):
        return self.directory[id]['total_vars']

    def print_directory(self):
        for key, value in self.directory.items():
            print(f'Scope {key}:')
            for key, value in value.items():
                if key == 'vars_table':
                    print(f'Vars table for {key}')
                    value.print_directory()
                else:
                    print(f'{key}: {value}')
            print()


class Vars(Directory):
    def __init__(self, scope):
        super().__init__()
        self.scope = scope
    
    def add_var(self, id, type, value = None):
        if id in self.directory:
            print_error('Variable {id} has already been declared in this scope', '')
        if type == 'void' or type not in ['int', 'float', 'char', 'bool']:
            print_error(f'{id} does not have a return type {type}', '')
        self.directory[id] = {'type': type ,'value': value, 'address': None}
    
    def set_var_address(self, id, address):
        self.directory[id]['address'] = address
    
    def set_arrray_values(self, id, bool_arr = False, arr_size = None):
        self.directory[id]['bool_arr'] = bool_arr
        self.directory[id]['arr_size'] = arr_size
