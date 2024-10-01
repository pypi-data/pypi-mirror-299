'''
Terminology
-----------
Literal is a pair [b, p], where 'b' is either 0 or 1 (i.e. a bit) and 'p' is just a string.
If b = 0, then [b, p] corresponds to the literal 'not p'. Otherwise it corresponds to the literal 'p'.
Term is a list of literals.
'''

def terms_match(term1, term2):
    complement_found = -1
    for i in range(len(term1)):
        if term1[i][1] != term2[i][1]:
            return -1
        elif term1[i][0] != term2[i][0]:
            if complement_found != -1:
                return -1
            else:
                complement_found = i
    return complement_found

def find_prime_implicants(terms):
    implicants = [sorted(term, key=lambda x: x[1]) for term in terms]
    prime_implicants = []
    while True:
        matches = [False] * len(implicants)
        new_implicants = []

        for i in range(len(implicants)):
            for j in range(i + 1, len(implicants)):
                result = terms_match(implicants[i], implicants[j])
                if result != -1:
                    matches[i] = True
                    matches[j] = True
                    implicant = implicants[i][:result] + implicants[i][result + 1:]
                    if not implicant in new_implicants:
                        new_implicants.append(implicant)
        
        for i in range(len(implicants)):
            if not matches[i]:
                prime_implicants.append(implicants[i])

        if len(new_implicants) == 0:
            break
        else:
            implicants = new_implicants
    return prime_implicants

def issubset(implicant, term):
    for literal in implicant:
        if literal not in term:
            return False
    return True

def find_sufficient_implicants(terms, implicants):
    sufficient_implicants = []
    local_terms = terms.copy()
    local_implicants = implicants.copy()
    
    while len(local_terms) > 0:
        best_implicant = None
        best_implicant_covered_terms = []
        for implicant in implicants:
            covered_terms = []
            for term in local_terms:
                if issubset(implicant, term):
                    covered_terms.append(term)
            if len(covered_terms) > len(best_implicant_covered_terms):
                best_implicant = implicant
                best_implicant_covered_terms = covered_terms

        sufficient_implicants.append(best_implicant)
        local_implicants.remove(best_implicant)
        for term in best_implicant_covered_terms:
            local_terms.remove(term)

    return sufficient_implicants

def minimize_dnf(terms):
    return find_sufficient_implicants(terms, find_prime_implicants(terms))