import sys
from pathlib import PosixPath

class PipePiece( object ):
    def __init__( character:str, x_idx:int, y_idx:int ):
        self.character = character
        self.x_idx = x_idx
        self.y_idx = y_idx
        self.start = character == 'S'
    
    def get_next_pipe_coords( self, x_input, y_input ):
        x_diff = x_input - self.x_idx
        y_diff = y_input - self.y_idx
        if abs(x_diff) >= 1 and abs(y_diff) >= 1:
            return None
        
        if x_diff == -1:
            if self.character == '-':
                return ( self.x_idx + 1, self.y_idx )
            elif self.character == 'J':
                return ( self.x_idx, self.y_idx + 1 )
            elif self.character == '7':
                return (self.x_idx, self.y_idx - 1 )
            else: 
                return None
        elif x_diff == 1:
            if self.character == '-':
                return ( self.x_idx - 1, self.y_idx )
            elif self.character == 'L':
                return ( self.x_idx, self.y_idx + 1 )
            elif self.character == 'F':
                return (self.x_idx, self.y_idx - 1 )
            else: 
                return None
        elif y_diff == -1:
            if self.character == '|':
                return ( self.x_idx, self.y_idx + 1 )
            elif self.character == 'F':
                return ( self.x_idx + 1, self.y_idx )
            elif self.character == '7':
                return (self.x_idx - 1, self.y_idx )
            else: 
                return None
        elif y_diff == 1:
            if self.character == '|':
                return ( self.x_idx, self.y_idx - 1 )
            elif self.character == 'L':
                return ( self.x_idx + 1, self.y_idx )
            elif self.character == 'J':
                return (self.x_idx - 1, self.y_idx )
            else: 
                return None
        else:
            return None

def find_furthest_pipe( map_file: str ):
    pipe_map = []
    with open(map_file) as f:
        for y_idx, line in enumerate(f):
            pipe_map.append(list(line))
            x_idx = line.find('S')
            if x_idx != -1:
                start_pipe = PipePiece(line[x_idx], x_idx, y_idx)

     

if __name__ == '__main__':
    if (len(sys.argv) != 2) or not PosixPath(sys.argv[1]).is_file() :
        print('Error 1 file argument needed')
        exit(1)

    find_furthest_pipe(sys.argv[1])

    exit(0)
