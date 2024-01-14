from .shift_rows import *
from .s_box import substitute

def get_array_grid(s):
    """ Convert bytes to integer representation in grid-like pattern.

    Example:
    b'0123456789abcdef' => [
        [
            [48, 52, 56, 99],
            [49, 53, 57, 100],
            [50, 54, 97, 101],
            [51, 55, 98, 102]
        ]
    ]

    """
    # print("get_array_grid:")
    all = []
    for i in range(len(s)//16):
        # Offset
        b = s[i*16: i*16 + 16]
        print(b)
        grid = [[], [], [], []]
        for i in range(4):
            for j in range(4):
                grid[i].append(b[i + j*4])
        all.append(grid)
    # print("RESULT(get_array_grid):", s, all)
    return all

def schedule_key(key, rounds):
    # Generate key for each round
    # Will produce continuous stream, use 'get_round_key' to get key at position

    # Initialize with first constant
    rcon = [[1, 0, 0, 0]]

    # Generate all other polynomials
    # https://en.wikipedia.org/wiki/AES_key_schedule : Round constants
    for _ in range(1, rounds):
        print("RCONp:", rcon)
        rcon.append([rcon[-1][0]*2, 0, 0, 0])
        print("RCONi:", rcon)

        if rcon[-1][0] > 0x80:
            rcon[-1][0] ^= 0x11b
    print("RCON:", rcon)

    key_grid = get_array_grid(key)[0]
    print("KEY_GRIDbefore:", key_grid)

    # FIPS-197 key expansion
    for round in range(rounds):
        last_column = [row[-1] for row in key_grid]
        last_column_rotate_step = shift_rows(last_column)
        last_column_sbox_step = [substitute(b) for b in last_column_rotate_step]
        last_column_rcon_step = [last_column_sbox_step[i]
                                 ^ rcon[round][i] for i in range(len(last_column_rotate_step))]

        for r in range(4):
            key_grid[r] += bytes([last_column_rcon_step[r]
                                  ^ key_grid[r][round*4]])

        # print("3 columns to go", key_grid)
        for i in range(len(key_grid)):
            for j in range(1, 4):
                key_grid[i] += bytes([key_grid[i][round*4+j]
                                      ^ key_grid[i][round*4+j+3]])
        # print("3 columns done:", key_grid)
                
    print("KEY_GRIDafter:", key_grid)
    return key_grid

def get_round_key(expanded_key, round):
    # Return key with offset
    return [row[round*4: round*4 + 4] for row in expanded_key]