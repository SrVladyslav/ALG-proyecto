# -*- coding: utf-8 -*-
import sys

def langford_directo(N, allsolutions):
    N2   = 2*N
    seq  = [0]*N2
    
    def is_feasible(s):
        for n in range(1,N+1):
            if n not in s:
                return False
            i = s.index(n)
            if i+1+n >= len(s) or (i+1+n < len(s) and s[i] != s[i+1+n]):
                return False
        return True
        
    def is_complete(s):
        result = True
        for n in s:
            if n == 0:
                result = False
                break
        return result
        
    def branch(s):
        result = []
        i = s.index(0)
        for n in range(N,0,-1):
            if n not in s:
                result.append((n, i, i+1+n))
        return result
    
    def backtrack(s):
        if is_complete(s):
            if is_feasible(s):
                return [s]
        else:
            result = None
            for p in branch(s):
                if p[1] < len(s) and p[2] < len(s) and s[p[1]] == 0 and s[p[2]] == 0:
                    sa = s.copy()
                    sa[p[1]] = p[0]
                    sa[p[2]] = p[0]
                    r = backtrack(sa)
                    if r != None:
                        if result == None: result = []
                        result.extend(r)
            return result
    
    def backtracking(num):
        if num<=0:
            yield "-".join(map(str, seq))
        else:
	    # COMPLETAR
            for s in backtrack(seq):
                yield s

    if N%4 not in (0,3):
        yield "no hay solucion"
    else:
        count = 0
        for s in backtracking(N):
            count += 1
            yield "solution %04d -> %s" % (count, s)
            if not allsolutions:
                break

# http://www.cs.mcgill.ca/~aassaf9/python/algorithm_x.html
def select(X, Y, r):
    cols = []
    for j in Y[r]:
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].remove(i)
        cols.append(X.pop(j))
    return cols

def deselect(X, Y, r, cols):
    for j in reversed(Y[r]):
        X[j] = cols.pop()
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)

def solve(X, Y, solution=[]):
    if not X:
        yield list(solution)
    else:
        c = min(X, key=lambda c: len(X[c]))
        for r in list(X[c]):
            solution.append(r)
            cols = select(X, Y, r)
            for s in solve(X, Y, solution):
                yield s
            deselect(X, Y, r, cols)
            solution.pop()

def langford_data_structure(N):
    # n1,n2,... means that the value has been used
    # p1,p2,... means that the position has been used
    def value(i):
        return sys.intern('n%d' % (i,))
    def position(i):
        return sys.intern('p%d' % (i,))

    X = set([value(i) for i in range(1,N+1)]+[position(i) for i in range(2*N)])
    Y = {}
    for v in range(1,N+1):
        # COMPLETAR
        ih = 0
        while ih+1+v < 2*N:
            Y[value(v) + position(ih)] = [value(v), position(ih), position(ih+1+v)]
            ih = ih + 1

    X = {j: set() for j in X}
    for i in Y:
        for j in Y[i]:
            X[j].add(i)

    return X, Y

def langford_exact_cover(N, allsolutions):
    if N%4 not in (0, 3):
        yield "no hay solucion"
    else:
        X,Y = langford_data_structure(N)
        sol = [None]*2*N
        count = 0
        for coversol in solve(X, Y):
            for item in coversol:
                n,p= map(int,item[1:].split('p'))
                sol[p]=n
                sol[p+n+1]=n
            count += 1
            yield "solution %04d -> %s" % (count,"-".join(map(str, sol)))
            if not allsolutions:
                break

if __name__ == "__main__":
    if len(sys.argv) not in (2, 3, 4):
        print('\nUsage: %s N [TODAS] [EXACT_COVER] \n' % (sys.argv[0],))
        sys.exit()
    try:
        N = int(sys.argv[1])
    except ValueError:
        print('First argument must be an integer')
        sys.exit()
    allSolutions = False
    langford_function = langford_directo
    for param in sys.argv[2:]:
        if param == 'TODAS':
            allSolutions = True
        elif param == 'EXACT_COVER':
            langford_function = langford_exact_cover
    for sol in langford_function(N, allSolutions):
        print(sol)

