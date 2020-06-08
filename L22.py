from liblet import ANTLR, Tree

from L21 import simple2ast

# simple + block

SimpleBlockLang = ANTLR(r"""grammar SimpleBlockLang;

program: stat+ EOF;

block: '{' stat* '}' ;

expr: '!' expr            #notExpr
    | expr ('+'|'-') expr #addSubExpr
    | expr '==' expr      #equalityExpr
    | ID                  #varRefExpr
    | INT                 #intExpr
    | '(' expr ')'        #subExpr
    ;

stat: block                                 #blockStat
    | 'var' ID ('=' expr)? ';'              #varDeclStat
    | 'if' expr 'then' stat ('else' stat)?  #ifElseStat
    | 'repeat' expr 'times' stat            #repeatStat
    | ID '=' expr ';'                       #assignementStat
    ;

ID: LETTER (LETTER | [0-9])* ;
INT: [0-9]+ ;
WS: [ \t\n\r]+ -> skip ;
fragment
LETTER : [a-zA-Z] ;
""")

simpleBlock2ast = simple2ast

@simpleBlock2ast.register
def blockStat(visit, ptree):
    return visit(ptree.children[0])

@simpleBlock2ast.register
def block(visit, ptree):
    _, *stats, _ = ptree.children
    return Tree({'type': 'blockStat'}, [visit(stat) for stat in stats])

@simpleBlock2ast.register
def ifElseStat(visit, ptree):
    if len(ptree.children) == 6:
        _, cond, _, true, _, false = ptree.children
        return Tree({'type': 'ifElseStat'}, [visit(cond), visit(true), visit(false)])
    else:
        _, cond, _, true = ptree.children
        return Tree({'type': 'ifStat'}, [visit(cond), visit(true)])

@simpleBlock2ast.register
def repeatStat(visit, ptree):
    _, count, _, stat = ptree.children
    return Tree({'type': 'repeatStat'}, [visit(count), visit(stat)])

@simpleBlock2ast.register
def prodExpr(visit, ptree):
    left, _, right = ptree.children
    return Tree({'type': 'prodExpr'}, [visit(left), visit(right)])
