from lexer import Lexer
from parser import Parser
from interpreter import Interpreter, Context, Number
from symbol_table import SymbolTable

# 全局作用域
global_symbol_table = SymbolTable()
# 默认变量 null
global_symbol_table.set('null', Number(0))


def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    # 生成AST
    parser = Parser(tokens)
    ast = parser.parse()
    # return ast.node, ast.error

    interpreter = Interpreter()
    context = Context("<program>")
    context.symbol_table = global_symbol_table
    res = interpreter.visit(ast.node, context)
    return res.value, res.error
