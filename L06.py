from liblet import Grammar, Production, closure, union_of

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