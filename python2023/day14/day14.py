import sys
from pathlib import PosixPath

def transpose_map( l: list ):
    return list(map(list, zip(*l)))

def tilt_platform( platform_map: list, tilt_direction: str ):

    if tilt_direction == 'N':
        row_organized_map = transpose_map(platform_map)
    elif tilt_direction == 'W':
        row_organized_map = platform_map
    elif tilt_direction == 'E':
        row_organized_map = [ list(reversed(row)) for row in platform_map ]
    elif tilt_direction == 'S':
        row_organized_map = transpose_map(platform_map)
        row_organized_map = [ list(reversed(row)) for row in row_organized_map ]
    else:
        assert(False)

    for tilting_row in row_organized_map:
        empty_tile = 0
        previous_square = '.'
        for place, square in enumerate(tilting_row):
            # 1(tilting_row)
            if square == '.':
                if previous_square != '.':
                    empty_tile = place
            elif square == 'O':
                if empty_tile is not None:
                    tilting_row[place] = '.'
                    square = '.'
                    tilting_row[empty_tile] = 'O'
                    if tilting_row[empty_tile+1] != '#':
                        empty_tile += 1

            elif square == '#':
                empty_tile = None
            else:
                assert(False)

            previous_square = square


    if tilt_direction == 'N':
        row_organized_map = transpose_map(row_organized_map)
    elif tilt_direction == 'E':
        row_organized_map = [ list(reversed(row)) for row in row_organized_map ]
    elif tilt_direction == 'S':
        row_organized_map = [ list(reversed(row)) for row in row_organized_map ]
        row_organized_map = transpose_map(row_organized_map)
    # Do nothing for W        

    return row_organized_map

def hash_platform( platform_map: list ):
    hashing_str = ''
    for row in platform_map:
        hashing_str += str(row)
    return hashing_str

if __name__ == '__main__':
    if (len(sys.argv) != 2) or not PosixPath(sys.argv[1]).is_file() :
        print('Error 1 file argument needed')
        exit(1)

    with open(sys.argv[1],'r') as f:
        initial_platform = f.readlines()

    initial_platform = [list(row.strip()) for row in initial_platform]

    tilted_map = tilt_platform(initial_platform, 'N')

    load = 0
    for platform_distance, platform_row in enumerate(reversed(tilted_map), start=1):
        rock_count = len([square_val for square_val in platform_row if square_val == 'O'])
        load += rock_count * platform_distance
    print(f'Total Load tilted north is {load}')

    # Part 2, spin cycle
    tilt_dir_cycle = ['N', 'W', 'S', 'E']
    tilted_map = initial_platform

    board_states = {}
    spin_count = 1000000000

    for i in range(spin_count):
        state = hash_platform(tilted_map)
        if board_states.get( state ) is None:
            board_states[state] = i
        else:
            # At this point we are in a defined loop. Find the loop length and then see what the output state is
            cycle_len = i - board_states[state]
            remaining_cycles = spin_count - i
            offset = remaining_cycles % cycle_len
            print(offset)
            break
    
        for tilt_dir in tilt_dir_cycle:
            tilted_map = tilt_platform(tilted_map, tilt_dir)

    for _i in range(offset):
        for tilt_dir in tilt_dir_cycle:
            tilted_map = tilt_platform(tilted_map, tilt_dir)

    load = 0
    for platform_distance, platform_row in enumerate(reversed(tilted_map), start=1):
        rock_count = len([square_val for square_val in platform_row if square_val == 'O'])
        load += rock_count * platform_distance

    print(f'Load after {spin_count} cycles is {load}')    

    exit(0)
