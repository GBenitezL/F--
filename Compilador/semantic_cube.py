from utils import logical_operators, data_types, print_error

class Semantic_Cube:
    def getType(symbol, type1, type2):
        basic_symbols = [logical_operators['SUM'], logical_operators['MINUS'], logical_operators['TIMES']]
        comparison_symbols = [
            logical_operators['LESSTHAN'],
            logical_operators['LESSEQUALTHAN'],
            logical_operators['GREATERTHAN'],
            logical_operators['GREATEREQUALTHAN'],
            logical_operators['EQUAL'],
            logical_operators['DIFFERENT'],
        ]

        if(symbol == logical_operators['EQUALS']):
            if type1 == type2:
                return True
            else:
                print_error(f'Cannot compare {type1} to a {type2}', '')

        if(type1 == data_types['INTEGER'] and type2 == data_types['INTEGER']):
            if(symbol == logical_operators['DIVISION']):
                return data_types['FLOAT']
            elif(symbol in basic_symbols):
                return data_types['INTEGER']
            elif(symbol in comparison_symbols):
                return data_types['BOOLEAN']
            else:
                print_error(f'Cannot perform operation {symbol} to {type1} and {type2}', '')

        if((type1 == data_types['INTEGER'] or type1 == data_types['FLOAT'])  and (type2 == data_types['INTEGER'] or type2 == data_types['FLOAT'])):
            if(symbol in basic_symbols or symbol == logical_operators['DIVISION']):
                return data_types['FLOAT']
            elif(symbol in comparison_symbols):
                return data_types['BOOLEAN']
            else:
                print_error(f'Cannot perform operation {symbol} to {type1} and {type2}', '')

        if((type1 == data_types['CHAR'] or type1 == data_types['INTEGER']) and (type2 == data_types['CHAR'] or type2 == data_types['INTEGER'])):
            if(symbol in basic_symbols):
                return data_types['INTEGER']
            elif(symbol == logical_operators['DIVISION']):
                return data_types['FLOAT']
            elif(symbol in comparison_symbols):
                return data_types['BOOLEAN']
            else:
                print_error(f'Cannot perform operation {symbol} to {type1} and {type2}', '')

        if((type1 == data_types['CHAR'] or type1 == data_types['FLOAT']) and (type2 == data_types['CHAR'] or type2 == data_types['FLOAT'])):
            if(symbol in basic_symbols or symbol == logical_operators['DIVISION']):
                return data_types['FLOAT']
            elif(symbol in comparison_symbols):
                return data_types['BOOLEAN']
            else:
                print_error(f'Cannot perform operation {symbol} to {type1} and {type2}', '')

        if(type1 == data_types['BOOLEAN'] and type2 == data_types['BOOLEAN']):
            if(symbol == logical_operators['AND'] or symbol == logical_operators['OR'] or symbol in comparison_symbols):
                return data_types['BOOLEAN']
            else:
                print_error(f'Cannot perform operation {symbol} to {type1} and {type2}', '')

        print_error(f'Cannot perform operation {symbol} to {type1} and {type2}', '')