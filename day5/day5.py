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
    print(outputs)
    return outputs


def parse_almanac( almanac_file: str ):
    with open(almanac_file,'r') as f:
        # First Line is starting seeds
        seed_nums = f.readline().strip().split(':')[1].split()
        seed_nums = [int(i) for i in seed_nums]

        agro_map = AgricultureMap()
        building = False

        for line in f:
            if 'map:' in line:  # New map
                agro_map.clear()
                building = True
            elif line.strip() == '': # Run seeds through map 
                seed_nums = map_seeds(agro_map, seed_nums)
                building = False
            else: # Build with numbers
                range_nums = line.strip().split()
                range_nums = [int(i) for i in range_nums]
                agro_map.add_range(range_nums)
        
        if building:
            seed_nums = map_seeds(agro_map, seed_nums)
        
        print(f'Lowest Location number: {min(seed_nums)}')
        


if __name__ == '__main__':
    if (len(sys.argv) != 2) or not PosixPath(sys.argv[1]).is_file() :
        print('Error 1 file argument needed')
        exit(1)

    parse_almanac(sys.argv[1])

    exit(0)
