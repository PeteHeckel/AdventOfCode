import sys
from pathlib import PosixPath

def Build_Schematic_Table( input_file: str ):
    character_table = []
    with open(input_file) as f:
        for line in f:
            character_table.append(list(line))
    return character_table

class Indices:
    start_idx = None
    end_idx = None

    def __repr__(self) -> str:
        return f'Start: {self.start_idx}, End: {self.end_idx}'


''' Returns list of start and end indices of numbers in the line '''
def Find_Part_Numbers( input_line: list ):
    all_number_indices = []
    active_number = Indices()

    for i, char in enumerate(input_line):  
        if active_number.start_idx is None:    # No active run of numbers ongoing
            if char.isnumeric():               # Start new number building
                active_number.start_idx = i
        else:                       # In prog building a number
            if not char.isnumeric():            # End of new number building
                active_number.end_idx = i
                all_number_indices.append(active_number)
                active_number = Indices()

    # Case where list ended with number run still ongoing
    if active_number.start_idx is not None and active_number.end_idx is None:
        active_number.end_idx = len(input_line)
        all_number_indices.append(active_number)
    
    return all_number_indices


def Check_For_Symbols( char_list: list ):
    str_slice = ''
    str_slice = str_slice.join(char_list)
    remaining_chars = str_slice.replace('.', '')
    # Symbols present if remaining chars not empty and not alphanumeric
    return (remaining_chars != '' and not remaining_chars.isalnum())


def CheckSurroundingChars( ref_table:list, line_idx, bound_idxs: Indices ):
    # If we should check above and below for symbols
    check_above = (line_idx != 0)
    check_below = (line_idx != (len(ref_table)-1))
    check_left = bound_idxs.start_idx != 0
    check_right = bound_idxs.end_idx != (len(ref_table[line_idx])-1)

    check_idxs = Indices()
    if check_left:
        check_idxs.start_idx = bound_idxs.start_idx - 1
    else:
        check_idxs.start_idx = bound_idxs.start_idx

    if check_right:
        check_idxs.end_idx = bound_idxs.end_idx + 1
    else:
        check_idxs.end_idx = bound_idxs.end_idx

    if check_left and Check_For_Symbols(ref_table[line_idx][check_idxs.start_idx]):
        return True

    if check_right and Check_For_Symbols( ref_table[line_idx][check_idxs.end_idx-1] ):
        return True

    if check_above and Check_For_Symbols(ref_table[line_idx-1][check_idxs.start_idx:check_idxs.end_idx] ):
        return True

    if check_below and Check_For_Symbols(ref_table[line_idx+1][check_idxs.start_idx:check_idxs.end_idx] ):
        return True

    return False


def Sum_Valid_Part_No_In_Line( ref_table:list, line_idx:int ):
    number_idxs = Find_Part_Numbers(ref_table[line_idx])

    line_sum = 0

    for start_end_idx in number_idxs:
        if CheckSurroundingChars(ref_table, line_idx, start_end_idx):
            part_no = ''
            line = ref_table[line_idx][start_end_idx.start_idx:start_end_idx.end_idx]
            line_sum += int(part_no.join(line))
    
    return line_sum


def Evaluate_Schematic_Part_Sum( schematic_table:list ):
    part_sum = 0
    for i in range(len(schematic_table)):
        part_sum += Sum_Valid_Part_No_In_Line(schematic_table, i)

    return part_sum


def Find_Full_Num( line:list, center_idx:int ):
    number = [line[center_idx]]
    assert(number[0].isnumeric())

    # Backtrack first
    idx = center_idx - 1
    while( idx >= 0 ):
        char = line[idx]
        if not char.isnumeric():
            break
        number.insert(0,char)
        idx -= 1
    
    idx = center_idx + 1
    while( idx < len(line)):
        char = line[idx]
        if not char.isnumeric():
            break
        number.append(char)
        idx += 1
    
    num_str = ''
    for digit in number:
        num_str += digit

    return int( num_str )


def CheckSurroundingNums( ref_table:list, line_idx:int, col_idx:int ):
    check_above = (line_idx != 0)
    check_below = (line_idx != (len(ref_table)-1))
    check_left = col_idx != 0
    check_right = col_idx != (len(ref_table[line_idx])-1)

    num_count = 0
    out_mult = 1

    if check_left and ref_table[line_idx][col_idx-1].isnumeric():
        num_count += 1
        out_mult *= Find_Full_Num(ref_table[line_idx], col_idx-1)

    if check_right and ref_table[line_idx][col_idx+1].isnumeric():
        num_count += 1
        out_mult *= Find_Full_Num(ref_table[line_idx],col_idx+1)
    
    if check_above:
        if ref_table[line_idx-1][col_idx].isnumeric():
            num_count += 1
            out_mult *= Find_Full_Num(ref_table[line_idx-1],col_idx)
        else:
            if check_left and ref_table[line_idx-1][col_idx-1].isnumeric():
                num_count += 1
                out_mult *= Find_Full_Num(ref_table[line_idx-1],col_idx-1)
            
            if check_right and ref_table[line_idx-1][col_idx+1].isnumeric():
                num_count += 1
                out_mult *= Find_Full_Num(ref_table[line_idx-1],col_idx+1)
    
    if check_below:
        if ref_table[line_idx-1][col_idx].isnumeric():
            num_count += 1
            out_mult *= Find_Full_Num(ref_table[line_idx-1],col_idx)
        else:
            if check_left and ref_table[line_idx+1][col_idx-1].isnumeric():
                num_count += 1
                out_mult *= Find_Full_Num(ref_table[line_idx+1],col_idx-1)
            
            if check_right and ref_table[line_idx+1][col_idx+1].isnumeric():
                num_count += 1
                out_mult *= Find_Full_Num(ref_table[line_idx+1],col_idx+1)

    if num_count != 2:
        return 0
    
    return out_mult


def Find_Gear_Idxs( line:list ):
    gear_idxs = []
    for i, char in enumerate(line):
        if char == '*':
            gear_idxs.append(i)

    return gear_idxs


def Sum_Gear_Ratio_In_Line( schematic_table:list, line_idx:int ):
    line_sum = 0
    gear_idxs = Find_Gear_Idxs( schematic_table[line_idx])

    for gear_idx in gear_idxs:
        line_sum += CheckSurroundingNums(schematic_table, line_idx, gear_idx)
    
    return line_sum


def Evaluate_Gear_Ratio_Sum( schematic_table: list ):
    ratio_sum = 0
    for i in range(len(schematic_table)):
        ratio_sum += Sum_Gear_Ratio_In_Line( schematic_table, i )
    
    return ratio_sum



if __name__ == '__main__':
    if len(sys.argv) != 2 or not PosixPath(sys.argv[1]).is_file():
        print('Error: Input 1 file argument')
        exit(1)
    
    schematic_table = Build_Schematic_Table(sys.argv[1])

    part_sum = Evaluate_Schematic_Part_Sum(schematic_table)
    gear_ratio_sum = Evaluate_Gear_Ratio_Sum(schematic_table)
    print(f'Part Sum {part_sum}')
    print(f'Gear Sum {gear_ratio_sum}')
    