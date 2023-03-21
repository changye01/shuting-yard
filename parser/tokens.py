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
