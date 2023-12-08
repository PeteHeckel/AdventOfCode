import sys
from pathlib import PosixPath


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

        while next_point != 'ZZZ':
            #rolling buffer
            direction = route.pop(0)
            route.append(direction)
            
            next_point = map_dict[next_point][direction]
            step_count += 1
        
        print(f'Total Steps Needed: {step_count}')
    

if __name__ == '__main__':
    if (len(sys.argv) != 2) or not PosixPath(sys.argv[1]).is_file() :
        print('Error 1 file argument needed')
        exit(1)

    iterations = find_my_way(sys.argv[1])

    exit(0)
