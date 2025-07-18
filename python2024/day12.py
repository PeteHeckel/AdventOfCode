import sys

test_input = "\
RRRRIICCFF\n\
RRRRIICCCF\n\
VVRRRCCFFF\n\
VVRCCCJFFF\n\
VVVVCJJCFE\n\
VVIVCCJJEE\n\
VVIIICJJEE\n\
MIIIIIJJEE\n\
MIIISIJEEE\n\
MMMISSJEEE"

def get_value( loc: tuple[int,int], input_map: list[str] ):
    if loc[0] < 0 or loc[1] < 0: return None
    try:
        return input_map[loc[1]][loc[0]]
    except:
        return None

def get_surrounding( x, y ):
    return [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]

def find_squares( region_area: set, search_coord:tuple[int,int], input_map: list[str] ):
    loc_value = get_value((search_coord[0], search_coord[1]), input_map)
    if not loc_value:
        return
    surrounding = get_surrounding(search_coord[0], search_coord[1])

    new_area = []
    for coord in surrounding:
        if loc_value == get_value( coord, input_map ) and coord not in region_area:
            new_area.append(coord)
    
    region_area = region_area.union(new_area)

    for coord in new_area:
        region_area = region_area.union(find_squares( region_area, coord, input_map ))
    
    return region_area
    

def find_regions( input_map: list[str] ):
    regions = []
    covered_areas = set()

    for y, row in enumerate(input_map):
        for x, _value in enumerate(row):
            if (x,y) in covered_areas:
                continue
            
            region_area = {(x,y)}
            region_area = region_area.union(find_squares( region_area, (x, y), input_map ))
            regions.append(region_area)
            covered_areas = covered_areas.union(region_area)

    return regions

def get_fence_cost( region: list[tuple[int,int]]) -> int:
    area = len(region)
    perimeter = 0
    for square in region:
        perimeter += 4 - len( set(region).intersection( get_surrounding(square[0], square[1]) ) )

    return area * perimeter

def get_fence_discount( region: list[tuple[int,int]]) -> int:
    area = len(region)
    sides = 0

    # Num sides == num corners
    for coord in region:
        # outer corners
        if (coord[0]+1, coord[1]) not in region and (coord[0], coord[1]+1) not in region: sides += 1
        if (coord[0]-1, coord[1]) not in region and (coord[0], coord[1]+1) not in region: sides += 1
        if (coord[0]+1, coord[1]) not in region and (coord[0], coord[1]-1) not in region: sides += 1
        if (coord[0]-1, coord[1]) not in region and (coord[0], coord[1]-1) not in region: sides += 1
        # inner corners
        if (coord[0]+1, coord[1]) in region and (coord[0], coord[1]+1) in region and (coord[0]+1, coord[1]+1) not in region: sides += 1
        if (coord[0]-1, coord[1]) in region and (coord[0], coord[1]+1) in region and (coord[0]-1, coord[1]+1) not in region: sides += 1
        if (coord[0]+1, coord[1]) in region and (coord[0], coord[1]-1) in region and (coord[0]+1, coord[1]-1) not in region: sides += 1
        if (coord[0]-1, coord[1]) in region and (coord[0], coord[1]-1) in region and (coord[0]-1, coord[1]-1) not in region: sides += 1

    return sides * area

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        inpt = test_input
    else:
        inpt = open("inputs/day12.txt").read()
    
    regions = find_regions( inpt.splitlines() )

    total = 0
    discounted = 0
    for region in regions:
        total += get_fence_cost(region)
        discounted += get_fence_discount(region)

    print( total )
    print( discounted )
