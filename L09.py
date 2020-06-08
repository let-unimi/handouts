from liblet import Grammar, Production, closure, union_of

# Da L05.ipynb (regole/simboli produttivi e raggiungibili, Sez. 2.9.5.1-2)

def find_productive(G):
    @closure
    def find(prod):
        return prod | {A for A, β in G.P if set(β) <= prod}
    return set(find(G.T))

def find_reachable(G):
    @closure
    def find(reach, G):
        return reach | union_of(set(β) for A, β in G.P if A in reach)
    return find({G.S}, G)

def remove_unproductive_unreachable(G):
    Gp = G.restrict_to(find_productive(G))
    return Gp.restrict_to(find_reachable(Gp))

# Da L08.ipynb

def cyk(G, INPUT):
    def fill(R, i, l):
        res = set()
        if l == 1:
            for (A, (a, *α)) in G.P:
                if not α and a == INPUT[i - 1]:
                    res.add(A)
        else:
            for k in range(1, l):
                for A, α in G.P:
                    if len(α) != 2: continue
                    B, C = α
                    if B in R[(i, k)] and C in R[(i + k, l - k)]:
                        res.add(A)
        return res
    R = {}
    for l in range(1, len(INPUT) + 1):
        for i in range(1, len(INPUT) - l + 2):
            R[(i, l)] = fill(R, i, l)
    return R

# Da L09.ipynb (utili per homework e soluzione)

def eliminate_ε_rules(G):
    @closure
    def replace_in_rhs(G, A):
        Ap = A + '’'
        prods = set()
        for B, β in G.P:
            if A in β:
                pos = β.index(A)
                rhs = β[:pos] + β[pos + 1:]
                if len(rhs) == 0: rhs = ('ε', )
                prods.add(Production(B, rhs))
                prods.add(Production(B, β[:pos] + (Ap, ) + β[pos + 1:]))
            else:
                prods.add(Production(B, β))
        return Grammar(G.N | {Ap}, G.T, prods, G.S)
    @closure
    def inline_ε_rules(G_seen):
        G, seen = G_seen
        for A in G.N - seen:
            if ('ε', ) in G.alternatives(A):
                return replace_in_rhs(G, A), seen | {A}
        return G, seen
    Gp, _ = inline_ε_rules((G, set()))
    prods = set(Gp.P)
    for Ap in Gp.N - G.N:
        A = Ap[:-1]
        for α in set(Gp.alternatives(A)) - {('ε', )}:
            prods.add(Production(Ap, α))
    return Grammar(Gp.N, Gp.T, prods, Gp.S)

def eliminate_unit_rules(G):
    @closure
    def _eliminate_unit_rules(G_seen):
        G, seen = G_seen
        for P in set(filter(Production.such_that(rhs_len = 1), G.P)) - seen:
            A, (B, ) = P
            if B in G.N:
                prods = (set(G.P) | {Production(A, α) for α in G.alternatives(B)}) - {P}
                return Grammar(G.N, G.T, prods, G.S), seen | {P}
        return G, seen
    return _eliminate_unit_rules((G, set()))[0]

def transform_nonsolitary(G):
    prods = set()
    for A, α in G.P:
        if len(α) > 1 and set(α) & G.T:
            rhs = []
            for x in α:
                if x in G.T:
                    N = 'N{}'.format(x)
                    prods.add(Production(N, (x, )))
                    rhs.append(N)
                else:
                    rhs.append(x)
            prods.add(Production(A, rhs))
        else:
            prods.add(Production(A, α))
    return Grammar(G.N | {A for A, α in prods}, G.T, prods, G.S)

def make_binary(G):
    prods = set()
    for A, α in G.P:
        if len(α) > 2:
            Ai = '{}{}'.format(A, 1)
            prods.add(Production(Ai, α[:2]))
            for i, Xi in enumerate(α[2:-1], 2):
                prods.add(Production('{}{}'.format(A, i), (Ai, Xi)))
                Ai = '{}{}'.format(A, i)
            prods.add(Production(A, (Ai, α[-1])))
        else:
            prods.add(Production(A, α))
    return Grammar(G.N | {A for A, α in prods}, G.T, prods, G.S)

def to_cnf(G):
    Gp = eliminate_unit_rules(eliminate_ε_rules(G))
    Gp_clean = remove_unproductive_unreachable(Gp)
    return make_binary(transform_nonsolitary(Gp_clean))