import sys
from pathlib import PosixPath
from collections import namedtuple


class AgricultureMap(object):
    RangeMap = namedtuple('Mapping_Ranges', ['output_start', 'input_start', 'size'] )
    range_maps = []

    def add_range( self, range_nums: list):
        if len(range_nums) != 3 :
            return
        new_range = self.RangeMap( range_nums[0], range_nums[1], range_nums[2] )
        self.range_maps.append(new_range)

    def map_input( self, input:int ):
        for rmap in self.range_maps:
            if rmap.input_start <= input < (rmap.input_start + rmap.size) :
                return rmap.output_start + (input - rmap.input_start)
        # if nothing found in the existing maps, pass input
        return input

    def clear( self ):
        self.range_maps = []


def map_seeds( agro_map:AgricultureMap, input_seeds:list ):
    outputs = []
    for seed in input_seeds:
        outputs.append(agro_map.map_input(seed))
    return outputs

def get_seeds( seed_line: str, range_of_seeds: bool ):
    seed_list = seed_line.strip().split(':')[1].split()
    seed_list = [int(i) for i in seed_list]

    seeds = []
    if range_of_seeds:
        for i in range(int(len(seed_list)/2)):
            start_range = seed_list[2*i]
            range_size = seed_list[2*i+1]
            seeds.extend(list(range(start_range, start_range + range_size)))
    else:
        seeds = seed_list
    return seeds


def parse_almanac( almanac_file: str ):
    with open(almanac_file,'r') as f:
        # First Line is starting seeds
        seed_line = f.readline()
        part1_seed_nums = get_seeds(seed_line, False)
        part2_seed_nums = get_seeds(seed_line, True)

        agro_map = AgricultureMap()
        building = False

        for line in f:
            if 'map:' in line:  # New map
                agro_map.clear()
                building = True
            elif line.strip() == '': # Run seeds through map 
                part1_seed_nums = map_seeds(agro_map, part1_seed_nums)
                part2_seed_nums = map_seeds(agro_map, part2_seed_nums)
                building = False
            else: # Build with numbers
                range_nums = line.strip().split()
                range_nums = [int(i) for i in range_nums]
                agro_map.add_range(range_nums)
        
        if building:
            part1_seed_nums = map_seeds(agro_map, part1_seed_nums)
            part2_seed_nums = map_seeds(agro_map, part2_seed_nums)
        
        print(f'Part1 Lowest Location number: {min(part1_seed_nums)}')
        print(f'Part2 Lowest Location number: {min(part2_seed_nums)}')



if __name__ == '__main__':
    if (len(sys.argv) != 2) or not PosixPath(sys.argv[1]).is_file() :
        print('Error 1 file argument needed')
        exit(1)

    parse_almanac(sys.argv[1])

    exit(0)
