import sys
from pathlib import PosixPath

class PipePiece( object ):
    def __init__( self, character:str, xy_coords:tuple ):
        self.character = character
        self.x_idx = xy_coords[0]
        self.y_idx = xy_coords[1]
        self.start = character == 'S'
    
    def get_coords( self ):
        return (self.x_idx, self.y_idx)

    def get_next_coords( self, xy_coords:tuple ):
        (x_input, y_input) = xy_coords
        x_diff = x_input - self.x_idx
        y_diff = y_input - self.y_idx
        if abs(x_diff) >= 1 and abs(y_diff) >= 1:
            return None
        
        if x_diff == -1:
            if self.character == '-':
                return ( self.x_idx + 1, self.y_idx )
            elif self.character == 'J':
                return ( self.x_idx, self.y_idx - 1 )
            elif self.character == '7':
                return (self.x_idx, self.y_idx + 1 )
            else: 
                return None
        elif x_diff == 1:
            if self.character == '-':
                return ( self.x_idx - 1, self.y_idx )
            elif self.character == 'L':
                return ( self.x_idx, self.y_idx - 1 )
            elif self.character == 'F':
                return (self.x_idx, self.y_idx + 1 )
            else: 
                return None
        elif y_diff == -1:
            if self.character == '|':
                return ( self.x_idx, self.y_idx + 1 )
            elif self.character == 'L':
                return ( self.x_idx + 1, self.y_idx )
            elif self.character == 'J':
                return (self.x_idx - 1, self.y_idx )
            else: 
                return None
        elif y_diff == 1:
            if self.character == '|':
                return ( self.x_idx, self.y_idx - 1 )
            elif self.character == 'F':
                return ( self.x_idx + 1, self.y_idx )
            elif self.character == '7':
                return (self.x_idx - 1, self.y_idx )
            else:
                return None
        else:
            return None

def get_character( char_map:list, xy_coordinates:tuple ):
    (x_idx,y_idx) = xy_coordinates
    return char_map[y_idx][x_idx]


def find_furthest_pipe( map_file: str ):
    pipe_map = []
    with open(map_file) as f:
        for y_idx, line in enumerate(f):
            pipe_map.append(list(line))
            x_idx = line.find('S')
            if x_idx != -1:
                start_pipe = PipePiece(line[x_idx], (x_idx, y_idx))
    
    (start_x, start_y) = start_pipe.get_coords()
    prev_coords = start_pipe.get_coords()
    next_char = get_character(pipe_map, (start_x, start_y+1))

    traveller = PipePiece( next_char, (start_x, start_y+1) )
    step_count = 1

    while not traveller.start:
        next_coords = traveller.get_next_coords( prev_coords )
        prev_coords = traveller.get_coords()
        next_char = get_character( pipe_map, next_coords )
        traveller = PipePiece( next_char, next_coords )
        step_count += 1

    half_point = step_count / 2

    print(f'Furthest point is {half_point}')    
     

if __name__ == '__main__':
    if (len(sys.argv) != 2) or not PosixPath(sys.argv[1]).is_file() :
        print('Error 1 file argument needed')
        exit(1)

    find_furthest_pipe(sys.argv[1])

    exit(0)
