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

def create_perms( perm_list: list[str], size: int, include_comb: bool ) -> list[str]:
    if not perm_list:
        perm_list = ["+", "*"]
        if include_comb: perm_list.append("|")
    
    if len(perm_list[0]) == size:
        return perm_list

    out_list = []
    for perm in perm_list:
        out_list.append(perm + "*")
        out_list.append(perm + "+")
        if include_comb: out_list.append(perm + "|")

    return create_perms(out_list, size, include_comb)

def check_operands_possible( output: int, input_vals: list[int], include_combine: bool ) -> bool:
    smallest = sum(input_vals)
    largest = math.prod(input_vals)

    operator_num = len(input_vals) - 1 
    perms = create_perms([], operator_num, include_combine)

    if output == smallest or output == largest:
        return True

    for operators in perms:
        tester_arr = input_vals.copy()
        value = tester_arr.pop(0)

        for op in operators:
            num = tester_arr.pop(0)
            if op == "*":
                value *= num
            elif op == "+":
                value += num
            elif op == "|":
                numSize = len(str(num))
                value = value * (10 ** numSize) + num
            else:
                assert(False)   # confirm we've parsed correctly
        assert(not tester_arr)  # confirm it's empty

        if value == output:
            return True

    return False

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        input = test_input
    else:
        input = open("inputs/day7.txt").read()

    calibration_list = parse_input(input)

    sum_of_valid = 0

    for (test_val, cal_values) in calibration_list:
        if check_operands_possible( test_val, cal_values, False ):
            sum_of_valid += test_val

    print(f"Valid calibration results: {sum_of_valid}")

    sum_of_valid = 0
    for (test_val, cal_values) in calibration_list:
        if check_operands_possible( test_val, cal_values, True ):
            sum_of_valid += test_val

    print(f"Valid calibration results with combinations: {sum_of_valid}")
