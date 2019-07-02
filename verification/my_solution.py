from string import ascii_uppercase as au


def hexagonal_islands(shores):

    all_hexes = {c+str(r) for c in au[:12] for r in range(1, 10)}

    def adjacent_hexes(tgt):
        c, r = tgt[0], int(tgt[1])
        c_num = au.index(c)
        u_r = r - (1 - c_num % 2)
        b_r = r + c_num % 2

        n = c+str(r-1)
        s = c+str(r+1)
        nw = au[c_num-1]+str(u_r)
        sw = au[c_num-1]+str(b_r)
        ne = au[c_num+1]+str(u_r)
        se = au[c_num+1]+str(b_r)

        return set(map(lambda h: h if h in all_hexes else None, (n, ne, se, s, sw, nw)))

    def search_adj_lands(start):
        done_hexes = {start}
        next_hexes = {start}
        while next_hexes:
            search_hexes = next_hexes
            next_hexes = set()
            for sx in search_hexes:
                next_hexes |= adjacent_hexes(sx) & shores
            next_hexes -= done_hexes
            done_hexes |= next_hexes
        return done_hexes

    def search_adj_hexes(start):
        done_hexes = {start}
        next_hexes = {start}
        sea = False

        while next_hexes:
            search_hexes = next_hexes
            next_hexes = set()
            for sx in search_hexes:
                adj_hexes = adjacent_hexes(sx)
                if None in adj_hexes:
                    sea = True
                next_hexes |= adj_hexes - {None} - shores
                done_hexes |= shores & adj_hexes
            next_hexes -= done_hexes
            done_hexes |= next_hexes
        return sea, done_hexes

    # islands
    islands = []
    rest_shores = set(shores)
    while rest_shores:
        tgt_hex = rest_shores.pop()
        island = search_adj_lands(tgt_hex)
        islands.append(island)
        rest_shores -= island

    # others
    rest_others = all_hexes - shores
    inland_hexes = set()
    while rest_others:
        tgt_hex = rest_others.pop()
        sea, hexes = search_adj_hexes(tgt_hex)
        if not sea:
            for i, island in enumerate(islands):
                if island & hexes:
                    inland_hexes |= hexes - shores
                    islands[i] = island | hexes
        rest_others -= hexes

    # print(sorted(map(len, islands)), inland_hexes)
    return sorted(map(len, islands)), inland_hexes


if __name__ == '__main__':
    assert sorted(hexagonal_islands({'G8', 'G9', 'H7', 'H9', 'I8', 'I9'})) == [1, 3]
