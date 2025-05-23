from pathlib import PosixPath
import sys

def find_similarity(input_arr) -> int:
    first_list = []
    freq_dict = {}

    for item in input_arr:
        first_list.append(item[0])
        if item[1] in freq_dict.keys():
            freq_dict[item[1]] = freq_dict[item[1]] + 1
        else:
            freq_dict[item[1]] = 1
    
    sim_score = 0
    for num in first_list :
        if num in freq_dict.keys():
            sim_score += num * freq_dict[num]
    return sim_score

def sort_and_find_dist(input_arr) -> int:
    first_list = [item[0] for item in input_arr]
    first_list.sort()

    second_list = [item[1] for item in input_arr]
    second_list.sort()

    cumdiff = 0
    for i, item in enumerate(first_list):
        cumdiff += abs(item - second_list[i])
    
    return cumdiff

def input_parse( input_path ) -> list:
    output_list = []
    with open(input_path) as f:
        for line in f:
            [num1_str, num2_str] = line.split()
            output_list.append([int(num1_str), int(num2_str)])
    
    return output_list


test_input = [[3,4], [4,3], [2,5], [1,3], [3,9], [3,3]]

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        input_arr = test_input
    else:
        input_arr = input_parse( PosixPath("inputs/day1.txt") )

    total_dist = sort_and_find_dist(input_arr)

    print(f'Total distance is {total_dist}')

    similarity = find_similarity(input_arr)

    print(f'Similarity Score is {similarity}')