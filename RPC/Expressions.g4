/**
 * Simple boolean expression language.
 *
 * Operator precedence
 *
 *  1. not
 *  2. or
 *  3. and
 *
 * Full example:
 *
 *   A and not (B or C) or D and not E and false or true
 */
grammar Expressions;

root: expr=expression EOF ;
expression: group
          | operator=NOT expression
          | expression (operator=AND expression)+
          | expression (operator=OR expression)+
          | IDENTIFIER
          | literal
          ;
group : GROUP_START content=expression GROUP_END ;
GROUP_START : '(' ;
GROUP_END : ')' ;
literal : value=TRUE | value=FALSE ;
TRUE : 'true' ;
FALSE : 'false' ;
AND : 'and' ;
OR : 'or' ;
NOT : 'not' ;
IDENTIFIER : [a-zA-Z_][a-zA-Z0-9_]* ;
WS : [ \t\r\n]+ -> skip ;
