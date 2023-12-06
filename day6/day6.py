import sys
from pathlib import PosixPath

SPEED_CHARGE_RATE = 1     # As charging, boat speed increases by 1 time / distance



def binary_search_charge_threshold( time:int, distance:int ):
    ## TODO
    
    return 4

def distance_calculator( max_time:int, charge_time:int ):
    run_time = max_time - charge_time
    return run_time * charge_time

def RAH_RAH_RAH( time:int, distance:int ):

    # Binary search to find the win_threshold
    winning_time_thresh = binary_search_charge_threshold(time, distance)

    # Middle of array is always apex in this fn
    best_time = distance_calculator(time/2, distance/2)

    win_conditions = (best_time - winning_time_thresh) * 2  # Double to account for both sides
    sole_winner = ((time % 2) != 0) # if time to hold is odd, there will be a single best time
    if sole_winner:
        win_conditions -= 1

    return win_conditions

def rah( time:int, distance:int ):
    print('RAH, ')

    above_values = 0
    for charge_time in range(time):
        my_boats_dist = distance_calculator(time, charge_time)
        if( my_boats_dist > distance ):
            above_values += 1
    
    return above_values


def lets_have_a_boat_race( timesheet_filepath: str ):
    with open(timesheet_filepath, 'r') as f:
        time_line = f.readline()
        dist_line = f.readline()

    times = time_line.split(':')[1].split()
    time_nums = [int(i) for i in times ]

    distances = dist_line.split(':')[1].split()
    dist_nums = [int(i) for i in distances ]

    real_record_time = ""
    for time in times:
        real_record_time += time.strip()
    real_record_time = int(real_record_time)
    
    real_record_dist = ""
    for dist in distances:
        real_record_dist += dist.strip()
    real_record_dist = int(real_record_dist)

    win_case_multiplyer = 1

    for i in range(len(time_nums)):
        win_case_multiplyer *= rah(time_nums[i], dist_nums[i])

    real_win_outcomes = RAH_RAH_RAH(real_record_time, real_record_dist)

    print(f"Output multiplier: {win_case_multiplyer}")
    print(f"Win Conditions: {real_win_outcomes}")

    

if __name__ == '__main__':
    if (len(sys.argv) != 2) or not PosixPath(sys.argv[1]).is_file() :
        print('Error 1 file argument needed')
        exit(1)

    lets_have_a_boat_race(sys.argv[1])

    exit(0)
