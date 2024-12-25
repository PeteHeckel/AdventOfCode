import sys
from pathlib import PosixPath
from numpy import lcm

def find_z_in_loop( start_point:str, map_dict:dict, directions:list ):
    point = start_point
    index_count = 0
    z_points = []
    cycle_dirs = directions.copy()
    while point[-1] != 'Z':
        direction = cycle_dirs.pop(0)
        cycle_dirs.append(direction)
        index_count += 1
        point = map_dict[point][direction]
    return index_count

def find_my_way( maps_filepath: str ):
    with open(maps_filepath) as f:
        route = list(f.readline().strip())

        for i in range(len(route)):
            if route[i] == 'L':
                route[i] = 0
            elif route[i] == 'R':
                route[i] = 1
            else:
                print(f'ERROR: {route[i]}')
                assert(False)
        _throwaway = f.readline()

        map_dict = {}
        for line in f:
            entry, paths = line.split('=')
            entry = entry.strip()
            path_left = paths[2:5]
            path_right = paths[7:10]
            map_dict[entry] = (path_left, path_right)

        next_point = 'AAA'
        step_count = 0

        original_route = route.copy()

        while next_point != 'ZZZ':
            #rolling buffer
            direction = route.pop(0)
            route.append(direction)
            
            next_point = map_dict[next_point][direction]
            step_count += 1
        print(f'Total Steps Needed (Part 1): {step_count}')
        
        # Part 2, build a list of starting points to do all simultaneously
        step_count = 0
        route = original_route.copy()
        start_points = [ point for point in map_dict.keys() if point[-1] == 'A' ]

        z_points_in_loop = []
        wrap_idxs = []

        z_points = []
        for key in start_points:
            z_points.append(find_z_in_loop(key, map_dict, route))
        
        print(f'Total Steps Needed (Part 2): {lcm.reduce(z_points)}')

        
    

if __name__ == '__main__':
    if (len(sys.argv) != 2) or not PosixPath(sys.argv[1]).is_file() :
        print('Error 1 file argument needed')
        exit(1)

    iterations = find_my_way(sys.argv[1])

    exit(0)
