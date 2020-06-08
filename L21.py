from liblet import AnnotatedTreeWalker, Tree

simple2ast = AnnotatedTreeWalker('name')

@simple2ast.register
def intExpr(visit, ptree):
    return Tree({'type': 'intExpr', 'value': int(ptree.children[0].root['value'])})

@simple2ast.register
def addSubExpr(visit, ptree):
    left, op, right = ptree.children
    return Tree({'type': 'addSubExpr', 'op': op.root['name']}, [visit(left), visit(right)])

@simple2ast.register
def equalityExpr(visit, ptree):
    left, _, right = ptree.children
    return Tree({'type': 'equalityExpr'}, [visit(left), visit(right)])

@simple2ast.register
def varRefExpr(visit, ptree):
    return Tree({'type': 'varRefExpr', 'varName': ptree.children[0].root['value']})

@simple2ast.register
def varDeclStat(visit, ptree):
    name = ptree.children[1].root['value']
    if len(ptree.children) == 5:
        return Tree({'type': 'varDeclInitStat', 'varName': name}, [visit(ptree.children[3])])
    else:
        return Tree({'type': 'varDeclStat', 'varName': name})

@simple2ast.register
def assignementStat(visit, ptree):
    name, _, right, _ = ptree.children
    return Tree({'type': 'assignementStat', 'varName': name.root['value']}, [visit(right)])

@simple2ast.register
def repeatStat(visit, ptree):
    _, expr, _, *stats, _ = ptree.children
    return Tree({'type': 'repeatStat'}, [visit(expr)] + [visit(stat) for stat in stats])

ELSE_ROOT = {'type': 'token', 'name': 'else', 'value': 'else'}

@simple2ast.register
def ifElseStat(visit, ptree):
    _, cond, _, *stats, _ = ptree.children
    roots = [stat.root for stat in stats]
    try:
        elsePos = roots.index(ELSE_ROOT)
    except ValueError:
        elsePos = len(stats)
    return Tree({'type': 'ifElseStat', 'elsePos': elsePos},
          [visit(cond)] +
          [visit(stat) for stat in stats[:elsePos]] +
          [visit(stat) for stat in stats[elsePos + 1:]]
        )

@simple2ast.register
def program(visit, ptree):
    return Tree({'type': 'program'}, [visit(child) for child in ptree.children])
