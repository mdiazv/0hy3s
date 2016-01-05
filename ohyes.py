import sys

def sign(x):
    return 1 if x >= 0 else -1

class Board:
    def __init__(self, f=None, b=None):
        if f:
            self.M = self.N = int(f.readline())
            self.b = [map(int, f.readline().split()) for _ in xrange(self.M)]
        elif b:
            self.M = self.N = len(b)
            self.b = b
        else:
            self.b = [
                [3, 0, 0, 0],
                [1, 0, 3, 0],
                [0, 0, 3, 0],
                [0,-1, 0, 2],
            ]
            self.M = self.N = len(self.b)
    def __len__(self):
        return self.M * self.N
    def oob(self, i, j):
        return i < 0 or j < 0 or i >= self.M or j >= self.N
    def get(self, i, j):
        return -1 if self.oob(i, j) else self.b[i][j]
    def sign(self, i, j):
        return sign(self.get(i, j))
    def set(self, i, j, v):
        self.b[i][j] = v

def gen_patterns(b, i, j):
    def gen(x, i, j, di, dj):
        if x == 0:
            return [(i+di, j+dj, -1)]
        return [(i+di, j+dj, 1)] + gen(x-1, i+di, j+dj, di, dj)
    def genall(left, up, right, down):
        return gen(left, i, j, -1, 0) + gen(up, i, j, 0, -1) + gen(right, i, j, 1, 0) + gen(down, i, j, 0, 1)

    n = b.get(i, j)
    if n < 1:
        return []

    p = []
    for left in xrange(n+1):
        for up in xrange(n+1):
            for right in xrange(n+1):
                for down in xrange(n+1):
                    if left+up+right+down == n:
                        p.append({(i, j): v for i, j, v in genall(left, up, right, down)})

    return p

def filter_patterns(b, s, patterns):
    def filter_ob(((i, j), v)):
        return v == -1 if b.oob(i, j) else True
    def filter_red((k, v)):
        return s[k] == 1 if v == 1 and k in s else True
    def filter_blue((k, v)):
        return s[k] == -1 if v == -1 and k in s else True
    def filter_all(x):
        filters = [filter_ob, filter_red, filter_blue]
        return all(map(lambda f: f(x), filters))
    def all_ok(p):
        return all(map(filter_all, p.items()))

    # keep only the ones that are ok
    f = filter(all_ok, patterns)
    # remove the tiles that are out of bounds
    return [{(i, j): v for (i, j), v in p.items() if not b.oob(i, j)} for p in f]

def and_patterns(patterns):
    def _and(p, i):
        if i >= len(patterns):
            return p
        if not p:
            return p
        px = patterns[i]
        return _and({k: v for k, v in p.items() if k in px and px[k] == v}, i+1)

    return _and(patterns[0], 1) if patterns else {}

def initial_solution(b):
    return {(i, j): b.sign(i, j) for i in xrange(b.M) for j in xrange(b.N) if b.get(i, j)}

def find_blues(b, s):
    found = {}
    for i in xrange(b.M):
        for j in xrange(b.N):
            got = and_patterns(filter_patterns(b, s, gen_patterns(b, i, j)))
            print "[{}, {}] = {}: {}".format(i, j, b.get(i, j), got)
            found.update(got)
    if found:
        print "blues: {}".format(found.items())
    return {k: v for k, v in found.items() if k not in s}

def find_reds(b, s):
    def solved(i, j):
        ps = filter_patterns(b, s, gen_patterns(b, i, j))
        return any(map(lambda p: all(map(lambda (k, v): k in s and s[k] == 1 if v == 1 else True, p.items())), ps))
    def redify(i, j):
        def go(i, j, di, dj):
            if i < 0 or j < 0 or i >= b.M or j >= b.N:
                return []
            if (i, j) in s and s[(i, j)] == 1:
                return go(i+di, j+dj, di, dj)
            return [(i, j)]
        return go(i, j, -1, 0) + go(i, j, 0, -1) + go(i, j, 1, 0) + go(i, j, 0, 1)

    reds = []
    for i in xrange(b.M):
        for j in xrange(b.N):
            if solved(i, j):
                print "[{}, {}] is solved!".format( i, j)
                reds += redify(i, j)
    return {k:-1 for k in reds if k not in s}

def astray_reds(b, s):
    def neighbors(i, j):
        return [b.sign(i-1, j), b.sign(i, j-1), b.sign(i+1, j), b.sign(i, j+1)]
    astray = {}
    for i in xrange(b.M):
        for j in xrange(b.N):
            if (i, j) not in s:
                n = neighbors(i, j)
                # red island
                if n == [-1, -1, -1, -1]:
                    astray[(i, j)] = -1
    return astray

def solve(b):
    n = 0
    oldlen = 0
    s = initial_solution(b)
    while len(s) < len(b):
        print "solution @ step {} (len {}): {}".format(n, len(s), s)
        if len(s) == oldlen:
            print "stuck after {} steps".format(n)
            print "no solution found!"
            return False

        n += 1
        oldlen = len(s)

        blues = find_blues(b, s)
        print "found {} blue dots (maybe some are red): {}".format(len(blues), blues)
        s.update(blues)

        reds = find_reds(b, s)
        print "found {} red dots: {}".format(len(reds), reds.keys())
        s.update(reds)

        astray = astray_reds(b, s)
        print "found {} astray red dots: {}".format(len(astray), astray.keys())
        s.update(astray)

        for (i, j), v in s.items():
            if v == -1:
                b.set(i, j, -1)

    print "solution found!"
    return s

def test() :
    b = Board()
    ps = gen_patterns(b, 3, 3)
    for p in ps:
        print p
    fps = filter_patterns(b, {}, ps)
    print fps
    aps = and_patterns(fps)
    print aps

def main():
    N = int(raw_input())
    for i in xrange(N):
        b = Board(f = sys.stdin)
        solve(b)

main()
