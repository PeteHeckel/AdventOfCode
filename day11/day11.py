import sys
from pathlib import PosixPath

def find_galaxy_dist( coords1:list, coords2:list ):
    return abs(coords1[0] - coords2[0]) + abs(coords1[1] - coords2[1])

def find_galaxy_path_sum( galaxy_map_file: str):
    with open(galaxy_map_file) as f:
        galaxy_map = f.read().split()

    empty_rows = []
    empty_columns = [True] * len(galaxy_map[0])
    galaxys = []

    for y_idx, line in enumerate(galaxy_map, start=1):
        galaxy_found = False
        for x_idx, char in enumerate(line.strip()):
            if char == '#':
                galaxy_found = True
                empty_columns[x_idx] = False
                galaxys.append([x_idx, y_idx])
        if not galaxy_found:
            empty_rows.append(y_idx)

    empty_columns = [i for i in range(len(empty_columns)) if empty_columns[i]]
    
    for extra_cols, empty_col in enumerate(empty_columns):
        for galaxy in galaxys:
            if galaxy[0] > empty_col + extra_cols:
                galaxy[0] += 1

    for extra_rows, empty_row in enumerate(empty_rows):
        for galaxy in galaxys:
            if galaxy[1] > empty_row + extra_rows:
                galaxy[1] += 1

    distance_sum = 0
    for idx in range(len(galaxys)):
        ref_galaxy = galaxys[idx]
        for galaxy in galaxys[idx:]:
            distance_sum += find_galaxy_dist(ref_galaxy, galaxy)

    print(f'Total sum of distances between galaxies: {distance_sum}')

if __name__ == '__main__':
    if (len(sys.argv) != 2) or not PosixPath(sys.argv[1]).is_file() :
        print('Error 1 file argument needed')
        exit(1)

    find_galaxy_path_sum(sys.argv[1])

    exit(0)
