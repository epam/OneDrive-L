"""Provides implementation of expressions interpreter."""
import collections
from typing import Dict, Set

import antlr4
import antlr4.error

from .exceptions import ExpressionSyntaxError, UnknownVariable
from .parser.ExpressionsLexer import ExpressionsLexer
from .parser.ExpressionsParser import ExpressionsParser
from .parser.ExpressionsVisitor import (
    ExpressionsVisitor as ExpressionsVisitorBase
)


class _ExpressionsVisitor(ExpressionsVisitorBase):
    """Performs actual evaluation of given expression."""
    def __init__(
        self,
        variables: Dict[str, bool] = None,
        literals: Dict[int, bool] = None,
        default: bool = None
    ):
        if variables is not None:
            self.variables = variables
        else:
            self.variables = {}

        if literals is not None:
            self.literals = literals
        else:
            self.literals = {}
        self.default = default

        self.cache = collections.defaultdict(dict)

    @staticmethod
    def __get_position(ctx):
        return f'{ctx.stop.line}:{ctx.stop.column + 1}'

    def visitRoot(
        self,
        ctx: ExpressionsParser.RootContext
    ):
        return self.visit(ctx.expr)

    def visitExpression(self, ctx: ExpressionsParser.ExpressionContext):
        if ctx.operator:
            arguments = [
                self.visit(c) for c in ctx.children
                if not (hasattr(c, 'symbol') and
                        c.symbol.type == ctx.operator.type)
            ]
            if ctx.operator.type == ctx.parser.AND:
                return all(arguments)
            elif ctx.operator.type == ctx.parser.OR:
                return any(arguments)
            elif ctx.operator.type == ctx.parser.NOT:
                assert len(arguments) == 1
                return not arguments[0]
            else:
                raise NotImplementedError(
                    f'Operator "{ctx.operator.txt}" is not implemented.'
                )

        variable = ctx.IDENTIFIER()
        if variable is not None:
            try:
                return self.variables[variable.getText()]
            except KeyError:
                if self.default is not None:
                    return self.default

                raise UnknownVariable(
                    f'Unknown variable: "{variable.getText()}" at '
                    f'{self.__get_position(ctx)}.'
                )

        literal = ctx.literal()
        if literal is not None:
            return self.visit(literal)

        group = ctx.group()
        if group is not None:
            return self.visit(group)

        raise NotImplementedError(
            f'Operator "{ctx.operator.txt}" is not implemented.'
        )

    def visitGroup(self, ctx: ExpressionsParser.GroupContext):
        return self.visit(ctx.content)

    def visitLiteral(self, ctx: ExpressionsParser.LiteralContext):
        try:
            return self.literals[ctx.value.type]
        except KeyError:
            raise NotImplementedError(
                f'Unknown literal: "{ctx.value.text}" at '
                f'{self.__get_position(ctx)}.'
            )


class _ErrorListener(antlr4.error.ErrorListener.ErrorListener):
    def syntaxError(self, _, __, line, column, ___, ____):
        raise ExpressionSyntaxError(f'Syntax error at {line}:{column}.')


def evaluate(
    expression: str,
    variables: Dict[str, bool],
    default: bool = None
) -> bool:
    """Evaluate 'expression' with provided 'variables'.

    If 'default' is provided it will substitute values of unknown variables.
    """
    error_listener = _ErrorListener()
    lexer = ExpressionsLexer(antlr4.InputStream(expression))
    lexer.removeErrorListeners()
    lexer.addErrorListener(error_listener)
    stream = antlr4.CommonTokenStream(lexer)
    parser = ExpressionsParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)
    tree = parser.root()
    visitor = _ExpressionsVisitor(
        variables=variables,
        literals={parser.TRUE: True, parser.FALSE: False},
        default=default
    )

    return visitor.visit(tree)


def get_variables(expression: str) -> Set[str]:
    """Returns variables used in the 'expression'."""
    error_listener = _ErrorListener()
    lexer = ExpressionsLexer(antlr4.InputStream(expression))
    lexer.removeErrorListeners()
    lexer.addErrorListener(error_listener)
    variables = set()
    for token in lexer.getAllTokens():
        if token.type == ExpressionsLexer.IDENTIFIER:
            variables.add(token.text)
    return variables
