def add_round_key(block_grid, key_grid):
    r = []
    # 4 rows in the grid
    for i in range(4):
        r.append([])
        # 4 values on each row
        for j in range(4):
            r[-1].append(block_grid[i][j] ^ key_grid[i][j])
    return r