import copy

"""
常量
"""
DIGITS = "0123456789"

"""
Token types
"""
TT_INT = "INT"
TT_FLOAT = "FLOAT"
TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT_DIV = "DIV"
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"
TT_EOF = "EOF"

"""
自定义Error
"""


class Error(object):
    def __init__(self, pos_start, pos_end, error_name, details):
        """
        :param pos_start: 错误开始位置
        :param pos_end: 错误终止位置
        :param error_name: 错误类型名称
        :param details: 错误细节
        """
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def __str__(self):
        res = f'{self.error_name}: {self.details}'
        res += f'File {self.pos_start.fn} , line {self.pos_end.ln + 1}'
        return res


class IllegalCharError(Error):
    # 非法字符错误
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Illegal Character", details)


class InvalidSyntaxError(Error):
    # 无效语法
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Invalid Syntax", details)


class Token(object):
    # <token-name attr-value>
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        """
        :param type_:
        :param value:
        :param pos_start: Position object
        :param pos_end:
        """
        self.type = type_
        self.value = value

        if pos_start:
            # Token 单个字符 + => pos_start = pos_end , advance
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance(self.value)  # 下一个token

        # Token 多个字符 123.122
        if pos_end:
            self.pos_end = pos_end

    def __repr__(self):
        # 方便调试 看信息
        if self.value:
            return f'{self.type}: {self.value}'
        return f'{self.type}'


class Position(object):
    def __init__(self, idx, ln, col, fn, txt):
        """
        :param idx: 索引
        :param ln: 行号
        :param col: 列号
        :param fn: 文件名
        :param txt: 内容
        """
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.txt = txt

    def advance(self, current_char):
        self.idx += 1  # 索引+1
        self.col += 1  # 列号+1

        if current_char == "\n":
            self.col = 0
            self.ln += 1

    def copy(self):
        return copy.deepcopy(self)
        # return Position(self.idx, self.ln, self.col, self.fn, self.txt)


"""
   词法分析器
"""


class Lexer(object):

    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    # 预读 独取下一个
    def advance(self):
        self.pos.advance(self.current_char)
        if self.pos.idx < len(self.text):
            self.current_char = self.text[self.pos.idx]  # 取了下一个, text => string
        else:
            self.current_char = None

    def make_tokens(self):
        """
        1. 遍历text
        2. 遍历的过程中，分别判断获取的内容
        """
        tokens = []
        while self.current_char is not None:
            if self.current_char in (" ", '\t'):
                # 空格和tab 跳过不处理
                self.advance()
            elif self.current_char in DIGITS:  # 数字
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            else:
                # 没有匹配到 非法字符错误
                pos_start = self.pos.copy()  # python -> 引用性调用， 赋值后操作会影响原有对象
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, f"'{char}")
        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num_str = ""
        dot_count = 0

        while self.current_char is not None and self.current_char in DIGITS + ".":
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += "."
            else:
                num_str += self.current_char
            self.advance()
        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))


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


"""
语法解析结果类
"""


class ParserResult(object):
    def __init__(self):
        self.error = None
        self.node = None

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self

    def register(self, res):
        if isinstance(res, ParserResult):
            if res.error:
                self.error = res.error
            return res.node
        return res


"""
语法解析器
"""


class Parser(object):
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

    def factor(self):
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

    def term(self):
        # term -> factor ((MUL | DIV) facter)*
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    def expr(self):
        # term((PLUS | MINUS) term)*
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def bin_op(self, func, ops):
        # 递归调用 构建AST
        res = ParserResult()
        # 1+1
        # 1
        # advance -> +
        left = res.register(func())
        while self.current_token.type in ops:
            op_token = self.current_token
            res.register(self.advance())
            right = res.register(func())
            left = BinOpNode(left, op_token, right)
        return res.success(left)


def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    # 生成AST
    parser = Parser(tokens)
    ast = parser.parse()
    return ast.node, ast.error
