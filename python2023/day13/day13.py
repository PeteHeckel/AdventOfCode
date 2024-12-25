import sys
from pathlib import PosixPath

def build_mirror_maps( mirror_rock_map: str ):
    mirrors = [[]]
    with open(mirror_rock_map) as f: 
        mirror_count = 0
        for line in f:
            if len(line.strip()) == 0:
                mirror_count += 1
                mirrors.append([])
            else:
                mirrors[mirror_count].append(list(line.strip()))
    return mirrors

# transpose
def transpose_lists(list_of_lists: list):
    return list(map(list, zip(*list_of_lists)))

# Part 1 check
def reflect_check( first_half: list, second_half: list ):
    first_half_compare = list(reversed(first_half))
    second_half_compare = second_half
    

    for half_1,half_2 in zip(first_half_compare, second_half_compare):
        if half_1 != half_2:
            return False

    return True

# Part 2 check
def smudge_check( first_half:list, second_half:list):
    first_half_compare = list(reversed(first_half))
    second_half_compare = second_half
    
    different_count = 0
    for half_1,half_2 in zip(first_half_compare, second_half_compare):
        for item1, item2 in zip(half_1, half_2):
            if item1 != item2:
                different_count += 1
    
    return different_count == 1

def mirror_code( mirror_map:list ):
    horizontal_split_potentials = set(range(1, len(mirror_map)))

    for split in horizontal_split_potentials:
        top_side = mirror_map[:split]
        bottom_side = mirror_map[split:]
        if smudge_check(top_side, bottom_side):
            return split * 100

    mirror_map_t = transpose_lists(mirror_map)

    vertical_split_potentials = set(range(1, len(mirror_map_t)))
    for split in vertical_split_potentials:
        top_side = mirror_map_t[:split]
        bottom_side = mirror_map_t[split:]
        if smudge_check(top_side, bottom_side):
            return split

    for line in mirror_map:
        print(line)

    assert(False)


def summarize_mirror( mirror_map: list ):
    # First check for vertical mirror
    vertical_split_potentials = set(range(1, len(mirror_map[0])))
    horizontal_split_potentials = set(range(1, len(mirror_map)))

    for row in mirror_map:
        new_potential_v_split = []
        for split in vertical_split_potentials:
            left_side = row[:split]
            right_side = row[split:]
            left_side.reverse()

            if all([x==y for x,y in zip(left_side,right_side)]):
                new_potential_v_split.append(split)

        vertical_split_potentials = vertical_split_potentials & set(new_potential_v_split) 

        if len(vertical_split_potentials) == 0:
            break

    horizontal_split = None
    # Then check for horizontal spanning mirror
    for split in horizontal_split_potentials:
        top_side = mirror_map[:split]
        bottom_side = mirror_map[split:]
        top_side.reverse()
        if all([x==y for x,y in zip(top_side,bottom_side)]):
            horizontal_split = split

    if ((horizontal_split is None and len(vertical_split_potentials) == 0) or
       (horizontal_split is not None and len(vertical_split_potentials) > 0)):
        for line in mirror_map:
            print(line)
        assert(False)

    if horizontal_split:
        return 100* horizontal_split
    else:
        return min(vertical_split_potentials)
        


if __name__ == '__main__':
    if (len(sys.argv) != 2) or not PosixPath(sys.argv[1]).is_file() :
        print('Error 1 file argument needed')
        exit(1)

    # part 1
    mirror_maps = build_mirror_maps(sys.argv[1])

    print(f'Number of mirrors: {len(mirror_maps)}')

    mirror_summary = 0

    for mirror_map in mirror_maps:
        mirror_summary += mirror_code( mirror_map )

    print(f'Mirror summary: {mirror_summary}')

    exit(0)
