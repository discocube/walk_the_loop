"""
Utilities used by iconsian game.
"""
from collections import defaultdict
from datetime import datetime
from functools import wraps
from itertools import chain, repeat
from more_itertools import chunked
import os
import pickle
from random import sample
import time
from typing import Iterator, Iterable


_c = 0


def cp(show=False, spacing=None, label=' №', justify=0) -> int:
    """
    Increments global variable _c consecutively when called during the lifetime of executing a program regardless of scope
    """
    def count():
        """
        Inner.
        """
        global _c
        _c += 1
        if show:
            if spacing:
                if not _c % spacing:
                    print(f"{_c}_{label}") if label else print(f"{_c}")
            else:
                out = f" {label} {_c}" if label else f"{_c}"
                print(f'{out}'.rjust(justify, ' '))
        return _c
    return count()


def timed(fn):
    """
    Decorator that times a function and prints a pretty readout
    fn: function to time
    :return: fn + runtime of decorated function.
    """

    @wraps(fn)
    def inner(*args, **kwargs):
        """
        inner function with lots of emojis.
        """
        fn_name = fn.__name__.upper()
        st = time.perf_counter()
        border = '═' + ('══' * ((len(fn.__name__) + 30) // 2))
        print()
        cp(show=True)
        print(border + '╕')
        print(f' 📌 {fn_name} | 🏁 {tstamp()}\n')
        res = fn(*args, **kwargs)
        print('\n', f'🕳 {fn_name} | 🕗 {time.perf_counter() - st:.7f} secs')
        print(border + '╛', '\n')
        return res

    return inner


def tstamp(year=True) -> str:
    """
    date- and timestamper
    :return: date/time in this format: 18:21 02/06/22
    """
    ts = datetime.now().strftime('%H:%M %d/%m/%y')
    return ts if year else ts[:-3]


def ae_for_grid(x: int = None, y: int = None, z: int = None, both: bool = False):
    """
    Create adjacency and edges dict/list for 2d/3d regular grids.
    Not providing z will create a 2d grid. Setting parameter <both> to True returns both 2d/3d versions as a dict.
    """
    xy_rng = range(_xy := x * y)
    xy_grid = list(chunked(xy_rng, x))
    A, E = defaultdict(set), set()
    for iy in range(y):
        for ix in range(x):
            n = xy_grid[iy][ix]
            if all((ix, iy)) and ix < x - 1 and iy < y - 1:
                A[n] = {n + 1, n - 1, n - x, n + x}
                E.update(map(lambda ns: frozenset([n, n + ns]), (1, -1, -x, x)))
            else:
                if ix:
                    A[n].add(n - 1)
                    E.add(frozenset([n, n - 1]))
                if ix < x - 1:
                    A[n].add(n + 1)
                    E.add(frozenset([n, n + 1]))
                if iy:
                    A[n].add(n - x)
                    E.add(frozenset([n, n - x]))
                if iy < y - 1:
                    A[n].add(n + x)
                    E.add(frozenset([n, n + x]))
    if not z:
        return A, E
    A3 = {k: set() for k in range(x * y * z)}
    for m in range(_xy):
        A3[m] = {*A[m], m + _xy}
        for i in range(1, z):
            n = m + (floor := i * _xy)
            A3[n] = {x + floor for x in A[m]}.union({n - _xy} if i == z - 1 else {n - _xy, n + _xy})
    E3 = {*map(frozenset, chain.from_iterable(map(lambda k: zip(repeat(k), A[k]), A)))}
    if not both:
        return A3, E3
    return {2: (A, E), 3: (A3, E3)}


def id_seq(seq, A) -> str or bool:
    """
    Certify sequence, return sequence type broken, loop, or snake.
    """
    for s in range(1, len(seq)):
        if seq[s - 1] not in A[seq[s]]:
            return 'broken'
    if seq[0] in A[seq[-1]]:
        return 'loop'
    return 'snake'


def key_loop(loop, node=0, rev=False):
    """
    keys loop to given node
    """
    loop = list(loop)
    loop = loop[loop.index(node):] + loop[:loop.index(node)]
    if rev:
        return loop[::-1]
    return loop


def print_xy_grid(x, y):
    """
    Print out xy grid.
    """
    for row in chunked(range(x * y), x):
        print(str([f'{r:0{len(str(x * y))}d}' for r in row])
              .replace("', '", '   ')
              .replace("']", ' ')
              .replace("['", ' '), '\n')


def cc_from_a(A, both: bool = False, oddeven: bool = False):
    """
    Returns a dict mapping a node to its chromatic coloring.
    """
    odd_even = {0: {0}, 1: {*A[0]}}
    while set(A.keys()).difference(odd_even[0].union(odd_even[1])):
        for odd in odd_even[0]:
            odd_even[1].update(A[odd])
        for even in odd_even[1]:
            odd_even[0].update(A[even])
    colored_nodes = {number: key for key in odd_even.keys() for number in odd_even[key]}
    return odd_even if oddeven else colored_nodes, odd_even if both else colored_nodes


def prune_graph(A, nodes=None):
    """
    remove nodes from given adjacency
    """
    if nodes is not None:
        return {k: v.difference(nodes) for k, v in A.items() if k not in nodes}
    return A


def adj_from_edges(edges):
    """
    Adjacency list from edges.
    """
    adj = {n: set() for n in {e for edge in edges for e in edge}}
    for edge in edges:
        adj[edge[0]].add(edge[1])
        adj[edge[1]].add(edge[0])
    return adj


def unpack(nested_list) -> Iterator[int]:
    """
    Unpack (completely) a nested list into a generator
    """
    for nested in nested_list:
        if isinstance(nested, Iterable) and not isinstance(nested, (str, bytes)):
            yield from unpack(nested)
        else:
            yield nested


@timed
def walk(A, start=0, walked=None, goal=None, shuffle=True, prune=False) -> list[int]:
    """
    General brute-force play algorithm.
    """
    if prune:
        A = prune_graph(A, walked)
    if shuffle:
        A = shuffle_adj(A)
    uu: list = []
    path = [start]
    walked.add(start)
    while True:
        if nxt := set(A[path[-1]].difference(walked)):
            step = nxt.pop()
            path.append(step)
            # HERE GIVE OUT PATH
            walked.add(step)
            if nxt:
                uu += [(len(path) - 1, n) for n in nxt]
        else:
            # HERE RED TO SHOW LACK OF SUCCESS
            if uu:

                path[u[0]:] = [(u := uu.pop())[1]]
                # back tracking finished: SEND THIS TO GAME
            else:
                break
        if path[-1] == goal:
            return path


def shuffle_adj(adj):
    """
    Shuffle the values adj[node] in the dictionary and freeze it.
    """
    return {k: frozenset(sample(v, len(v))) for k, v in adj.items()}


def get_G(ORD):
    """
    Get DC graph.
    """
    fpg = os.path.join('/home/rommelo/Repos/discocube/data/graphs/dcgrid', f'g_{ORD}')
    return pickleload(fpg)


def pickleload(filename, mode='rb', raise_error=False):
    """
    Load object from a .pickle file
    """
    filename = f'{filename}.pickle' if 'pickle' not in filename else filename
    try:
        with open(filename, mode) as f:
            print(f' 📩 {filename}')
            try:
                return pickle.load(f)
            except pickle.UnpicklingError:
                print(filename)
    except EOFError:
        print(f"❌ {filename}")
        if raise_error:
            raise FileNotFoundError


def scale_vertices(vertices, scale=10):
    """
    Scale vertices according to factor
    """
    return [(a * scale, b * scale) for a, b in vertices]


def walker(A, s: tuple[int] = (0,)):
    """
    General brute-force walk algorithm.
    """
    longest_move = []
    ORD = len(A)
    uu: list = []
    loops: set = set()
    w: list = [*s]
    while True:
        time.sleep(0.1)
        yield w
        if nxt := A[w[-1]].difference(w):
            w.append(nxt.pop())
            if len(w) > len(longest_move):
                longest_move = w.copy()
            if nxt:
                uu += [(len(w) - 1, n) for n in nxt]
        else:
            if uu:
                w[u[0]:] = [(u := uu.pop())[1]]
            else:
                yield longest_move
                return
        if len(w) == ORD:
            if w[0] in A[w[-1]]:
                loops.add(tuple(w))
                print(cp() - 1, tuple(w))
                yield w


def scale_point(point, scale, intd=True):
    """
    Scale point according to scale
    """

    return [(int(p * scale) if intd else p * scale) for p in point]
