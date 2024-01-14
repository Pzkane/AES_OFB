def gmul(a, b):
    # https://stackoverflow.com/a/66137113
    if b == 1:
        return a
    tmp = (a << 1) & 0xff
    if b == 2:
        return tmp if a < 128 else tmp ^ 0x1b
    if b == 3:
        return gmul(a, 2) ^ a

def mix_columns(grid):
    new_grid = [[], [], [], []]
    for i in range(4):
        col = [grid[j][i] for j in range(4)]
        col = [
            gmul(col[0], 2) ^ gmul(col[1], 3) ^ col[2] ^ col[3],
            col[0] ^ gmul(col[1], 2) ^ gmul(col[2], 3) ^ col[3],
            col[0] ^ col[1] ^ gmul(col[2], 2) ^ gmul(col[3], 3),
            gmul(col[0], 3) ^ col[1] ^ col[2] ^ gmul(col[3], 2),
        ]
        for i in range(4):
            new_grid[i].append(col[i])
    return new_grid
