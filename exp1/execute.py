
"""
def execution_order(formula_list: list):
    print("order: (arguments in reverse order)")
    str_pos = 0
    run_num, res = 0, ''
    stack = []
    print(formula_list)
    while str_pos < len(formula_list):
        # 读取下一个参数
        c = formula_list[str_pos]
        # 如果是数字或者标识，则推入栈中
        if is_indent(c):
            stack.append(c)
        # 如果是操作符 (操作符在这里表示运算符和函数)
        elif is_operator(c) or is_function(c):
            res = "_%02d" % run_num
            print("%s = " % res, end='')
            run_num += 1
            # 运算符和函数的参数个数是已知的
            nargs = op_arg_count(c)
            # 栈中的参数少于nargs，则符号放错
            if len(stack) < nargs:
                # （error）用户没有在表达式中输入足够的值
                print("Error: 表达式参数不足")
                return False
            # Else 从堆栈取出nargs个参数
            # 使用值作为参数评估运算符。
            if is_function(c):
                print("%s(" % c, end='')
                while nargs > 0:
                    sc = stack.pop()
                    if nargs > 1:
                        print("%s, " % sc, end='')
                    else:
                        print("%s)" % sc)
                    nargs -= 1
            else:
                sc = stack.pop()
                if nargs == 1:
                    print("%s %s;" % (c, sc))
                else:
                    sec_sc = stack.pop()
                    print("%s %s %s;" % (sec_sc, c, sc))
            stack.append(res)
        str_pos += 1
        # print(c, stack)
    if len(stack) == 1:
        sc = stack.pop()
        print("%s is a result" % sc)
        return True
    return False
"""
