"""
AST 节点
"""


class NumberNode(object):
    def __init__(self, token):
        self.token = token
        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

    def __repr__(self):
        return f'{self.token}'


class VarAccessNode(object):
    """
    访问变量 a
    获取名为a的变量的值
    """

    def __init__(self, var_name_token):
        self.var_name_token = var_name_token

        self.pos_start = self.var_name_token.start
        self.pos_end = self.var_name_token.end

    def __repr__(self):
        return f"({self.var_name_token})"


class VarAssignNode(object):
    """
    为变量分配值 var a = 1
    """

    def __init__(self, var_name_token, value_node):
        self.var_name_token = var_name_token
        self.value_node = value_node

        self.pos_start = self.var_name_token.start
        self.pos_end = self.var_name_token.end

    def __repr__(self):
        return f"({self.var_name_token}, {self.value_node})"


class BinOpNode(object):
    # 二元操作 + - * /， 1+2 left_node = 1, op_token = +, right_node = 2
    def __init__(self, left_node, op_token, right_node):
        self.right_node = right_node
        self.op_token = op_token
        self.left_node = left_node
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node}, {self.op_token}, {self.right_node})'


class UnaryOpNode(object):
    #  一元操作 -1  op_token = -, node = 1
    def __init__(self, op_token, node):
        self.op_token = op_token
        self.node = node
        self.pos_start = self.op_token.pos_start
        self.pos_end = self.node.pos_end

    def __repr__(self):
        return f'{self.op_token}, {self.node}'
