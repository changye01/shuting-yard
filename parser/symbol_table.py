class SymbolTable(object):
    """
    符号表实现
    """

    def __init__(self):
        # 符号表
        self.symbols = {}
        # 用于判断作用域
        self.parent = None

    def get(self, name):
        """
        获取符号的值
        :param name:
        :return:
        """
        value = self.symbols.get(name, None)
        # func -> a -> 全局变量里有a
        if value is None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        """
        变量赋值
        :param name:
        :param value:
        :return:
        """
        self.symbols[name] = value


def remove(self, name):
    """
    删除变量
    :param self:
    :param name:
    :return:
    """
    del self.symbols[name]
