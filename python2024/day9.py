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
            print(f"(F) {calc_idx} * {file_id_min} = {file_id_min * calc_idx}")
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

            print(f"(B) {calc_idx} * {file_id_max} = {file_id_max * calc_idx}")
            checksum += file_id_max * calc_idx
            disk_map[map_idx] -= 1
            disk_map[end_idx] -= 1
            calc_idx += 1
        map_idx += 1

    return checksum

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        inp = test_input
    else:
        inp = open("inputs/day9.txt").read()
    
    print(f"File checksum: {calc_checksum(inp)}")