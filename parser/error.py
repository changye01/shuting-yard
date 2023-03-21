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
        res += f' File {self.pos_start.fn} , line {self.pos_end.ln + 1}'
        return res


class IllegalCharError(Error):
    # 非法字符错误
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Illegal Character", details)


class InvalidSyntaxError(Error):
    # 无效语法
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Invalid Syntax", details)


class RTError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, "Runtime Error", details)
        self.context = context

    def __str__(self):
        result = self.generate_traceback()
        result += f'{self.error_name}: {self.details}'
        result += f' File {self.pos_start.fn} , line {self.pos_end.ln + 1}'
        return result

    def generate_traceback(self):
        """
        生成错误栈信息
        :return:
        """
        result = ''
        pos = self.pos_start
        ctx = self.context
        # 上下文可能存在parent
        while ctx:
            result = f' File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n' + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        return 'Traceback (most recent call last):\n' + result
