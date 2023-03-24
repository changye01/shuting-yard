from error import RTError
from tokens import *

"""
解释器
获得运行时结果
"""


class RTResult(object):
    def __init__(self):
        self.value = None
        self.error = None

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self

    def register(self, res):
        if res.error:
            self.error = res.error
        return res.value


class Number(object):
    def __init__(self, value):
        self.value = value
        self.set_pos()  # 报错的位置
        self.set_context()  # 方便定义错误，运行时报错的上下文
        self.context = None
        self.pos_end = None
        self.pos_start = None

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def added_by(self, other):
        # 加法操作
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    def subbed_by(self, other):
        # 加法操作
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    def multiplied_by(self, other):
        # 加法操作
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    def dived_by(self, other):
        # 加法操作
        if isinstance(other, Number):
            # 分母不能为0
            if other.value == 0:
                return None, RTError(other.pos_start, other.pos_start, '分母不可为0', self.context)
            return Number(self.value / other.value).set_context(self.context), None

    def powered_by(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return str(self.value)


"""
Context 上下文
"""


class Context(object):
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None  # 符号表


"""
Interpreter 解释器
"""


class Interpreter(object):
    def visit(self, node, context):
        """
        递归下降算法 ->ast node
        :param node: 起始node
        :param context: 上下文 方便定位错误
        :return:
        """
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node):
        raise Exception(f'No visit_{type(node).__name__}')

    def visit_NumberNode(self, node, context):
        return RTResult().success(
            Number(node.token.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_VarAccessNode(self, node, context):
        """
        访问变量的值
        :param node:
        :param context:
        :return:
        """
        res = RTResult()
        var_name = node.var_name_token.value  # 从token中获取变量名
        value = context.symbol_table.get(var_name)  # 从符号表中取值
        if not value:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                f"{var_name} is not defined",
                context
            ))
        # copy 自身避免影响后续操作
        value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)

    def visit_VarAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_token.value
        value = res.register(self.visit(node.value_node, context))
        if res.error:
            return res
        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_BinOpNode(self, node, context):
        # 二元操作
        res = RTResult()

        # 左递归
        left = res.register(self.visit(node.left_node, context))
        if res.error:
            return res
        # 右递归
        right = res.register(self.visit(node.right_node, context))
        if res.error:
            return res

        if node.op_token.type == TT_PLUS:
            result, error = left.added_by(right)
        elif node.op_token.type == TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_token.type == TT_MUL:
            result, error = left.multiplied_by(right)
        elif node.op_token.type == TT_DIV:
            result, error = left.dived_by(right)
        elif node.op_token.type == TT_POW:
            result, error = left.powered_by(right)
        else:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                f"{node.op_token.type} is not support",
                context
            ))

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.error:
            return res

        error = None

        if node.op_token.type == TT_MINUS:
            number, error = number.multiplied_by(Number(-1))

        if error:
            return res.failure(error)
        return res.success(number.set_pos(node.pos_start, node.pos_end))
