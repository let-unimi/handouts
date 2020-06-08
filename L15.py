from liblet import Table, closure, warn

def suffixes(α):
    for i in range(len(α)):
        yield α[i:]

def compute_εfirst(G):

    FIRST = Table(1, element = set) # questo significa che gli elementi dell tabella sono insiemi

    # per prima cosa, il caso banele
    for t in G.T: FIRST[(t, )] = {t} # attensione, gli indici sono forme sentenziali, ossia tuple!

    # qualche caso "extra" che ci verrà comodo poi
    FIRST[tuple()] = {'ε'}
    FIRST[('ε', )] = {'ε'}
    FIRST[('#', )] = {'#'}

    @closure
    def update_with_suffixes(FIRST):
        for N, α in G.P:
            FIRST[(N, )] |= FIRST[α]
            for γ in suffixes(α):
                A, *β = γ
                FIRST[γ] |= FIRST[(A, )] - {'ε'}
                if 'ε' in FIRST[(A, )]: FIRST[γ] |= FIRST[β]
        return FIRST

    return update_with_suffixes(FIRST)
