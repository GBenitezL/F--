class Memory():
    count_global_int =  11000
    count_global_float= 12000
    count_global_char = 13000
    count_global_bool = 14000

    count_local_int =   21000
    count_local_float = 22000
    count_local_char =  23000
    count_local_bool =  24000

    count_temp_int =    31000
    count_temp_float =  32000
    count_temp_char =   33000
    count_temp_bool =   34000

    count_const_int =   41000
    count_const_float = 42000
    count_const_char =  43000
    count_const_bool =  44000

    count_pointers =    50000

    def reset_local_counters(self):
        self.count_local_int = 21000
        self.count_local_float = 22000
        self.count_local_char = 23000
        self.count_local_bool = 24000
        
    def reset_temp_counters(self):
        self.count_temp_int = 31000
        self.count_temp_float = 32000
        self.count_temp_char = 33000
        self.count_temp_bool = 34000
    
    def set_count(self, counter_type, type, space = 1):
        match counter_type:
            case 'global':
                match type:
                    case 'int':
                        self.count_global_int = self.count_global_int + space
                    case 'float':
                        self.count_global_float = self.count_global_float + space
                    case 'char':
                        self.count_global_char = self.count_global_char + space
                    case 'bool':
                        self.count_global_bool = self.count_global_bool + space
            case 'local':
                match type:
                    case 'int':
                        self.count_local_int = self.count_local_int + space
                    case 'float':
                        self.count_local_float = self.count_local_float + space
                    case 'char':
                        self.count_local_char = self.count_local_char + space
                    case 'bool':
                        self.count_local_bool = self.count_local_bool + space
            case 'temp':
                match type:
                    case 'int':
                        self.count_temp_int = self.count_temp_int + space
                    case 'float':
                        self.count_temp_float = self.count_temp_float + space
                    case 'char':
                        self.count_temp_char = self.count_temp_char + space
                    case 'bool':
                        self.count_temp_bool = self.count_temp_bool + space
            case 'const':
                match type:
                    case'int':
                        self.count_const_int = self.count_const_int + space
                    case 'float':
                        self.count_const_float = self.count_const_float + space
                    case 'char':
                        self.count_const_char = self.count_const_char + space
                    case 'bool':
                        self.count_const_bool = self.count_const_bool + space
            case 'pointer':
                self.count_pointers = self.count_pointers + space