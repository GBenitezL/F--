class Quadruple():
    def __init__(self, operator, left_oper, right_oper, result):
        self.operator = operator
        self.left_oper = left_oper
        self.right_oper = right_oper
        self.result = result

    def get_operator(self):
        return self.operator

    def get_left_oper(self):
        return self.left_oper

    def get_right_oper(self):
        return self.right_oper

    def get_result(self):
        return self.result

    def set_result(self, result):
        self.result = result

    def print(self):
        print('\t', self.operator, '\t', self.left_oper, '\t', self.right_oper, '\t', self.result)
