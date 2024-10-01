grammar SimpleDSL;

prog: stat+ ;

stat: assignStat
    | printStat
    ;

assignStat: ID '=' expr ';' # AssignStatement
          ;

printStat: 'print' expr ';' # PrintStatement
         ;

expr: expr op=('*'|'/') expr # MulDivExpr
    | expr op=('+'|'-') expr # AddSubExpr
    | INT                    # IntExpr
    | ID                     # IdExpr
    ;

ID: [a-zA-Z]+ ;
INT: [0-9]+ ;
WS: [ \t\r\n]+ -> skip ;