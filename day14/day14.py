from itertools import count
import sys
from pathlib import PosixPath

def transpose_map( l: list ):
    return list(map(list, zip(*l)))

def tilt_platform( platform_map: list ):
    row_organized_map = transpose_map(platform_map)
    
    for tilting_row in row_organized_map:
        empty_tile = 0
        previous_square = '.'
        for place, square in enumerate(tilting_row):
            # print(tilting_row)
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

    return transpose_map(row_organized_map)


if __name__ == '__main__':
    if (len(sys.argv) != 2) or not PosixPath(sys.argv[1]).is_file() :
        print('Error 1 file argument needed')
        exit(1)

    with open(sys.argv[1],'r') as f:
        initial_platform = f.readlines()

    initial_platform = [list(row.strip()) for row in initial_platform]

    tilted_map = tilt_platform(initial_platform)

    load = 0
    for platform_distance, platform_row in enumerate(reversed(tilted_map), start=1):
        rock_count = len([square_val for square_val in platform_row if square_val == 'O'])
        load += rock_count * platform_distance
    
    print(f'Total Load is {load}')
    exit(0)
