import sys
import numpy as np
import math

test_input = "\
Button A: X+94, Y+34\n\
Button B: X+22, Y+67\n\
Prize: X=8400, Y=5400\n\
\n\
Button A: X+26, Y+66\n\
Button B: X+67, Y+21\n\
Prize: X=12748, Y=12176\n\
\n\
Button A: X+17, Y+86\n\
Button B: X+84, Y+37\n\
Prize: X=7870, Y=6450\n\
\n\
Button A: X+69, Y+23\n\
Button B: X+27, Y+71\n\
Prize: X=18641, Y=10279"

def parse_input( input_str: str ):
    output = []

    for line in input_str.splitlines():
        if "Button" in line:
            x_vec, y_vec = line.split(",")
            x_vec = int(x_vec.split("+")[1])
            y_vec = int(y_vec.split("+")[1])

            if "A" in line:
                a_button = (x_vec,y_vec)
            else:
                b_button = (x_vec,y_vec)
        elif "Prize" in line:
            x_vec, y_vec = line.split(",")
            x_vec = int(x_vec.split("=")[1])
            y_vec = int(y_vec.split("=")[1])
            prize = (x_vec, y_vec)
            output.append((a_button, b_button, prize))

    return output

def find_cheapest_route( a_vec, b_vec, target_vec ) -> int:
    a_array = np.array([np.array([a_vec[0] * n, a_vec[1] * n]) for n in range(101)])
    b_array = np.array([np.array([b_vec[0] * n, b_vec[1] * n]) for n in range(101)])

    # Create 2d array by address broadcasting
    loc_matrix = a_array[:, np.newaxis] + b_array[np.newaxis, :]
    
    a_cost = np.array([n * 3 for n in range(len(a_array))])
    b_cost = np.array(range(len(b_array)))
    cost_matrix = a_cost[:, np.newaxis] + b_cost[np.newaxis, :]

    min_cost = None
    for y, line in enumerate(loc_matrix):
        for x, loc in enumerate(line):
            if loc[0] == target_vec[0] and loc[1] == target_vec[1]:
                cost = cost_matrix[y][x]
                if min_cost is None or cost < min_cost:
                    min_cost = cost
    
    return min_cost

def calc_cheapest_route( a_vec, b_vec, target_vec ) -> int:
    # Must create a system of equations
    # where, n * a + m * b = t
    # Lin-alg to the rescue!
    a = np.array(a_vec)
    b = np.array(b_vec)
    t = np.array(target_vec)

    # [a0] * n + [b0] * m = t0
    # [a1] * n + [b1] * m = t1
    A = np.array([[a[0], b[0]], [a[1], b[1]]])

    soln = np.linalg.solve(A,t)
    
    # Test solution (solve function will give floating point answers
    # we are only looking for integer correct answers)
    a_press = int(soln[0])
    b_press = int(soln[1])
    if ((a[0] * a_press + b[0] * b_press == t[0]) and 
       (a[1] * a_press + b[1] * b_press == t[1])):
        return soln[0] * 3 + soln[1]

    return None


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        inp = test_input
    else:
        inp = open("inputs/day13.txt").read()
    
    machine_params = parse_input(inp)

    total_tokens = 0
    for (a, b, target) in machine_params:
        cost = find_cheapest_route(a,b,target)
        if cost:
            total_tokens += cost

    print(f"Total Tokens required: {total_tokens}")

    # Part 2

    total_tokens = 0
    for (a,b,target) in machine_params:
        target = (target[0] + 10000000000000, target[1] + 10000000000000)
        cost = calc_cheapest_route(a,b,target)
        if cost:
            total_tokens += cost
    print(f"Total Tokens required: {total_tokens}")
    