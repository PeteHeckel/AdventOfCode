from pathlib import PosixPath
import sys

def create_map(mapfile: str):
    with open(mapfile, 'r') as f:
        maprows = f.readlines()
    return [list(row.strip()) for row in maprows]

class CartPath(object):
    def __init__(self, coordinates:tuple, visited_paths:list, goal:tuple ):
        self.x_limit = goal[0]
        self.y_limit = goal[1]
        self.heat_accumulated = 0
        self.x_idx = coordinates[0]
        self.y_idx = coordinates[1]
        self.visited_paths = visited_paths

    def get_coords(self):
        return (self.x_idx, self.y_idx)



if __name__ == '__main__':
    if (len(sys.argv) != 2) or not PosixPath(sys.argv[1]).is_file() :
        print('Error 1 file argument needed')
        exit(1)
    
    heat_map = create_map(sys.argv[1])