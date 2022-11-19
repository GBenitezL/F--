class Memory():
    count_global_int =  1100
    count_global_float= 1200
    count_global_char = 1300
    count_global_bool = 1400

    count_local_int =   2100
    count_local_float = 2200
    count_local_char =  2300
    count_local_bool =  2400

    count_temp_int =    3100
    count_temp_float =  3200
    count_temp_char =   3300
    count_temp_bool =   3400

    count_const_int =   4100
    count_const_float = 4200
    count_const_char =  4300
    count_const_bool =  4400

    count_pointers =    5000

    def reset_local_counters(self):
        self.count_local_int = 2100
        self.count_local_float = 2200
        self.count_local_char = 2300
        self.count_local_bool = 2400
        
    def reset_temp_counters(self):
        self.count_temp_int = 3100
        self.count_temp_float = 3200
        self.count_temp_char = 3300
        self.count_temp_bool = 3400
    
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