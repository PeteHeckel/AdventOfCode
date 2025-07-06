import sys 

test_input = "\
....#.....\n\
.........#\n\
..........\n\
..#.......\n\
.......#..\n\
..........\n\
.#..^.....\n\
........#.\n\
#.........\n\
......#..."

class traveller(object): 
    def __init__( self, labmap: list[str] ):
        # Find Traveller
        for i, line in enumerate(labmap):
            start = line.find("^")
            if start != -1:
                self.coords = (start, i)
                break
        
        assert(self.coords != None)
        self.dir = "N"  # In both the example and the real case, the starting direction is north/up
        self.labmap = labmap
        self.ylim = len(labmap)
        self.xlim = len(labmap[0])
        self.visited_coords = {self.coords}
    
    def rotate( self ): 
        match self.dir:
            case "N": self.dir = "E"
            case "E": self.dir = "S"
            case "S": self.dir = "W"
            case "W": self.dir = "N"

    def travel( self ) -> bool:
        match self.dir:
            case "N": next_coords = (self.coords[0], self.coords[1]-1)
            case "E": next_coords = (self.coords[0]+1, self.coords[1])
            case "S": next_coords = (self.coords[0], self.coords[1]+1)
            case "W": next_coords = (self.coords[0]-1, self.coords[1])
        
        if (not (0 <= next_coords[0] < self.xlim)) or (not (0 <= next_coords[1] < self.ylim)):
            return True # broke free of the map
        
        print(next_coords)
        print(self.dir)
        if self.labmap[next_coords[1]][next_coords[0]] == "#":
            self.rotate()
        else:
            self.coords = next_coords
            if not next_coords in self.visited_coords:
                self.visited_coords.add(next_coords)
        
        return False
    
    def get_visited( self ) -> int:
        return len(self.visited_coords)


def parse_input( input: str ) -> list[str] :
    return [ line.strip() for line in input.splitlines() ]


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        input = test_input
    else:
        input = open("inputs/day6.txt").read()
    
    labmap = parse_input( input )

    travelling_dude = traveller(labmap)

    while( not travelling_dude.travel() ):
        # wait till he breaks free
        pass
    
    print(f'Spots visited = {travelling_dude.get_visited()}')


