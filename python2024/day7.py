import sys
import math

test_input = "190: 10 19\n\
3267: 81 40 27\n\
83: 17 5\n\
156: 15 6\n\
7290: 6 8 6 15\n\
161011: 16 10 13\n\
192: 17 8 14\n\
21037: 9 7 18 13\n\
292: 11 6 16 20"

def parse_input( input: str):
    output = []
    for line in input.splitlines():
        test_value, cal_values = line.split(":")
        cal_values = [int(val) for val in cal_values.split()]
        output.append((int(test_value), cal_values))
    return output

def check_operands_possible( output: int, input_vals: list[int] ) -> bool:
    smallest = sum(input_vals)
    largest = math.prod(input_vals)

    if output == smallest or output == largest:
        return True
    
    bit_multer = 0
    while bit_multer.bit_length() < (len(input_vals)):
        input_copy = input_vals.copy()
        value = input_copy.pop(0)

        bit_multer_tester = bit_multer
        while input_copy:
            if bit_multer_tester & 1:
                value *= input_copy.pop(0)
            else:
                value += input_copy.pop(0)
            bit_multer_tester = bit_multer_tester >> 1
        if value == output:
            return True
        bit_multer += 1

    return False

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        input = test_input
    else:
        input = open("inputs/day7.txt").read()

    calibration_list = parse_input(input)

    sum_of_valid = 0

    for (test_val, cal_values) in calibration_list:
        ops = check_operands_possible( test_val, cal_values )
        if ops:
            sum_of_valid += test_val * ops
    
    print(f"Valid calibration results: {sum_of_valid}")