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


    # Part 2
    boxes = {}
    for box_num in range(256):
        boxes[box_num] = {}

    for input in inputs:
        input = input.strip()
        split_idx = input.find('-')
        if split_idx != -1:
            operator = '-'
            focal_length = None
        else:
            split_idx = input.find('=')
            operator = '='
            focal_length = input[split_idx+1]
        lens_label = input[:split_idx]
        box_label = holiday_ascii_string_helper(lens_label)

        if operator == '=':
            assert(focal_length is not None)
            boxes[box_label][lens_label] = int(focal_length)
        elif boxes[box_label].get(lens_label):
            boxes[box_label].pop(lens_label)

    focusing_power = 0
    for box_mult, box in enumerate(boxes.values(), start=1):
        for lens_mult, lens in enumerate(box.values(),start=1):
            focusing_power += box_mult * lens_mult * int(lens)

    print(f'Focusing power of the lens config: {focusing_power}')