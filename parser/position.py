import copy


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
