from liblet import (
  Grammar, Production, Derivation, ProductionGraph, CYKTable, closure, union_of, ε
)

def remove_unproductive_unreachable(G):
  def find_productive(G):
    @closure
    def find(prod):
      return prod | {A for A, α in G.P if set(α) <= prod}
    return find(G.T)
  def find_reachable(G):
    @closure
    def find(reach):
      return reach | union_of(set(α) for A, α in G.P if A in reach)
    return find({G.S})
  Gp = G.restrict_to(find_productive(G))
  return Gp.restrict_to(find_reachable(Gp))

def cyk(G, INPUT):
  def fill(R, i, l):
    res = set()
    if l == 1:
      for A, (a,) in filter(Production.such_that(rhs_len = 1), G.P):
        if a == INPUT[i - 1]: res.add(A)
    else:
      for k in range(1, l):
        for A, (B, C) in filter(Production.such_that(rhs_len = 2), G.P):
          if B in R[i, k] and C in R[i + k, l - k]: res.add(A)
    return res
  R = CYKTable()
  for l in range(1, len(INPUT) + 1):
    for i in range(1, len(INPUT) - l + 2):
      R[i, l] = fill(R, i, l)
  return R


def eliminate_ε_rules(G):

  @closure
  def replace_in_rhs(G, A):
    Ap = A + '′'
    prods = set()
    for B, β in G.P:
      if A in β:
        pos = β.index(A)
        rhs = β[:pos] + β[pos + 1:]
        if len(rhs) == 0: rhs = (ε, )
        prods.add(Production(B, rhs))
        prods.add(Production(B, β[:pos] + (Ap, ) + β[pos + 1:]))
      else:
        prods.add(Production(B, β))
    return Grammar(G.N | {Ap}, G.T, prods, G.S)

  @closure
  def inline_ε_rules(G_seen):
    G, seen = G_seen
    for A in G.N - seen:
      if (ε, ) in G.alternatives(A):
        return replace_in_rhs(G, A), seen | {A}
    return G, seen

  Gp, _ = inline_ε_rules((G, set()))
  prods = set(Gp.P)
  for Ap in Gp.N - G.N:
    A = Ap[:-1]
    for α in set(Gp.alternatives(A)) - {(ε, )}:
      prods.add(Production(Ap, α))
  return Grammar(Gp.N, Gp.T, prods, Gp.S)


def eliminate_unit_rules(G):
  @closure
  def eliminate(G_seen):
    G, seen = G_seen
    for P in set(filter(Production.such_that(rhs_len = 1), G.P)) - seen:
      A, (B, ) = P
      if B in G.N:
        prods = (set(G.P) | {Production(A, α) for α in G.alternatives(B)}) - {P}
        return Grammar(G.N, G.T, prods, G.S), seen | {P}
    return G, seen
  return eliminate((G, set()))[0]

def transform_nonsolitary(G):
  prods = set()
  for A, α in G.P:
    prods.add(Production(A, [f'N{x}' if x in G.T else x for x in α] if len(α) > 1 else α))
    prods |= {Production(f'N{x}', (x, )) for x in α if x in G.T and len(α) > 1}
  return Grammar(G.N | {A for A, α in prods}, G.T, prods, G.S)

def make_binary(G):
  prods = set()
  for A, α in G.P:
    if len(α) > 2:
      Ai = f'{A}{1}'
      prods.add(Production(Ai, α[:2]))
      for i, Xi in enumerate(α[2:-1], 2):
          prods.add(Production(f'{A}{i}', (Ai, Xi)))
          Ai = f'{A}{i}'
      prods.add(Production(A, (Ai, α[-1])))
    else:
      prods.add(Production(A, α))
  return Grammar(G.N | {A for A, α in prods}, G.T, prods, G.S)

