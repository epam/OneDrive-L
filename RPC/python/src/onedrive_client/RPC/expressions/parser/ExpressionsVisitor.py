# Generated from Expressions.g4 by ANTLR 4.7
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ExpressionsParser import ExpressionsParser
else:
    from ExpressionsParser import ExpressionsParser

# This class defines a complete generic visitor for a parse tree produced by ExpressionsParser.

class ExpressionsVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ExpressionsParser#root.
    def visitRoot(self, ctx:ExpressionsParser.RootContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpressionsParser#expression.
    def visitExpression(self, ctx:ExpressionsParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpressionsParser#group.
    def visitGroup(self, ctx:ExpressionsParser.GroupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExpressionsParser#literal.
    def visitLiteral(self, ctx:ExpressionsParser.LiteralContext):
        return self.visitChildren(ctx)



del ExpressionsParser