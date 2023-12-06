import sys
from pathlib import PosixPath
from collections import namedtuple

class SeedRange(object):
    def __init__(self, start:int, length:int):
        self.start = start
        self.length = length
        self.end = start + length
    
    def update_start( self, new_start: int ):
        self.length = new_start - self.end
        self.start = new_start
        assert(self.length >= 0)

    def update_end( self, new_end: int ):
        self.length = new_end - self.start
        self.end = new_end
        assert(self.length >= 0)

    def map_range( self, rmap:tuple ):
        if rmap.input_start <= self.start < (rmap.input_end) :
            self.start = rmap.output_start + (self.start - rmap.input_start)
            self.end = rmap.output_start + (self.end - rmap.input_start)

class SeedMap(object):
    def __init__(self, input_start:int, output_start:int, size:int ):
        self.input_start = input_start
        self.input_end = input_start + size
        self.output_start = output_start
        self.output_end = output_start + size


class AgricultureMap(object):
    range_maps = []

    def add_map_range( self, range_nums: list):
        if len(range_nums) != 3 :
            return
        new_range = SeedMap( range_nums[0], range_nums[1], range_nums[2] )
        self.range_maps.append(new_range)

    def map_input( self, input:int ):
        for rmap in self.range_maps:
            if rmap.input_start <= input < rmap.input_end :
                return rmap.output_start + (input - rmap.input_start)
        # if nothing found in the existing maps, pass input
        return input

    def check_seed_range_overlap( self, input_range: SeedRange ):
        for rmap in self.range_maps:
            if (rmap.input_start <= input_range.start < rmap.input_end or
                rmap.input_start <= input_range.end < rmap.input_end or
                input_range.start <= rmap.input_start < input_range.end ):
                return True
        return False

    def map_seed_range( self, input_range: SeedRange ):
        output_ranges = []
        unmapped_ranges = [input_range]

        while( len(unmapped_ranges) != 0 ):
            test_range = unmapped_ranges[0]
            if not self.check_seed_range_overlap( test_range ):
                output_ranges.append(unmapped_ranges.pop(0))
            else:
                for rmap in self.range_maps:
                    if rmap.input_start <= test_range.start < rmap.input_end: # Starts within a map
                        unmapped_ranges.pop(0)
                        if rmap.input_end < test_range.end:
                            #split into one lower mapped range and one higher unmapped
                            unmapped_range = SeedRange( rmap.input_end, test_range.end )
                            unmapped_ranges.append(unmapped_range)
                            test_range.update_end( rmap.input_end )

                        test_range.map_range( rmap )
                        output_ranges.append( test_range )
                        break

                    elif rmap.input_start <= input_range.end < rmap.input_end: # Ends within a map
                        # starts within map case already checked above so only output is one lower unmapped and one higher mapped
                        unmapped_ranges.pop(0)
                        unmapped_range = SeedRange( test_range.start, rmap.input_start)
                        unmapped_ranges.append(unmapped_range)
                        test_range.update_start( rmap.input_start )
                        test_range.map_range( rmap )
                        output_ranges.append( test_range )
                        break

                    elif test_range.start < rmap.input_start and test_range.end >= rmap.input_end:   # input_range covers map + more
                        # create 2 new unmapped ranges and map the inside range
                        unmapped_ranges.pop(0)
                        lower_unmapped = SeedRange( test_range.start, rmap.input_start )
                        higher_unmapped = SeedRange( rmap.input_end, test_range.end )
                        unmapped_ranges.extend([lower_unmapped, higher_unmapped])
                        test_range.update_start(rmap.input_start)
                        test_range.update_end(rmap.input_end)
                        output_ranges.append( test_range )
                        break

        return output_ranges

    def clear( self ):
        self.range_maps = []


def map_seeds( agro_map:AgricultureMap, input_seeds:list ):
    outputs = []
    for seed in input_seeds:
        outputs.append(agro_map.map_input(seed))
    return outputs


def map_seed_ranges( agro_map: AgricultureMap, input_seed_ranges:list ):
    outputs = []
    for seed_range in input_seed_ranges:
        outputs.append(agro_map.map_seed_range(seed_range))
    return outputs


def get_seeds( seed_line: str ):
    seed_list = seed_line.strip().split(':')[1].split()
    return [int(i) for i in seed_list]


def get_seed_ranges( seed_line: str ):
    seed_list = get_seeds(seed_line)
    output_range = []
    for i in range( int(len(seed_list) / 2) ):
        output_range.append( SeedRange(seed_list[2*i], seed_list[2*i+1]) )
    return output_range


def parse_almanac( almanac_file: str ):
    with open(almanac_file,'r') as f:
        # First Line is starting seeds
        seed_line = f.readline()
        part1_seed_nums = get_seeds(seed_line)
        seed_ranges = get_seed_ranges(seed_line)

        agro_map = AgricultureMap()
        building = False

        for line in f:
            if 'map:' in line:  # New map
                agro_map.clear()
                building = True
            elif line.strip() == '': # Run seeds through map 
                part1_seed_nums = map_seeds(agro_map, part1_seed_nums)
                part2_seed_nums = map_seed_ranges(agro_map, seed_ranges)
                building = False
            else: # Build with numbers
                range_nums = line.strip().split()
                range_nums = [int(i) for i in range_nums]
                agro_map.add_map_range(range_nums)
        
        if building:
            part1_seed_nums = map_seeds(agro_map, part1_seed_nums)
            part2_seed_nums = map_seed_ranges(agro_map, part2_seed_nums)
        
        print(f'Part1 Lowest Location number: {min(part1_seed_nums)}')
        print(f'Part2 Lowest Location number: {min(part2_seed_nums)}')



if __name__ == '__main__':
    # if (len(sys.argv) != 2) or not PosixPath(sys.argv[1]).is_file() :
    #     print('Error 1 file argument needed')
    #     exit(1)

    parse_almanac(sys.argv[1])

    exit(0)
