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

    # def as_string(self):

    def __str__(self):
        res = f'{self.error_name}: {self.details}'
        res += f'File {self.pos_start.fn} , line {self.pos_end.ln + 1}'
        return res


class IllegalCharError(Error):
    # 非法字符错误
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Illegal Character", details)


class Token(object):
    # <token-name attr-value>
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

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


class Lexer(object):
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

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
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            else:
                # 没有匹配到 非法字符错误
                pos_start = self.pos.copy()  # python -> 引用性调用， 赋值后操作会影响原有对象
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, f"'{char}")
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


def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    return tokens, error
