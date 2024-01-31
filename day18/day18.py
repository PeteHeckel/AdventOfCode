from pathlib import PosixPath
import sys

def read_dig_plan( map_file: str, hex_value=False ):
    with open(map_file) as f:
        dig_plan = f.readlines()
    
    edge_list = []
    for line in dig_plan:
        line = line.strip()
        [direction, length, rgb_colour] = line.split(' ', 3)
        if hex_value:
            num_to_direction_dict = {'0':'R', '1':'D', '2':'L', '3':'U'}
            direction = num_to_direction_dict[rgb_colour[7]]
            length = int(rgb_colour[2:7], base=16)
        edge_list.append((direction, int(length), rgb_colour))

    return edge_list

class Edge(object):
    def __init__(self, coordinates, colour) -> None:
        self.colour = colour
        self.x_idx = coordinates[0]
        self.y_idx = coordinates[1]
        self.direction = None
        self.x_end_idx = None
        self.y_end_idx = None
        self.len = None


    def get_end_coords(self, direction, length) -> list:
        direction_map = {
            'R' : (1,0),
            'L' : (-1,0),
            'U' : (0,-1),
            'D' : (0,1)
        }
        self.direction = direction
        self.len = length
        (x_idx_mult, y_idx_mult) = direction_map[direction]
        x_offset = x_idx_mult * length
        y_offset = y_idx_mult * length
        self.x_end_idx = self.x_idx + x_offset
        self.y_end_idx = self.y_idx + y_offset
        return (self.x_end_idx, self.y_end_idx)

    def get_coordinates(self) -> tuple:
        return (self.x_idx, self.y_idx)

def calc_lagoon_area( dig_plan: list ):
    coordinates = (0,0)
    lagoon_edges = []

    for edge in dig_plan:
        (direction, length, rgb_colour) = edge
        corner_piece = Edge(coordinates, rgb_colour)
        coordinates = corner_piece.get_end_coords(direction, int(length))
        lagoon_edges.append(corner_piece)
    
    # shoelace formula 
    area = 0
    edge_len = 0
    for i, edge in enumerate(lagoon_edges):
        if i == len(lagoon_edges)-1:    #wrap case
            next_edge = lagoon_edges[0]
        else:
            next_edge = lagoon_edges[i+1]
        area += edge.x_idx * next_edge.y_idx - next_edge.x_idx * edge.y_idx
        edge_len += edge.len
    
    area /= 2
    print(f'A: {area}')
    print(f'B: {edge_len}')
    
    # A = shoelace formula
    # b = perimeter
    # Rearrange Picks theorem to solve for number of points inside (i)
    # A = i + b/2 - 1 => A + 1 - b/2 = i
    # Request is for b + i
    # b + i = b + A + 1 - b/2 = A + 1 + b/2
    holes = area + edge_len/2 + 1
    print(f'Volume: {holes}')


if __name__ == '__main__':
    if (len(sys.argv) != 2) or not PosixPath(sys.argv[1]).is_file() :
        print('Error 1 file argument needed')
        exit(1)
    
    print('Part1:')
    plan = read_dig_plan(sys.argv[1], False)
    calc_lagoon_area(plan)

    print('Part2:')
    plan = read_dig_plan(sys.argv[1], True)
    calc_lagoon_area(plan)

    exit(0)