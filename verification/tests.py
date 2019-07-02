"""
TESTS is a dict with all you tests.
Keys for this will be categories' names.
Each test is dict with
    "input" -- input data for user function
    "answer" -- your right answer
    "explanation" -- not necessary key, it's using for additional info in animation.
"""

from string import ascii_uppercase as au
from random import sample, randint, choice


def hexagonal_islands_make_random_tests(num):

    all_hexes = {c+str(r) for c in au[:12] for r in range(1, 10)}

    def adjacent_hexes(tgt_hex):
        col, row = tgt_hex[0], int(tgt_hex[1])
        col_idx = au.index(col)
        u_row = row - (1 - col_idx % 2)
        b_row = row + col_idx % 2
        n = col+str(row-1)
        s = col+str(row+1)
        nw = au[col_idx-1]+str(u_row)
        sw = au[col_idx-1]+str(b_row)
        ne = au[col_idx+1]+str(u_row)
        se = au[col_idx+1]+str(b_row)
        adj_hexes = (n, ne, se, s, sw, nw)
        return set(map(lambda h: h if h in all_hexes else None, adj_hexes))

    def make_island(rest_hexes):
        next_hexes = {choice(list(rest_hexes))}
        done_hexes = next_hexes
        while next_hexes:
            search_hexes = next_hexes
            next_hexes = set()
            for sx in search_hexes:
                adj_hexes = (adjacent_hexes(sx)-{None}) & rest_hexes
                next_hexes |= set(sample(adj_hexes,
                                    randint(0, min(3, len(adj_hexes)))))
            next_hexes -= done_hexes
            done_hexes |= next_hexes
        adj_sea_hexes = set()
        shore_hexes = set()
        for dx in done_hexes:
            adj_hexes = adjacent_hexes(dx)
            adj_sea_hexes |= adj_hexes-{None}-done_hexes
            if adj_hexes - done_hexes:
                shore_hexes.add(dx)
        return done_hexes, shore_hexes, adj_sea_hexes

    def check_hole(shore_hexes):
        rest_hexes = set(shore_hexes)
        while rest_hexes:
            start_hex = rest_hexes.pop()
            done_hexes = {start_hex}
            next_hexes = {start_hex}
            sea = False
            while next_hexes:
                search_hexes = next_hexes
                next_hexes = set()
                for s in search_hexes:
                    adj_hexes = adjacent_hexes(s)
                    if None in adj_hexes:
                        sea = True
                    next_hexes |= (adjacent_hexes(s) - {None}) & shore_hexes
                next_hexes -= done_hexes
                done_hexes |= next_hexes
            if not sea and len(shore_hexes - done_hexes) > 0:
                return False
            rest_hexes -= done_hexes
        return True

    random_tests = []
    for _ in range(num):
        rest_hexes = set(all_hexes)
        coasts = []
        answer = []
        inlands = []
        for _ in range(randint(1, 10)):
            while True:
                land, shore, adj_sea = make_island(rest_hexes)
                if check_hole(adj_sea):
                    rest_hexes -= land | adj_sea
                    coasts += list(shore)
                    answer.append(len(land))
                    inlands += list(land - shore)
                    break
            if not rest_hexes:
                break
        random_tests.append({'input': coasts,
                             'answer': sorted(answer),
                             'explanation': inlands})
    return random_tests


TESTS = {
    "Randoms": hexagonal_islands_make_random_tests(10),
    "Basics": [
        {
            'input': ['C5', 'E5', 'F4', 'F5', 'H4',
                        'H5','I4', 'I6', 'J4', 'J5'],
            'answer': [1, 3, 7],
            'explanation': ['I5'],
        },
        {
            'input': ['A1', 'A2', 'A3', 'A4', 'B1', 'B4', 'C2', 'C5',
                        'D2','D3', 'D4', 'D5',
                        'H6', 'H7', 'H8', 'I6', 'I9', 'J5', 'J9',
                        'K6', 'K9', 'L6', 'L7', 'L8'],
            'answer': [16, 19],
            'explanation': ['B2', 'B3', 'C3', 'C4',
                            'I7', 'I8', 'J6', 'J7', 'J8', 'K7', 'K8'],
        },
    ],
    "Extra": [
        {
            'input': ['A1', 'A4', 'A5', 'A9', 'B1', 'B2', 'B8', 'C3', 'C4',
                      'C5', 'C6', 'C8', 'D1', 'D3', 'D6', 'D7', 'E3', 'E5',
                      'E7', 'F1', 'F3', 'F5', 'F7', 'G2', 'G4', 'G6', 'G8',
                      'H2', 'H4', 'H8', 'I3', 'I7', 'I8', 'J2', 'J3', 'J4',
                      'J5', 'J6', 'J8', 'K2', 'K5', 'K7', 'K8', 'K9', 'L1',
                      'L5', 'L6', 'L9'],
            'answer': [1, 2, 3, 44],
            'explanation': ['J7', 'K6'],
        },
        {
            'input': ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                      'B1', 'B9', 'C1', 'C9', 'D1', 'D9', 'E1', 'E9', 'F1',
                      'F9', 'G1', 'G9', 'H1', 'H9', 'I1', 'I9', 'J1', 'J9',
                      'K1', 'K9', 'L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7',
                      'L8', 'L9'],
            'answer': [108],
            'explanation': ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'C2',
                            'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'D2', 'D3',
                            'D4', 'D5', 'D6', 'D7', 'D8', 'E2', 'E3', 'E4',
                            'E5', 'E6', 'E7', 'E8', 'F2', 'F3', 'F4', 'F5',
                            'F6', 'F7', 'F8', 'G2', 'G3', 'G4', 'G5', 'G6',
                            'G7', 'G8', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7',
                            'H8', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8',
                            'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'K2',
                            'K3', 'K4', 'K5', 'K6', 'K7', 'K8'],
        },
    ],
}
