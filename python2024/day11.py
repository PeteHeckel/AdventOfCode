import sys

test_input = "125 17"

def update_stones( stones: list[int] ):
    new_stones = []
    for stone in stones:
        if stone == 0:
            new_stones.append(1)
        elif len(str(stone)) % 2 == 0:
            half_digits = int(len(str(stone)) / 2)
            new_stones.append(int(str(stone)[:half_digits]))
            new_stones.append(int(str(stone)[half_digits:]))
        else:
            new_stones.append(2024*stone)
    return new_stones

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        inp = test_input
    else:
        inp = open("inputs/day11.txt").read()
    
    stones = [int(x) for x in inp.split()]

    for i in range(25):
        stones = update_stones(stones)

    print(f"After 25 blinks -> {len(stones)} stones")