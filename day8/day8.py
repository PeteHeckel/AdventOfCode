import sys
from pathlib import PosixPath

def find_z_in_loop( start_point:str, map_dict:dict, directions:list ):
    point = start_point
    index_count = 0
    z_points = []
    for direction in directions:
        index_count += 1
        point = map_dict[point][direction]
        if point[-1] == 'Z':
            z_points.append(index_count)
    print(f'Next Point: {point}, Z-Indices: {z_points}')
    return point, z_points  # Return the end point of the direction loop and a list of all the matching z_points

def inner_join_lists( list_of_lists ):
    common_list = list_of_lists[0]
    for num_list in list_of_lists:
        common_list = list(set(common_list) & set(num_list))
    return common_list



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

        # while next_point != 'ZZZ':
        #     #rolling buffer
        #     direction = route.pop(0)
        #     route.append(direction)
            
        #     next_point = map_dict[next_point][direction]
        #     step_count += 1
        # print(f'Total Steps Needed (Part 1): {step_count}')
        
        # Part 2, build a list of starting points to do all simultaneously
        step_count = 0
        route = original_route.copy()
        start_points = [ point for point in map_dict.keys() if point[-1] == 'A' ]

        z_points_in_loop = [[]] * len(start_points)

        print(len(start_points))
        z_point_dict = {}
        for key in map_dict.keys():
            z_point_dict[key] = find_z_in_loop(key, map_dict, route)
        
        while 1:
            for i in range(len(start_points)):
                start_points[i], z_points_in_loop[i] = z_point_dict[start_points[i]]
            common_z = inner_join_lists( z_points_in_loop )
            if len(common_z) != 0:
                step_count += common_z[0]
                break
            else:
                step_count += len(route)

        # while not check_end_points(start_points):
        #     print(start_points)
        #     break
        #     #rolling buffer
        #     direction = route.pop(0)
        #     route.append(direction)

        #     for i in range(len(start_points)):
        #         start_points[i] = map_dict[start_points[i]][direction]
        #     step_count += 1
        print(f'Total Steps Needed (Part 2): {step_count}')

        
    

if __name__ == '__main__':
    if (len(sys.argv) != 2) or not PosixPath(sys.argv[1]).is_file() :
        print('Error 1 file argument needed')
        exit(1)

    iterations = find_my_way(sys.argv[1])

    exit(0)
