from lexer import Lexer
from parser import Parser
from interpreter import Interpreter, Context


def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    # 生成AST
    parser = Parser(tokens)
    ast = parser.parse()
    # return ast.node, ast.error

    interpreter = Interpreter()
    context = Context("<program>")
    res = interpreter.visit(ast.node, context)
    return res.value, res.error
