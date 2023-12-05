import sys
import os
from pathlib import PosixPath

def Get_Max_Wins( card_line: str ):
    numbers_str = card_line.split(':')[1].split('|')[0]
    num_list = numbers_str.split(' ')
    while '' in num_list:
        num_list.remove('')
    return len(num_list)


def List_Shift_Left( input_list: list ):
    for i in range(len(input_list)-1):
        input_list[i] = input_list[i+1]
    input_list[-1] = 1


def Get_Card_Matches( card_line: str ):
    numbers = card_line.split(':')[1]

    [win_nums, my_nums] = numbers.split('|')
    win_nums = win_nums.strip().split(' ')
    my_nums = my_nums.strip().split(' ')

    inner_join_nums = list( set(win_nums) & set(my_nums) ) 

    if '' in inner_join_nums:
        inner_join_nums.remove('')
    
    return len(inner_join_nums)


def Calculate_Card_Points( matching_nums: int ):
    if matching_nums == 0:
        return 0
    else:
        return 2**(matching_nums-1)


def Calculate_Deck_Values( input_file_path: str ):
    total_points = 0
    total_card_count = 0

    with open(input_file_path,'r') as f:
        max_wins = Get_Max_Wins(f.readline())

    with open(input_file_path,'r') as f:
        rolling_card_cnt = [1] * max_wins

        for line in f:
            matches = Get_Card_Matches(line)
            total_points += Calculate_Card_Points(matches)

            card_count = rolling_card_cnt[0]
            total_card_count += card_count

            List_Shift_Left(rolling_card_cnt)
            copy_add_idx = 0
            while(copy_add_idx < matches ):
                rolling_card_cnt[copy_add_idx] += card_count
                copy_add_idx += 1

    print(f'Part 1: My cards are worth ${total_points}')
    print(f'Part 2: I have {total_card_count} cards')



if __name__ == '__main__':
    if (len(sys.argv) != 2) or not PosixPath(sys.argv[1]).is_file() :
        print('Error 1 file argument needed')
        exit(1)

    Calculate_Deck_Values( sys.argv[1])

    exit(0)
