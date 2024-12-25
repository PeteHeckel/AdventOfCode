import sys
from pathlib import PosixPath


def find_potential_places( springs:str, broken_len:int ):
    broken_spring = '#'
    unknown_spuring = '?'
    good_spring = '.'

    spring_count = len(springs)
    # Add tailing valid spring to avoid out of bounds checks later  
    springs = springs + '.'

    if broken_len > spring_count:
        return []

    last_start = springs.find(broken_spring)

    if last_start == -1 or last_start > (spring_count - broken_len):
        last_start = spring_count - broken_len

    assert(last_start >= 0)

    potential_starts = []

    for i in range(last_start):
        check_range = springs[i:(i+broken_len)]
        next_spring = springs[i+broken_len]
        if '.' not in check_range and next_spring != '#':
            potential_starts.append(i)
    
    return potential_starts


def recursive_perm_count( springs:str, broken_runs:list ):
    if len(broken_runs) == 0:
        return 0

    broken_len = broken_runs[0]
    potential_list = find_potential_places(springs, broken_len)

    # return none found or number found if we are at the end of the list 
    if len(potential_list) == 0 or len(broken_runs) == 1:
        return len(potential_list)

    perm_count = 0
    for idx in potential_list:
        perm_count += recursive_perm_count(springs[idx+broken_len+1], broken_runs[1:])

    return perm_count


def count_permutations( spring_line: str ):
    springs, groups = spring_line.split(sep=' ')
    broken_groups = [ int(x) for x in groups.split(sep=',') ]
    return recursive_perm_count(springs.strip(), broken_groups)


def count_all_spring_possibilities( spring_file: str ):
    permutation_count = 0
    with open(spring_file) as f:
        for line in f:
            permutation_count += count_permutations(line)

    print(f'There are {permutation_count} different broken spring arrangements')

if __name__ == '__main__':
    if (len(sys.argv) != 2) or not PosixPath(sys.argv[1]).is_file() :
        print('Error 1 file argument needed')
        exit(1)

    # part 1
    count_all_spring_possibilities(sys.argv[1])

    exit(0)
