import sys
from pathlib import PosixPath

SPEED_CHARGE_RATE = 1     # As charging, boat speed increases by 1 time / distance

def distance_calculator( max_time:int, charge_time:int ):
    run_time = max_time - charge_time
    return run_time * charge_time

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
    times = [int(i) for i in times ]

    distances = dist_line.split(':')[1].split()
    distances = [int(i) for i in distances ]

    win_case_multiplyer = 1

    for i in range(len(times)):
        win_case_multiplyer *= rah(times[i], distances[i])

    print(f"Output multiplier: {win_case_multiplyer}")

    

if __name__ == '__main__':
    if (len(sys.argv) != 2) or not PosixPath(sys.argv[1]).is_file() :
        print('Error 1 file argument needed')
        exit(1)

    lets_have_a_boat_race(sys.argv[1])

    exit(0)
