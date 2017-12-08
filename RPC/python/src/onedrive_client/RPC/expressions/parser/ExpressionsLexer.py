# Generated from Expressions.g4 by ANTLR 4.7
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\13")
        buf.write("=\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\3\2\3\2\3\3\3\3\3\4\3\4\3\4\3")
        buf.write("\4\3\4\3\5\3\5\3\5\3\5\3\5\3\5\3\6\3\6\3\6\3\6\3\7\3\7")
        buf.write("\3\7\3\b\3\b\3\b\3\b\3\t\3\t\7\t\62\n\t\f\t\16\t\65\13")
        buf.write("\t\3\n\6\n8\n\n\r\n\16\n9\3\n\3\n\2\2\13\3\3\5\4\7\5\t")
        buf.write("\6\13\7\r\b\17\t\21\n\23\13\3\2\5\5\2C\\aac|\6\2\62;C")
        buf.write("\\aac|\5\2\13\f\17\17\"\"\2>\2\3\3\2\2\2\2\5\3\2\2\2\2")
        buf.write("\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3")
        buf.write("\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\3\25\3\2\2\2\5\27\3\2")
        buf.write("\2\2\7\31\3\2\2\2\t\36\3\2\2\2\13$\3\2\2\2\r(\3\2\2\2")
        buf.write("\17+\3\2\2\2\21/\3\2\2\2\23\67\3\2\2\2\25\26\7*\2\2\26")
        buf.write("\4\3\2\2\2\27\30\7+\2\2\30\6\3\2\2\2\31\32\7v\2\2\32\33")
        buf.write("\7t\2\2\33\34\7w\2\2\34\35\7g\2\2\35\b\3\2\2\2\36\37\7")
        buf.write("h\2\2\37 \7c\2\2 !\7n\2\2!\"\7u\2\2\"#\7g\2\2#\n\3\2\2")
        buf.write("\2$%\7c\2\2%&\7p\2\2&\'\7f\2\2\'\f\3\2\2\2()\7q\2\2)*")
        buf.write("\7t\2\2*\16\3\2\2\2+,\7p\2\2,-\7q\2\2-.\7v\2\2.\20\3\2")
        buf.write("\2\2/\63\t\2\2\2\60\62\t\3\2\2\61\60\3\2\2\2\62\65\3\2")
        buf.write("\2\2\63\61\3\2\2\2\63\64\3\2\2\2\64\22\3\2\2\2\65\63\3")
        buf.write("\2\2\2\668\t\4\2\2\67\66\3\2\2\289\3\2\2\29\67\3\2\2\2")
        buf.write("9:\3\2\2\2:;\3\2\2\2;<\b\n\2\2<\24\3\2\2\2\5\2\639\3\b")
        buf.write("\2\2")
        return buf.getvalue()


class ExpressionsLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    GROUP_START = 1
    GROUP_END = 2
    TRUE = 3
    FALSE = 4
    AND = 5
    OR = 6
    NOT = 7
    IDENTIFIER = 8
    WS = 9

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'('", "')'", "'true'", "'false'", "'and'", "'or'", "'not'" ]

    symbolicNames = [ "<INVALID>",
            "GROUP_START", "GROUP_END", "TRUE", "FALSE", "AND", "OR", "NOT", 
            "IDENTIFIER", "WS" ]

    ruleNames = [ "GROUP_START", "GROUP_END", "TRUE", "FALSE", "AND", "OR", 
                  "NOT", "IDENTIFIER", "WS" ]

    grammarFileName = "Expressions.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None

