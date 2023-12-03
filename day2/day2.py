import sys
from pathlib import PosixPath
from numpy import prod

def calc_set_power( cube_counts:dict ):
    return prod(list(cube_counts.values()))

def get_min_cubes( game_history: str ):
    draw_history = game_history.split(':')[1].split(';')
    
    cube_bag = {'red':0, 'green':0, 'blue':0 }

    for draw in draw_history:
        for count_colour in draw.split(','):
            [count,colour] = count_colour.strip().split(' ')
            if int(count) > cube_bag[colour]:
                cube_bag[colour] = int(count)

    return cube_bag            


"""Returns the ID number of the game if the game is valid as specified by the cube dictionary"""
def game_validity_check( game_history: str , cube_counts: dict ):
    [game_id, draw_history] = game_history.split(':')
    id_num = int(game_id.split(' ')[1])    
    
    draw_history = draw_history.split(';')

    for draw in draw_history:
        for count_colour in draw.split(','):
            [count, colour] = count_colour.strip().split(' ')
            if int(count) > cube_counts[colour]:
                return 0    # Too many cubes pulled, return 0 as failure case

    return id_num


if __name__ == '__main__':
    if len(sys.argv) != 2 or not PosixPath(sys.argv[1]).is_file():
        print('1 File Input Argument Needed')
        exit(1)

    input_file = sys.argv[1]

    bag = {'red':12, 'green':13, 'blue':14}
        
    with open(input_file, 'r') as f:
        valid_game_id_sum = 0
        set_power_sum = 0
        for game in f:
            valid_game_id_sum += game_validity_check(game, bag)
            set_power_sum += calc_set_power(get_min_cubes(game))

    print(f'Valid Game ID Sum: {valid_game_id_sum}')
    print(f'Sum of Product of Minumum Cube Counts: {set_power_sum}')