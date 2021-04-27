from liblet import Table, HASH, ε, closure, suffixes

def compute_εfirst(G):

    FIRST = Table(1, element = set) # questo significa che gli elementi dell tabella sono insiemi

    # per prima cosa, il caso banele
    for t in G.T: FIRST[(t, )] = {t} # attenzione, gli indici sono forme sentenziali, ossia tuple!

    # qualche caso "extra" che ci verrà comodo poi
    FIRST[tuple()] = {ε}
    FIRST[(ε, )] = {ε}
    FIRST[(HASH, )] = {HASH}

    @closure
    def update_with_suffixes(FIRST):
        for N, α in G.P:
            FIRST[(N, )] |= FIRST[α]
            for γ in suffixes(α):
                A, *β = γ
                FIRST[γ] |= FIRST[(A, )] - {ε}
                if ε in FIRST[(A, )]: FIRST[γ] |= FIRST[β]
        return FIRST

    return update_with_suffixes(FIRST)

def make_first_function(G):

    FIRST = compute_εfirst(G)

    def FIRSTf(ω):
        if not ω: return {ε}
        X, *γ = ω
        fx = FIRST[(X, )]
        if ε in fx:
            return (fx - {ε}) | FIRSTf(γ)
        else:
            return fx

    return FIRSTf