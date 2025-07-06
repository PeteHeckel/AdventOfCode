import copy
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
        self.dir = "N"  # In both the example and the real case, the starting direction is north/up

        # Find Traveller
        for y_axis, line in enumerate(labmap):
            x_axis = line.find("^")
            if x_axis != -1:
                self.coords = (x_axis, y_axis)
                break
        
        assert(self.coords != None)
        self.labmap = labmap.copy()
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
        
        # Move to next square
        if self.labmap[next_coords[1]][next_coords[0]] == "#":
            self.rotate()
        else:
            self.coords = next_coords
            if not next_coords in self.visited_coords:
                self.visited_coords.add(next_coords)
        
        return False
    
    def check_recurive( self ) -> bool:
        
        # Simulate placing a single rock at the current point, and redo the whole walkthrough to see if it generates a loop
        fake_map = copy.deepcopy(self.labmap)
        if fake_map[self.coords[1]][self.coords[0]] == "^":
            return False # can't place a fake rock at the starting point
        
        # Replace the value with # instead
        fake_map[self.coords[1]] = fake_map[self.coords[1]][:self.coords[0]] + "#" + fake_map[self.coords[1]][self.coords[0] + 1:]

        recurse_tester = traveller(fake_map)

        seen_vecs = {(recurse_tester.coords, recurse_tester.dir)}
        while( not recurse_tester.travel() ):
            current_vec = (recurse_tester.coords, recurse_tester.dir)
            if current_vec in seen_vecs:
                return True
            seen_vecs.add(current_vec)

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

    recursive_positions = set()

    while( not travelling_dude.travel() ):
        if (not travelling_dude.coords in recursive_positions) and travelling_dude.check_recurive():
            recursive_positions.add(travelling_dude.coords)
        pass

    print(f'Spots visited = {travelling_dude.get_visited()}')
    print(f'recursions: {len(recursive_positions)}')

