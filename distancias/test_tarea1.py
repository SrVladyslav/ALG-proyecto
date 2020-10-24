import numpy as np

def dp_levenshtein_backwards(x, y):
    M = np.zeros((len(x) + 1, len(y) + 1))
    for i in range(1, len(x) + 1):
        M[i, 0] = i
    for j in range(1, len(y) + 1):
        M[0, j] = j
    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            if x[i - 1] == y[j - 1]:
                M[i, j] = min(M[i - 1, j] + 1, M[i, j - 1] + 1, M[i-1][j-1])
            else:
                M[i, j] = min(M[i - 1, j] + 1, M[i, j - 1] + 1, M[i-1][j-1] + 1)
    return M[len(x), len(y)]

def dp_restricted_damerau_backwards(x, y):
    M = np.zeros((len(x) + 1, len(y) + 1))
    for i in range(1, len(x) + 1):
        M[i, 0] = i
    for j in range(1, len(y) + 1):
        M[0, j] = j
    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            if i > 1 and j > 1 and x[i - 2] == y[j - 1] and x[i - 1] == y[j - 2]:
                if x[i - 1] == y[j - 1]:
                    M[i, j] = min(M[i - 1, j] + 1, M[i, j - 1] + 1, M[i-1][j-1], M[i-2][j-2] + 1)
                else:
                    M[i, j] = min(M[i - 1, j] + 1, M[i, j - 1] + 1, M[i-1][j-1] + 1, M[i-2][j-2] + 1)
            else:
                if x[i - 1] == y[j - 1]:
                    M[i, j] = min(M[i - 1, j] + 1, M[i, j - 1] + 1, M[i-1][j-1])
                else:
                    M[i, j] = min(M[i - 1, j] + 1, M[i, j - 1] + 1, M[i-1][j-1] + 1)
    return M[len(x), len(y)]

def dp_intermediate_damerau_backwards(x, y):
    M = np.zeros((len(x) + 1, len(y) + 1))
    for i in range(1, len(x) + 1):
        M[i, 0] = i
    for j in range(1, len(y) + 1):
        M[0, j] = j
    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            minInit = 0
            if x[i - 1] == y[j - 1]:
                minInit = min(M[i-1, j] + 1, M[i, j-1] + 1, M[i-1][j-1])
            else:
                minInit = min(M[i-1, j] + 1, M[i, j-1] + 1, M[i-1][j-1] + 1)

            if j > 1 and i > 1 and x[i - 2] == y[j - 1] and x[i - 1] == y[j - 2]:
                M[i,j] = min(minInit, M[i-2][j-2] + 1)
            elif j > 2 and i > 1 and x[i-2] == y[j-1] and x[i-1] == y[j-3]:
                M[i,j] = min(minInit, M[i-2][j-3] + 2)
            elif i > 2 and j > 1 and x[i - 3] == y[j-1] and x[i-1] == y[j-2]:
                M[i,j] = min(minInit, M[i-3][j-2] + 2)
            else:
                M[i,j] = minInit
    return M[len(x), len(y)]

test = [("algoritmo","algortimo"),
        ("algoritmo","algortximo"),
        ("algoritmo","lagortimo"),
        ("algoritmo","agaloritom"),
        ("algoritmo","algormio"),
        ("acb","ba")]

for x,y in test:
    print(f"{x:12} {y:12}",end="")
    for dist,name in ((dp_levenshtein_backwards,"levenshtein"),
                      (dp_restricted_damerau_backwards,"restricted"),
                      (dp_intermediate_damerau_backwards,"intermediate")):
        print(f" {name} {dist(x,y):2}",end="")
    print()
                 
"""
Salida del programa:

algoritmo    algortimo    levenshtein  2 restricted  1 intermediate  1
algoritmo    algortximo   levenshtein  3 restricted  3 intermediate  2
algoritmo    lagortimo    levenshtein  4 restricted  2 intermediate  2
algoritmo    agaloritom   levenshtein  5 restricted  4 intermediate  3
algoritmo    algormio     levenshtein  3 restricted  3 intermediate  2
acb          ba           levenshtein  3 restricted  3 intermediate  2
"""         
