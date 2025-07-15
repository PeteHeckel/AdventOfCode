import sys

test_input = "2333133121414131402"

def calc_checksum( disk_map: str ) -> int:
    checksum = 0
    disk_map = [int(x) for x in disk_map]

    map_idx = 0
    calc_idx = 0
    file_id_min = 0
    file_id_max = int(len(disk_map) / 2)
    end_idx = len(disk_map) - 1

    while map_idx <= end_idx:

        # Calculate the existing files multiplied by their ID
        while disk_map[map_idx] > 0:
            checksum += file_id_min * calc_idx
            disk_map[map_idx] -= 1
            calc_idx += 1

        file_id_min += 1
        map_idx += 1

        # Fill blanks from the end
        while disk_map[map_idx] > 0:
            if disk_map[end_idx] == 0:   # Ensure you aren't pulling from empty bins
                file_id_max -= 1
                end_idx -= 2
            
            if map_idx >= end_idx:
                break   # If the map is at the same place as the end, break so we can do one last fill

            checksum += file_id_max * calc_idx
            disk_map[map_idx] -= 1
            disk_map[end_idx] -= 1
            calc_idx += 1
        map_idx += 1

    return checksum

def calc_defrag_checksum ( disk_map: str ) -> int:
    checksum = 0
    file_map = [int(x) for x in disk_map]
    files = file_map[::2]
    gaps = file_map[1::2]

    # fs format is (id, len, starting_idx )
    idx = 0
    fs = []
    for i, len in enumerate(file_map):
        if i % 2 == 0:  # file size
            id = int(i/2)
        else:   # gap size
            id = -1
        
        if len:
            fs.append((id, len, idx))
            idx += len
    
    compressed_fs = []
    while fs:
        to_move = fs.pop()
        if to_move[0] == -1:
            continue    # Gap at the end, continue looking for real files
        
        comp_file = to_move
        for i, file in enumerate(fs):
            if file[0] == -1 and file[1] >= to_move[1]:
                comp_file = (to_move[0], to_move[1], file[2] )
                fs[i] = (file[0], file[1] - to_move[1], file[2] + to_move[1])   # update gap info
                break
        compressed_fs.append(comp_file)

    # Calculate checksum
    for (id, len, idx) in compressed_fs:
        for i in range(len):
            checksum += id * (i+idx)


    return checksum

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        inp = test_input
    else:
        inp = open("inputs/day9.txt").read()
    
    print(f"File checksum: {calc_checksum(inp)}")

    print(f"Defragged file checksum: {calc_defrag_checksum(inp)}")