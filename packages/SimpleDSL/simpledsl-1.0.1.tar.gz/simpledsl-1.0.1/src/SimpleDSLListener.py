# Generated from SimpleDSL.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .SimpleDSLParser import SimpleDSLParser
else:
    from SimpleDSLParser import SimpleDSLParser

# This class defines a complete listener for a parse tree produced by SimpleDSLParser.
class SimpleDSLListener(ParseTreeListener):

    # Enter a parse tree produced by SimpleDSLParser#prog.
    def enterProg(self, ctx:SimpleDSLParser.ProgContext):
        pass

    # Exit a parse tree produced by SimpleDSLParser#prog.
    def exitProg(self, ctx:SimpleDSLParser.ProgContext):
        pass


    # Enter a parse tree produced by SimpleDSLParser#stat.
    def enterStat(self, ctx:SimpleDSLParser.StatContext):
        pass

    # Exit a parse tree produced by SimpleDSLParser#stat.
    def exitStat(self, ctx:SimpleDSLParser.StatContext):
        pass


    # Enter a parse tree produced by SimpleDSLParser#AssignStatement.
    def enterAssignStatement(self, ctx:SimpleDSLParser.AssignStatementContext):
        pass

    # Exit a parse tree produced by SimpleDSLParser#AssignStatement.
    def exitAssignStatement(self, ctx:SimpleDSLParser.AssignStatementContext):
        pass


    # Enter a parse tree produced by SimpleDSLParser#PrintStatement.
    def enterPrintStatement(self, ctx:SimpleDSLParser.PrintStatementContext):
        pass

    # Exit a parse tree produced by SimpleDSLParser#PrintStatement.
    def exitPrintStatement(self, ctx:SimpleDSLParser.PrintStatementContext):
        pass


    # Enter a parse tree produced by SimpleDSLParser#MulDivExpr.
    def enterMulDivExpr(self, ctx:SimpleDSLParser.MulDivExprContext):
        pass

    # Exit a parse tree produced by SimpleDSLParser#MulDivExpr.
    def exitMulDivExpr(self, ctx:SimpleDSLParser.MulDivExprContext):
        pass


    # Enter a parse tree produced by SimpleDSLParser#IdExpr.
    def enterIdExpr(self, ctx:SimpleDSLParser.IdExprContext):
        pass

    # Exit a parse tree produced by SimpleDSLParser#IdExpr.
    def exitIdExpr(self, ctx:SimpleDSLParser.IdExprContext):
        pass


    # Enter a parse tree produced by SimpleDSLParser#IntExpr.
    def enterIntExpr(self, ctx:SimpleDSLParser.IntExprContext):
        pass

    # Exit a parse tree produced by SimpleDSLParser#IntExpr.
    def exitIntExpr(self, ctx:SimpleDSLParser.IntExprContext):
        pass


    # Enter a parse tree produced by SimpleDSLParser#AddSubExpr.
    def enterAddSubExpr(self, ctx:SimpleDSLParser.AddSubExprContext):
        pass

    # Exit a parse tree produced by SimpleDSLParser#AddSubExpr.
    def exitAddSubExpr(self, ctx:SimpleDSLParser.AddSubExprContext):
        pass



del SimpleDSLParser