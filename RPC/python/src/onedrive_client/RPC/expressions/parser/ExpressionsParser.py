# Generated from Expressions.g4 by ANTLR 4.7
# encoding: utf-8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys

def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\13")
        buf.write("\61\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\3\2\3\2\3\2\3\3\3")
        buf.write("\3\3\3\3\3\3\3\3\3\5\3\24\n\3\3\3\3\3\3\3\6\3\31\n\3\r")
        buf.write("\3\16\3\32\3\3\3\3\3\3\6\3 \n\3\r\3\16\3!\7\3$\n\3\f\3")
        buf.write("\16\3\'\13\3\3\4\3\4\3\4\3\4\3\5\3\5\5\5/\n\5\3\5\2\3")
        buf.write("\4\6\2\4\6\b\2\2\2\64\2\n\3\2\2\2\4\23\3\2\2\2\6(\3\2")
        buf.write("\2\2\b.\3\2\2\2\n\13\5\4\3\2\13\f\7\2\2\3\f\3\3\2\2\2")
        buf.write("\r\16\b\3\1\2\16\24\5\6\4\2\17\20\7\t\2\2\20\24\5\4\3")
        buf.write("\7\21\24\7\n\2\2\22\24\5\b\5\2\23\r\3\2\2\2\23\17\3\2")
        buf.write("\2\2\23\21\3\2\2\2\23\22\3\2\2\2\24%\3\2\2\2\25\30\f\6")
        buf.write("\2\2\26\27\7\7\2\2\27\31\5\4\3\2\30\26\3\2\2\2\31\32\3")
        buf.write("\2\2\2\32\30\3\2\2\2\32\33\3\2\2\2\33$\3\2\2\2\34\37\f")
        buf.write("\5\2\2\35\36\7\b\2\2\36 \5\4\3\2\37\35\3\2\2\2 !\3\2\2")
        buf.write("\2!\37\3\2\2\2!\"\3\2\2\2\"$\3\2\2\2#\25\3\2\2\2#\34\3")
        buf.write("\2\2\2$\'\3\2\2\2%#\3\2\2\2%&\3\2\2\2&\5\3\2\2\2\'%\3")
        buf.write("\2\2\2()\7\3\2\2)*\5\4\3\2*+\7\4\2\2+\7\3\2\2\2,/\7\5")
        buf.write("\2\2-/\7\6\2\2.,\3\2\2\2.-\3\2\2\2/\t\3\2\2\2\b\23\32")
        buf.write("!#%.")
        return buf.getvalue()


class ExpressionsParser ( Parser ):

    grammarFileName = "Expressions.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "'true'", "'false'", "'and'", 
                     "'or'", "'not'" ]

    symbolicNames = [ "<INVALID>", "GROUP_START", "GROUP_END", "TRUE", "FALSE", 
                      "AND", "OR", "NOT", "IDENTIFIER", "WS" ]

    RULE_root = 0
    RULE_expression = 1
    RULE_group = 2
    RULE_literal = 3

    ruleNames =  [ "root", "expression", "group", "literal" ]

    EOF = Token.EOF
    GROUP_START=1
    GROUP_END=2
    TRUE=3
    FALSE=4
    AND=5
    OR=6
    NOT=7
    IDENTIFIER=8
    WS=9

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class RootContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.expr = None # ExpressionContext

        def EOF(self):
            return self.getToken(ExpressionsParser.EOF, 0)

        def expression(self):
            return self.getTypedRuleContext(ExpressionsParser.ExpressionContext,0)


        def getRuleIndex(self):
            return ExpressionsParser.RULE_root

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRoot" ):
                listener.enterRoot(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRoot" ):
                listener.exitRoot(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRoot" ):
                return visitor.visitRoot(self)
            else:
                return visitor.visitChildren(self)




    def root(self):

        localctx = ExpressionsParser.RootContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_root)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 8
            localctx.expr = self.expression(0)
            self.state = 9
            self.match(ExpressionsParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ExpressionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.operator = None # Token

        def group(self):
            return self.getTypedRuleContext(ExpressionsParser.GroupContext,0)


        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ExpressionsParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(ExpressionsParser.ExpressionContext,i)


        def NOT(self):
            return self.getToken(ExpressionsParser.NOT, 0)

        def IDENTIFIER(self):
            return self.getToken(ExpressionsParser.IDENTIFIER, 0)

        def literal(self):
            return self.getTypedRuleContext(ExpressionsParser.LiteralContext,0)


        def AND(self, i:int=None):
            if i is None:
                return self.getTokens(ExpressionsParser.AND)
            else:
                return self.getToken(ExpressionsParser.AND, i)

        def OR(self, i:int=None):
            if i is None:
                return self.getTokens(ExpressionsParser.OR)
            else:
                return self.getToken(ExpressionsParser.OR, i)

        def getRuleIndex(self):
            return ExpressionsParser.RULE_expression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression" ):
                listener.enterExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression" ):
                listener.exitExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpression" ):
                return visitor.visitExpression(self)
            else:
                return visitor.visitChildren(self)



    def expression(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = ExpressionsParser.ExpressionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_expression, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 17
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ExpressionsParser.GROUP_START]:
                self.state = 12
                self.group()
                pass
            elif token in [ExpressionsParser.NOT]:
                self.state = 13
                localctx.operator = self.match(ExpressionsParser.NOT)
                self.state = 14
                self.expression(5)
                pass
            elif token in [ExpressionsParser.IDENTIFIER]:
                self.state = 15
                self.match(ExpressionsParser.IDENTIFIER)
                pass
            elif token in [ExpressionsParser.TRUE, ExpressionsParser.FALSE]:
                self.state = 16
                self.literal()
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 35
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,4,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 33
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
                    if la_ == 1:
                        localctx = ExpressionsParser.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 19
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 22 
                        self._errHandler.sync(self)
                        _alt = 1
                        while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                            if _alt == 1:
                                self.state = 20
                                localctx.operator = self.match(ExpressionsParser.AND)
                                self.state = 21
                                self.expression(0)

                            else:
                                raise NoViableAltException(self)
                            self.state = 24 
                            self._errHandler.sync(self)
                            _alt = self._interp.adaptivePredict(self._input,1,self._ctx)

                        pass

                    elif la_ == 2:
                        localctx = ExpressionsParser.ExpressionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expression)
                        self.state = 26
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 29 
                        self._errHandler.sync(self)
                        _alt = 1
                        while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                            if _alt == 1:
                                self.state = 27
                                localctx.operator = self.match(ExpressionsParser.OR)
                                self.state = 28
                                self.expression(0)

                            else:
                                raise NoViableAltException(self)
                            self.state = 31 
                            self._errHandler.sync(self)
                            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

                        pass

             
                self.state = 37
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,4,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx

    class GroupContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.content = None # ExpressionContext

        def GROUP_START(self):
            return self.getToken(ExpressionsParser.GROUP_START, 0)

        def GROUP_END(self):
            return self.getToken(ExpressionsParser.GROUP_END, 0)

        def expression(self):
            return self.getTypedRuleContext(ExpressionsParser.ExpressionContext,0)


        def getRuleIndex(self):
            return ExpressionsParser.RULE_group

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGroup" ):
                listener.enterGroup(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGroup" ):
                listener.exitGroup(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGroup" ):
                return visitor.visitGroup(self)
            else:
                return visitor.visitChildren(self)




    def group(self):

        localctx = ExpressionsParser.GroupContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_group)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 38
            self.match(ExpressionsParser.GROUP_START)
            self.state = 39
            localctx.content = self.expression(0)
            self.state = 40
            self.match(ExpressionsParser.GROUP_END)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class LiteralContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.value = None # Token

        def TRUE(self):
            return self.getToken(ExpressionsParser.TRUE, 0)

        def FALSE(self):
            return self.getToken(ExpressionsParser.FALSE, 0)

        def getRuleIndex(self):
            return ExpressionsParser.RULE_literal

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiteral" ):
                listener.enterLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiteral" ):
                listener.exitLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLiteral" ):
                return visitor.visitLiteral(self)
            else:
                return visitor.visitChildren(self)




    def literal(self):

        localctx = ExpressionsParser.LiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_literal)
        try:
            self.state = 44
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [ExpressionsParser.TRUE]:
                self.enterOuterAlt(localctx, 1)
                self.state = 42
                localctx.value = self.match(ExpressionsParser.TRUE)
                pass
            elif token in [ExpressionsParser.FALSE]:
                self.enterOuterAlt(localctx, 2)
                self.state = 43
                localctx.value = self.match(ExpressionsParser.FALSE)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[1] = self.expression_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expression_sempred(self, localctx:ExpressionContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 3)
         




