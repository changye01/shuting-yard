"""
AST 节点
"""


class NumberNode(object):
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f'{self.token}'


class BinOpNode(object):
    # 二元操作 + - * /， 1+2 left_node = 1, op_token = +, right_node = 2
    def __init__(self, left_node, op_token, right_node):
        self.right_node = right_node
        self.op_token = op_token
        self.left_node = left_node

    def __repr__(self):
        return f'({self.left_node}, {self.op_token}, {self.right_node})'


class UnaryOpNode(object):
    #  一元操作 -1  op_token = -, node = 1
    def __init__(self, op_token, node):
        self.op_token = op_token
        self.node = node

    def __repr__(self):
        return f'{self.op_token}, {self.node}'
