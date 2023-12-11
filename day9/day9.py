import sys
from pathlib import PosixPath

def line_diff( line_input:list ):
    differentials = [0] * (len(line_input) - 1)
    for i in range(len(differentials)):
        differentials[i] = line_input[i+1] - line_input[i]
    
    return differentials

def extrapolate( line_history: str ):
    points = [int(i) for i in line_history.split()]
    differential_layers = [points]
    layer_depth = 0
    while( not all( diff == 0 for diff in differential_layers[layer_depth]) ):
        next_layer = line_diff(differential_layers[layer_depth])
        differential_layers.append(next_layer)
        layer_depth += 1

    next_sequence_num = 0
    differential_layers.reverse()

    for layer in differential_layers:
        next_sequence_num += layer[-1]

    return next_sequence_num

def OASIS( input_file: str ):
    sum_of_next_values = 0
    with open(input_file) as f:
        for line in f:
            next_value = extrapolate(line)
            sum_of_next_values += next_value
    print(f'Sum of Extrapolations: {sum_of_next_values}')

if __name__ == '__main__':
    if (len(sys.argv) != 2) or not PosixPath(sys.argv[1]).is_file() :
        print('Error 1 file argument needed')
        exit(1)

    OASIS(sys.argv[1])

    exit(0)
