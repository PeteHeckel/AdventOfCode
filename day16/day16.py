import sys
from pathlib import PosixPath

def create_mirror_map( mapfile:str):
    with open(mapfile, 'r') as f:
        map_rows = f.readlines()
    return [ list(row.strip()) for row in map_rows ]


class Beam(object):
    def __init__(self, coords:tuple, direction:str) -> None:
        possible_directions = ['N','E','S','W']
        self.x_pos = coords[0]
        self.y_pos = coords[1]
        assert(direction in possible_directions)
        self.direction = direction

    def get_coords(self):
        return (self.x_pos, self.y_pos)

    def split_beam(self, mirror_map:list):
        try:
            tile = mirror_map[self.y_pos][self.x_pos]
        except IndexError:
            return []
        
        if (tile == '-' and 
            self.direction in ['N', 'S']):
            return [Beam(self.get_coords(), 'E'), Beam(self.get_coords(), 'W')]

        elif (tile == '|' and
              self.direction in ['E', 'W'] ):
            return [Beam(self.get_coords(), 'N'), Beam(self.get_coords(), 'S')]
        else:
            return []


    def move(self, mirror_map):
        map_x_bound = len(mirror_map[0])
        map_y_bound = len(mirror_map)
        
        tile = mirror_map[self.y_pos][self.x_pos]

        if tile == '|' and self.direction in ['E','W']:
            return False
        
        if tile == '-' and self.direction in ['N','S']:
            return False


        backslash_mirror_dir_map = {'N':'W', 'E':'S', 'S':'E', 'W':'N'}
        forwardslash_mirror_dir_map = {'N':'E', 'E':'N', 'S':'W', 'W':'S'}
        if tile == '\\':
            self.direction = backslash_mirror_dir_map[self.direction]
        elif tile == '/':
            self.direction = forwardslash_mirror_dir_map[self.direction]


        if self.direction == 'N':
            self.y_pos -= 1
        elif self.direction == 'S':
            self.y_pos += 1
        elif self.direction == 'E':
            self.x_pos += 1
        elif self.direction == 'W':
            self.x_pos -= 1

        # Return true if the beam is within the bounds of the map
        return ((0 <= self.x_pos < map_x_bound) and 
                (0 <= self.y_pos < map_y_bound))

def find_energized( mirror_map, start_coords, start_dir ):
    beams = [Beam(start_coords, start_dir)]
    energized_tiles = {start_coords:[start_dir]}

    while len(beams) > 0:
        moving_beam = beams.pop(0)
        while moving_beam.move(mirror_map):
            energy_dir = energized_tiles.get(moving_beam.get_coords())
            if energy_dir:
                if moving_beam.direction in energy_dir:
                    break
                energized_tiles[moving_beam.get_coords()].append(moving_beam.direction)
            else:
                energized_tiles[moving_beam.get_coords()] = [moving_beam.direction]
        beams.extend(moving_beam.split_beam(mirror_map))

    return len(energized_tiles)

if __name__ == '__main__':
    if (len(sys.argv) != 2) or not PosixPath(sys.argv[1]).is_file() :
        print('Error 1 file argument needed')
        exit(1)

    # Part 1
    mirror_map = create_mirror_map( sys.argv[1] )
    energized_tiles = find_energized(mirror_map, (0,0), 'E')
    print(f'Total energized tiles: {energized_tiles}')

    exit(0)