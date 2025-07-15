import sys

test_input = "89010123\n\
78121874\n\
87430965\n\
96549874\n\
45678903\n\
32019012\n\
01329801\n\
10456732"


class topography_map( object ):
    def __init__( self, input_map: str ):
        self.map = [[int(x) for x in y] for y in input_map.splitlines()]
        self.xlim = len(self.map[0])
        self.ylim = len(self.map)
        self.trailheads = []
        for y,line in enumerate(self.map):
            for x, elev in enumerate(line):
                if elev == 0:
                    self.trailheads.append((x,y))
    
    def get_value( self, x:int, y:int ) -> int:
        if (not (0 <= x < self.xlim )) or (not (0 <= y < self.ylim)):
            return None
        return self.map[y][x]

    def get_next( self, x:int, y:int ) -> list[tuple[int,int]]:
        next_paths = []
        val = self.get_value(x,y)
        if val == 9 or val is None:
            return next_paths
        
        search = val + 1
        if self.get_value( x+1, y ) == search:
            next_paths.append( (x+1, y) )
        if self.get_value( x-1, y ) == search:
            next_paths.append( (x-1, y) )
        if self.get_value( x, y+1 ) == search:
            next_paths.append( (x, y+1) )
        if self.get_value( x, y-1 ) == search:
            next_paths.append( (x, y-1) )
        return next_paths

    def get_endpoints( self, points: set[tuple[int,int]] ) -> int:
        ends = 0
        next_points = set()
        for point in points:
            if self.get_value(point[0], point[1]) == 9:
                ends += 1
            else:
                next_points = next_points.union( self.get_next(point[0], point[1]) )

        if next_points:
            ends = self.get_endpoints(next_points)

        return ends

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        inp = test_input
    else:
        inp = open("inputs/day10.txt").read()
    
    topo_map = topography_map( inp )
    
    endpoint_sum = 0
    for starts in topo_map.trailheads:
        endpoint_sum += topo_map.get_endpoints({(starts[0], starts[1])})

    print(f"Trailhead scores = {endpoint_sum}")
    