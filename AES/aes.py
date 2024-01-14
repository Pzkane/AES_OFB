from .schedule_key import get_array_grid, schedule_key, get_round_key
from .add_round_key import add_round_key
from .s_box import substitute
from .shift_rows import shift_rows
from .mix_columns import mix_columns

def encrypt(key, data):
    # Initialize padding with \x00 and break it into blocks of 16
    pad = bytes(16 - len(data) % 16)
    print("PADDING: ", pad, len(data))
    
    # Apply padding to the data
    if len(pad) != 16:
        data += pad
    grids = get_array_grid(data)

    # Expand the key for multiple rounds: "AES uses up to rcon10 for AES-128 (as 11 round keys are needed)"
    # https://en.wikipedia.org/wiki/AES_key_schedule
    expanded_key = schedule_key(key, 11)

    # Apply the original key
    temp_grids = []
    round_key = get_round_key(expanded_key, 0)
    print("RK[0]:", round_key, expanded_key)

    # Add first round key K0
    for grid in grids:
        temp_grids.append(add_round_key(grid, round_key))

    grids = temp_grids
    print("Streamed grids:", grids)

    # Go through encryption rounds
    # FIPS-197
    # Iterate from 1st to 9th round
    for round in range(1, 10):
        temp_grids = []
        round_key = get_round_key(expanded_key, round)
        
        print("GRID len: ",len(grids))
        for grid in grids:
            # Substitute bytes
            sub_bytes_step = [[substitute(val) for val in row] for row in grid]
            print(sub_bytes_step)
            # Shift rows
            shift_rows_step = [shift_rows(
                sub_bytes_step[i], i) for i in range(4)]
            # Mix columns
            mix_column_step = mix_columns(shift_rows_step)
            # Add round key
            print("ROUND:", round, "KEY:", round_key)
            add_round_key_step = add_round_key(mix_column_step, round_key)
            temp_grids.append(add_round_key_step)

        grids = temp_grids

    # Final round without mix columns
    temp_grids = []
    round_key = get_round_key(expanded_key, 10)

    for grid in grids:
        # Substitute bytes
        sub_bytes_step = [[substitute(val) for val in row] for row in grid]
        # Shift rows
        shift_rows_step = [shift_rows(
            sub_bytes_step[i], i) for i in range(4)]
        # Add round key
        add_round_key_step = add_round_key(shift_rows_step, round_key)
        temp_grids.append(add_round_key_step)

    grids = temp_grids

    # Assemble into single array
    int_grid = []
    
    for grid in grids:
        for column in range(4):
            for row in range(4):
                int_grid.append(grid[row][column])

    return bytes(int_grid)