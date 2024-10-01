from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from src.SimpleDSLLexer import SimpleDSLLexer
from src.SimpleDSLParser import SimpleDSLParser
from src.SimpleDSLListener import SimpleDSLListener

class SimpleDSLCompiler(SimpleDSLListener):
    def __init__(self):
        self.variables = {}

    def enterAssignStatement(self, ctx: SimpleDSLParser.AssignStatementContext):
        var_name = ctx.ID().getText()
        value = self.evaluate(ctx.expr())
        self.variables[var_name] = value

    def enterPrintStatement(self, ctx: SimpleDSLParser.PrintStatementContext):
        value = self.evaluate(ctx.expr())
        print(value)

    def evaluate(self, ctx):
        if isinstance(ctx, SimpleDSLParser.MulDivExprContext):
            left = self.evaluate(ctx.expr(0))
            right = self.evaluate(ctx.expr(1))
            if ctx.op.type == SimpleDSLParser.MUL:
                return left * right
            else:
                return left / right
        elif isinstance(ctx, SimpleDSLParser.AddSubExprContext):
            left = self.evaluate(ctx.expr(0))
            right = self.evaluate(ctx.expr(1))
            if ctx.op.type == SimpleDSLParser.ADD:
                return left + right
            else:
                return left - right
        elif isinstance(ctx, SimpleDSLParser.IntExprContext):
            return int(ctx.INT().getText())
        elif isinstance(ctx, SimpleDSLParser.IdExprContext):
            var_name = ctx.ID().getText()
            return self.variables.get(var_name, 0)
        else:
            return 0

def main():
    lexer = SimpleDSLLexer(FileStream('example.dsl'))
    stream = CommonTokenStream(lexer)
    parser = SimpleDSLParser(stream)
    tree = parser.prog()

    compiler = SimpleDSLCompiler()
    walker = ParseTreeWalker()
    walker.walk(compiler, tree)

if __name__ == '__main__':
    main()