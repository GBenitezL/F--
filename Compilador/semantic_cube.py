from Compilador.utils import print_error

class Semantic_Cube:
    
    def getType(symbol, type1, type2):
        # print('checking', symbol, type1, type2)
        basic_symbols = ['+', '-', '*']
        comparison_symbols = ['<', '<=', '>', '>=', '==', '!=']
        if(symbol == '='):
            if type1 == type2:
                return True

        if(type1 == 'int' and type2 == 'int'):
            if(symbol == '/'):
                return 'float'
            elif(symbol in basic_symbols):
                return 'int'
            elif(symbol in comparison_symbols):
                return 'bool'

        if((type1 == 'int' or type1 == 'float') 
            and (type2 == 'int' or type2 == 'float')):
            if(symbol in basic_symbols or symbol == '/'):
                return 'float'
            elif(symbol in comparison_symbols):
                return 'bool'

        if((type1 == 'char' or type1 == 'int') 
            and (type2 == 'char' or type2 == 'int')):
            if(symbol in basic_symbols):
                return 'int'
            elif(symbol == '/'):
                return 'float'
            elif(symbol in comparison_symbols):
                return 'bool'

        if((type1 == 'char' or type1 == 'float') 
            and (type2 == 'char' or type2 == 'float')):
            if(symbol in basic_symbols or symbol == '/'):
                return 'float'
            elif(symbol in comparison_symbols):
                return 'bool'

        if(type1 == 'bool' and type2 == 'bool'):
            if(symbol == '&&' or 
                symbol == '||' or 
                symbol in comparison_symbols):
                return 'bool'

        print_error(f'Cannot perform operation {symbol} to {type1} and {type2}', '')

