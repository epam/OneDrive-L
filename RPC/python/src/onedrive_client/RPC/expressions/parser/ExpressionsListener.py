# Generated from Expressions.g4 by ANTLR 4.7
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ExpressionsParser import ExpressionsParser
else:
    from ExpressionsParser import ExpressionsParser

# This class defines a complete listener for a parse tree produced by ExpressionsParser.
class ExpressionsListener(ParseTreeListener):

    # Enter a parse tree produced by ExpressionsParser#root.
    def enterRoot(self, ctx:ExpressionsParser.RootContext):
        pass

    # Exit a parse tree produced by ExpressionsParser#root.
    def exitRoot(self, ctx:ExpressionsParser.RootContext):
        pass


    # Enter a parse tree produced by ExpressionsParser#expression.
    def enterExpression(self, ctx:ExpressionsParser.ExpressionContext):
        pass

    # Exit a parse tree produced by ExpressionsParser#expression.
    def exitExpression(self, ctx:ExpressionsParser.ExpressionContext):
        pass


    # Enter a parse tree produced by ExpressionsParser#group.
    def enterGroup(self, ctx:ExpressionsParser.GroupContext):
        pass

    # Exit a parse tree produced by ExpressionsParser#group.
    def exitGroup(self, ctx:ExpressionsParser.GroupContext):
        pass


    # Enter a parse tree produced by ExpressionsParser#literal.
    def enterLiteral(self, ctx:ExpressionsParser.LiteralContext):
        pass

    # Exit a parse tree produced by ExpressionsParser#literal.
    def exitLiteral(self, ctx:ExpressionsParser.LiteralContext):
        pass


