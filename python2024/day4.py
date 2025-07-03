import sys

class word_map(object):
    def __init__( self, input: list[str] ):
        self.map = input
        self.bottom_bound = len(input)
        self.end_bound = len(input[0].strip())
    
    def get_char( self, x: int, y: int ) -> str:
        if x >= self.end_bound or x < 0:
            return ""
        if y >= self.bottom_bound or y < 0:
            return ""
        return self.map[y][x]
    
# Part 1
def count_xmas( input: list[str] ) -> int :
    search_crit = ["XMAS", "SAMX"]
    
    input_map = word_map(input)
    total = 0

    for y in range(input_map.bottom_bound):
        for x in range(input_map.end_bound):
            # Horizontal, vertical, diag up, diag down
            test_strs = ["", "", "", ""]
            for idx in range(4):
                test_strs[0] += input_map.get_char(x+idx,y)
                test_strs[1] += input_map.get_char(x,y+idx)
                test_strs[2] += input_map.get_char(x+idx,y+idx)
                test_strs[3] += input_map.get_char(x+idx,y-idx)
            
            total += len([string for string in test_strs if string in search_crit])
    
    return total

# Part 2
def count_x_mas( input: list[str] ) -> int: 
    search_crit = ["MS", "SM"]
    
    input_map = word_map(input)
    total = 0

    for y in range(1, input_map.bottom_bound - 1):
        for x in range(1, input_map.end_bound - 1):
            if input_map.get_char(x,y) != "A":
                continue
            
            diag1 = input_map.get_char(x-1,y+1) + input_map.get_char(x+1,y-1)
            diag2 = input_map.get_char(x-1,y-1) + input_map.get_char(x+1,y+1)

            if diag1 in search_crit and diag2 in search_crit:
                total +=1

    return total

test_array = "MMMSXXMASM\n\
MSAMXMSMSA\n\
AMXSXMAAMM\n\
MSAMASMSMX\n\
XMASAMXAMM\n\
XXAMMXXAMA\n\
SMSMSASXSS\n\
SAXAMASAAA\n\
MAMMMXMMMM\n\
MXMXAXMASX"

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "test":
        input = test_array.split()
    else:
        input = open("inputs/day4.txt").readlines()
    
    count = count_xmas(input)
    
    print(f'Number of XMAS occurances: {count}')

    count = count_x_mas(input)

    print(f'Number of X-MAS occurances: {count}')
