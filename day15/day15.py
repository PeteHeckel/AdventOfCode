import sys
from pathlib import PosixPath


def holiday_ascii_string_helper( hashing_input: str ):
    current_val = 0

    for character in hashing_input:
        current_val += ord(character)
        current_val *= 17
        current_val %= 256

    return current_val

if __name__ == '__main__':
    if (len(sys.argv) != 2) or not PosixPath(sys.argv[1]).is_file() :
        print('Error 1 file argument needed')
        exit(1)

    with open(sys.argv[1]) as f:
        input_seq = f.readline()
        inputs = input_seq.split(',')

    # Part 1
    hash_sum = 0
    for input in inputs:
        hash_sum += holiday_ascii_string_helper(input.strip())
    print(f'Hashing Sum {hash_sum}')

