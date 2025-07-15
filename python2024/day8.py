import sys

test_input = "............\n\
........0...\n\
.....0......\n\
.......0....\n\
....0.......\n\
......A.....\n\
............\n\
............\n\
........A...\n\
.........A..\n\
............\n\
............"

class antenna_map(object):
    def __init__(self, map_input: list[str]):
        self.freqs = {}
        self.xlim = len(map_input[0].strip())
        self.ylim = len(map_input)
        self.antinodes = set()
        self.harmonic_nodes = set()

        for y, row in enumerate(map_input):
            for x, point in enumerate(row.strip()):
                if point != '.':
                    point_loc = (x,y)
                    if point in self.freqs.keys():
                        
                        for loc in self.freqs[point]:
                            # Part 1
                            antis = self.get_antinode(point_loc, loc)
                            self.antinodes = self.antinodes.union(antis)

                            # Part 2
                            harmonics = self.get_harmonics( point_loc, loc )
                            self.harmonic_nodes = self.harmonic_nodes.union(harmonics)

                        self.freqs[point].append( point_loc )
                    else:
                        self.freqs[point] = [ point_loc ]
        
    def check_bounds( self, point: tuple[int,int]) -> bool:
        in_x = (0 <= point[0] < self.xlim)
        in_y = (0 <= point[1] < self.ylim)
        return in_x and in_y

    def get_harmonics( self, p1: tuple[int,int], p2: tuple[int,int] ) -> list[tuple[int,int]]:
        xdiff = p2[0] - p1[0]
        ydiff = p2[1] - p1[1]

        ret = []
        # Check positive vec:
        extpos = p2
        while self.check_bounds(extpos):
            ret.append(extpos)
            extpos = (extpos[0] + xdiff, extpos[1] + ydiff)

        # Check negative vec:
        extneg = p1
        while self.check_bounds(extneg):
            ret.append(extneg)
            extneg = (extneg[0] - xdiff, extneg[1] - ydiff)

        return ret

    def get_antinode(self, p1: tuple[int,int], p2: tuple[int,int] ) -> list[tuple[int,int]]:
        xdiff = p2[0] - p1[0]
        ydiff = p2[1] - p1[1]
        # Extend the vector past p2 and prior to p1
        ext2 = (p2[0] + xdiff, p2[1] + ydiff)
        ext1 = (p1[0] - xdiff, p1[1] - ydiff) 
        
        ret = []
        if self.check_bounds(ext2):
            ret.append(ext2)
        if self.check_bounds(ext1):
            ret.append(ext1)
        return ret

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        inp = test_input
    else:
        inp = open("inputs/day8.txt").read()
    
    ant_map = antenna_map(inp.splitlines())

    print(f"Number of antinodes = {len(ant_map.antinodes)}")
    
    print(f"Number of harmonic antinodes = {len(ant_map.harmonic_nodes)}")