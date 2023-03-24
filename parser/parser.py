from tokens import *
from error import *
from ast_node import *


class ParserResult(object):
    """
    语法解析结果类
    """

    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self

    def register_advancement(self):
        self.advance_count += 1

    def register(self, res):
        # # 避免递归子层执行报错， 父层可以判断
        # if isinstance(res, ParserResult):
        #     if res.error:
        #         self.error = res.error
        #     return res.node
        # return res
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        return res.node


class Parser(object):
    """
    语法解析器
    """

    def __init__(self, tokens):
        self.current_token = None
        self.tokens = tokens
        self.token_idx = -1
        self.advance()

    def advance(self):
        self.token_idx += 1
        if self.token_idx < len(self.tokens):
            self.current_token = self.tokens[self.token_idx]
        return self.current_token

    def parse(self):
        res = self.expr()
        if not res.error and self.current_token.type != TT_EOF:
            # 返回报错
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "Expected '+','-','*' or '/'"
            ))
        return res

    def factor1(self):
        """
        factor -> INT | FLOAT
               -> (PLUS | MINUS) factor
               -> LPAREN expr RPAREN
        :return:
        """
        res = ParserResult()
        token = self.current_token

        """
        1 + 1
        INT -> 1
        token = +
        并不需要error判断 因为只是一个简单的token

        -1 + 1
        MINUS -> - 
        token = 1
        token = factor
        factor 非终止符
        因为它是非终止符 会继续进行匹配 匹配的过程中 可以发现error
        所以要进行error的判断
        """
        if token.type in (TT_INT, TT_FLOAT):
            # factor -> INT | FLOAT
            res.register(self.advance())
            return res.success(NumberNode(token))

        elif token.type in (TT_PLUS, TT_MINUS):
            # (PLUS | MINUS) factor
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(token, factor))

        elif token.type == TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error:
                return res

            if self.current_token.type == TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                # 返回报错
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Expected ')'"
                ))
        return res.failure(InvalidSyntaxError(
            self.current_token.pos_start, self.current_token.pos_end,
            "Expected int or float"
        ))

    def factor(self):
        """
        factor  -> (PLUS | MINUS) factor
                -> power
        :return:
        """
        res = ParserResult()
        token = self.current_token

        if token.type in (TT_MINUS, TT_PLUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(token, factor))
        return self.power()

    def power(self):
        """
        power   -> atom (POW factor) *
        :return:
        """
        return self.bin_op(self.atom, (TT_POW,), self.factor)

    def atom(self):
        res = ParserResult()
        token = self.current_token

        if token.type in (TT_INT, TT_FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(token))

        elif token.type == TT_IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(token))

        elif token.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res

            if self.current_token.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Expected ')'"
                ))
        return res.failure(InvalidSyntaxError(
            token.pos_start, token.pos_end,
            "Expected int, float, identifier, '+', '-', '*', '/', '(' or ')'"
        ))

    def term(self):
        # term -> factor ((MUL | DIV) facter)*
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    def expr(self):
        # # term((PLUS | MINUS) term)*
        # return self.bin_op(self.term, (TT_PLUS, TT_MINUS))
        # expr    -> KEYWORD:var IDENTIFIER EQ expr
        #         -> term (( PLUS | MINUS ) term)*
        res = ParserResult()

        if self.current_token.matches(TT_KEYWORDS, 'var'):
            res.register_advancement()
            self.advance()

            # 不是变量名 报错
            if self.current_token.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Expected identifier"
                ))

            var_name = self.current_token
            res.register_advancement()
            self.advance()
            if self.current_token.type != TT_EQ:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Expected '='"
                ))

            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            return res.success(VarAssignNode(var_name, expr))
        else:
            node = res.register(self.bin_op(self.term, (TT_PLUS, TT_MINUS)))
            if res.error:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Expected 'var', int, float, identifier, '+', '-' or '('"
                ))
            return res.success(node)

    # def bin_op1(self, func, ops):
    #     # 递归调用 构建AST
    #     res = ParserResult()
    #     # 1+1
    #     # 1
    #     # advance -> +
    #     left = res.register(func())
    #     while self.current_token.type in ops:
    #         op_token = self.current_token
    #         res.register(self.advance())
    #         right = res.register(func())
    #         left = BinOpNode(left, op_token, right)
    #     return res.success(left)

    def bin_op(self, func_a, ops, func_b=None):
        # 递归调用 构建AST
        if func_b is None:
            func_b = func_a
        res = ParserResult()
        # 1+1
        # 1
        # advance -> +
        left = res.register(func_a())
        while self.current_token.type in ops:
            op_token = self.current_token
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            left = BinOpNode(left, op_token, right)
        return res.success(left)
