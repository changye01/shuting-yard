# 操作符列表
OPERATOR_LIST = ('+', '-', '/', '*', '!', '=', '<', '>')
# 左操作符列表
OPERATOR_LEFT = ('+', '-', '/', '*', '%', '<', '>')
# 分隔符列表
DELIMITER_LIST = (',', '(', ')', ' ', ';')
# 函数列表
FUNCTION_LIST = ('Min', 'Max', 'Round', 'IF')

# 操作符需要的操作数个数
OPERAND_COUNT = {
    '*': 2,
    '/': 2,
    '%': 2,
    '+': 2,
    '=': 2,
    '^': 2,
    '-': 2,
    '<': 2,
    '>': 2,
    '!': 1,
}

# 函数所需的参数个数
FUNCTION_ARG_COUNT = {
    'Max': 2,
    'Min': 2,
    'Round': 2,
    "IF": 2,
}

# 算数运算符优先级
PRECEDENCE = {
    '!': 5,
    '^': 5,
    '*': 4,
    '/': 4,
    '%': 4,
    '+': 3,
    '-': 3,
    '>': 2,
    '<': 2,
    '=': 1
}


def op_left_assoc(c):
    """
    判断操作符是否是左结合
    :param c:
    :return:
    """
    return c in OPERATOR_LEFT


def is_operator(c):
    """
    判断是否是操作符
    :param c:
    :return:
    """
    return c in OPERATOR_LIST


def is_digit(c):
    """
    判断是否是数字
    :param c:
    :return:
    """
    try:
        float(c)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(c)
        return True
    except (TypeError, ValueError):
        pass

    return False


def is_variable(c):
    """
    判断是否是变量
    :param c:
    :return:
    """
    return not is_function(c) and c.isalpha()


def is_function(c):
    """
    判断是否是函数
    :param c:
    :return:
    """
    return c in FUNCTION_LIST


# 操作符
# 优先级	符号	运算顺序
# 1		!		从右至左
# 2		* / %	从左至右
# 3		+ -		从左至右
# 4		=		从右至左
def op_precedent(c):
    # 输入不是运算符 返回0
    return PRECEDENCE.get(c, 0)


def op_arg_count(c):
    return OPERAND_COUNT.get(c, 0)


def func_arg_count(c):
    return FUNCTION_ARG_COUNT.get(c, 0)


def assign(vari_dict, a, b):
    vari_dict[a] = b


def atof(s):
    val = sign = i = 0
    power = 1
    while i < len(s) and s[i].isspace():
        i += 1

    sign = -1 if s[i] == '-' else 1
    if s[i] in '+-':
        i += 1

    while i < len(s):
        if s[i].isdigit():
            val = val * 10 + int(s[i])
            i += 1
        elif s[i] == '.':
            i += 1
            while i < len(s) and s[i].isdigit():
                val = val * 10 + int(s[i])
                power *= 10
                i += 1
            break
        else:
            break
    # 不要使用 sign * val * 10 ** power 这种方式 这样会变成浮点数运算, 导致出现精度问题
    return val * sign / power if power != 1 else val * sign


def arithmetic_calculation(vari_dict, a, b, op):
    # 算数表达式实现
    # python 没有switch 多分支选择 所以用字典来实现
    arithmetic = {
        '+': lambda vari, x, y: float(x) + float(y),
        '-': lambda vari, x, y: float(x) - float(y),
        '/': lambda vari, x, y: float(x) / float(y),
        '*': lambda vari, x, y: float(x) * float(y),
        '%': lambda vari, x, y: float(x) % float(y),
        "=": assign
    }
    return arithmetic.get(op, 0)(vari_dict, a, b)


def function_calculation(func, *args):
    # 函数表达式实现
    function = {
        'Min': lambda x, y: min(x, y),
        'Max': lambda x, y: max(x, y),
        'Round': lambda x, y: round(x, int(y)),
        'IF': lambda x, y, z: y if x else z
    }
    return function.get(func, 0)(*args)


def shunting_yard(formula: str, output: list):
    str_pos = 0
    # 操作数堆栈
    stack = []

    while str_pos < len(formula):
        c = parameter = formula[str_pos]
        i = str_pos + 1
        if c == ' ':
            str_pos = i
            continue
        if c not in DELIMITER_LIST and not is_operator(c):
            while i < len(formula) and formula[i] not in DELIMITER_LIST and not is_operator(formula[i]):
                parameter += formula[i]
                i += 1
        # 扫描到左括号直接入栈
        if parameter == '(':
            stack.append(parameter)
        # 如果输入为数字 或 变量符，则直接入输出队列
        elif is_digit(parameter):
            output.append(atof(parameter))
        elif is_variable(parameter):
            output.append(parameter)
        # 如果输入为函数记号，则压入堆栈
        elif is_function(parameter):
            stack.append(parameter)
        # 如果输入为函数分割符（如: 逗号）
        elif parameter == ',':
            pe = False
            while len(stack):
                # stack char
                sc = stack[-1]
                # 扫描左括号
                # 跳出输出循环，此时左括号作为函数边界判定，所以不出栈
                if sc == '(':
                    pe = True
                    break
                else:
                    # 栈顶元素不是左括号
                    # 将栈顶元素依次出栈并放入输出队列
                    output.append(stack.pop())
            # 如果没有遇到左括号，则有可能是符号放错或者不匹配
            if not pe:
                print("Error: 分隔符或括号不匹配")
                return False
        # 如果输入符号为运算符
        elif is_operator(parameter):
            while len(stack):
                sc = stack[-1]
                # sc为其栈顶元素
                # 如果c是左结合性的且它的优先级小于等于栈顶运算符sc的优先级
                # 或者c是右结合性且它的优先级小于栈顶运算符sc的优先级
                # 将栈顶元素sc出栈，否则sc进栈
                if is_operator(sc) and ((op_left_assoc(parameter) and (op_precedent(parameter) <= op_precedent(sc))) or
                                        (not op_left_assoc(parameter) and op_precedent(parameter) < op_precedent(sc))):
                    output.append(stack.pop())
                else:
                    break
            # c的优先级大于或大于等于结合性的要求，则将其入栈
            stack.append(parameter)
        # 扫描到右括号
        elif parameter == ')':
            pe = False
            # 从栈顶向下扫描左括号，将扫描到左括号之前的栈顶运算符出栈并放入输出队列
            while len(stack):
                sc = stack[-1]
                if sc == '(':
                    pe = True
                    break
                else:
                    output.append(stack.pop())
            if not pe:
                print("Error: 括号不匹配")
                return False
            # 左括号出栈且不放入输出队列
            stack.pop()
            # 扫描完左括号后
            # 如果栈顶元素是函数运算符
            # 则将其出栈并放入输出队列
            if len(stack):
                sc = stack[-1]
                if is_function(sc):
                    output.append(stack.pop())
        else:
            print("Error: 不支持的字符: \"%s\"" % parameter)
            return False
        str_pos = i

    # 当所有元素已经读完
    # 栈中还有剩余运算符
    while len(stack):
        sc = stack[-1]
        # 如果剩余括号，则符号放错或者不匹配
        if sc == '(' or sc == ')':
            print("Error: 括号不匹配")
            return False
        output.append(stack.pop())

    return True


# def execution_order(formula_list: list):
#     print("order: (arguments in reverse order)")
#     str_pos = 0
#     run_num, res = 0, ''
#     stack = []
#
#     print(formula_list)
#     while str_pos < len(formula_list):
#         # 读取下一个参数
#         c = formula_list[str_pos]
#         # 如果是数字或者标识，则推入栈中
#         if is_indent(c):
#             stack.append(c)
#         # 如果是操作符 (操作符在这里表示运算符和函数)
#         elif is_operator(c) or is_function(c):
#             res = "_%02d" % run_num
#             print("%s = " % res, end='')
#             run_num += 1
#             # 运算符和函数的参数个数是已知的
#             nargs = op_arg_count(c)
#             # 栈中的参数少于nargs，则符号放错
#             if len(stack) < nargs:
#                 # （error）用户没有在表达式中输入足够的值
#                 print("Error: 表达式参数不足")
#                 return False
#             # Else 从堆栈取出nargs个参数
#             # 使用值作为参数评估运算符。
#             if is_function(c):
#                 print("%s(" % c, end='')
#                 while nargs > 0:
#                     sc = stack.pop()
#                     if nargs > 1:
#                         print("%s, " % sc, end='')
#                     else:
#                         print("%s)" % sc)
#                     nargs -= 1
#             else:
#                 sc = stack.pop()
#                 if nargs == 1:
#                     print("%s %s;" % (c, sc))
#                 else:
#                     sec_sc = stack.pop()
#                     print("%s %s %s;" % (sec_sc, c, sc))
#             stack.append(res)
#         str_pos += 1
#         # print(c, stack)
#
#     if len(stack) == 1:
#         sc = stack.pop()
#         print("%s is a result" % sc)
#         return True
#     return False

def vari_value(vari_dict, vari_name):
    return vari_dict.get(vari_name, vari_name) if is_variable(str(vari_name)) else vari_name


def execute(formula_list: list):
    print("execute: ", end='')
    str_pos = 0
    stack, vari_dict = [], {}

    while str_pos < len(formula_list):
        # 读取下一个参数 char
        c = formula_list[str_pos]
        # 如果是数字或者标识，则推入栈中
        if is_digit(c):
            stack.append(c)
        elif is_variable(c):
            stack.append(c)
        # 如果是操作符 (操作符在这里表示运算符和函数)
        elif is_operator(c) or is_function(c):
            res = 0
            # 运算符和函数的参数个数是已知的
            nargs = op_arg_count(c) if is_operator(c) else func_arg_count(c)
            # 栈中的参数少于nargs，则符号放错
            # print(c, nargs, stack)
            if len(stack) < nargs:
                # （error）用户没有在表达式中输入足够的值
                print("Error: 表达式参数不足")
                return False
            # Else 从堆栈取出nargs个参数
            # 使用值作为参数评估运算符。
            if is_function(c):
                args = []
                while nargs:
                    args.insert(0, vari_value(vari_dict, stack.pop()))
                    nargs -= 1
                res = function_calculation(c, *args)
            else:
                sc = vari_value(vari_dict, stack.pop())
                if nargs == 1:
                    pass
                else:
                    # 第二个参数放在第一位
                    sec_sc = vari_value(vari_dict, stack.pop())
                    res = arithmetic_calculation(vari_dict, sec_sc, sc, c)
            res and stack.append(res)
        str_pos += 1

    if len(stack) == 1:
        sc = vari_value(vari_dict, stack.pop())
        print("%s is a result" % sc)
        return True
    return False


def main():
    # functions: A() B(a) C(a, b), D(a, b, c)...
    # identifiers: 0 1 2 3 ... and a b c d e ...
    # operators: = - + / * % !
    # formula = "a = D(f - b * c + d, !e, g)"
    # formula = "51 + ((1 + 2) * 4) - 31"
    # formula = "1+2+3"
    # Max
    # formula = "a = Max(100+(考核项.完成值-考核项.目标值)*2, 120)"
    # Min Round
    # formula = "Round(Min(80+(考核项.完成值/考核项.目标值-1)*100,120),2)"
    # Min Max IF Round
    formula = "Min(100, Max(0, IF(考核项.完成值 / 考核项.目标值 < 0.5, 0, Round(考核项.完成值 / 考核项.目标值 * 100, 2))))"
    complete = 10
    target = 20
    formula = formula.replace('考核项.完成值', str(complete))
    formula = formula.replace('考核项.目标值', str(target))
    print("input:%s" % formula)

    # todo : 增加预编译
    output = list()
    if shunting_yard(formula, output):
        print("output:", output)
        # execute(output)
        # if (not execution_order(output)):
        #     print("Invalid input")


if __name__ == '__main__':
    main()
