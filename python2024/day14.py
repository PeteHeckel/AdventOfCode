import sys
import math

test_input = "\
p=0,4 v=3,-3\n\
p=6,3 v=-1,-3\n\
p=10,3 v=-1,2\n\
p=2,0 v=2,-1\n\
p=0,0 v=1,3\n\
p=3,0 v=-2,-2\n\
p=7,6 v=-1,-3\n\
p=3,0 v=-1,-2\n\
p=9,3 v=2,3\n\
p=7,3 v=-1,2\n\
p=2,4 v=2,-3\n\
p=9,5 v=-3,-3"

class robot(object):
    def __init__(self, info_str: str, map_size: list[int]):
        pos,vel = info_str.split()
        self.pos = [int(x) for x in pos.split("=")[1].split(",")]
        self.vel = [int(x) for x in vel.split("=")[1].split(",")]

        self.map = map_size

    def move( self ):
        for i in [0,1]: # axis
            self.pos[i] = (self.pos[i] + self.vel[i]) % self.map[i]
    
    def get_quadrant( self ) -> int:
        """
        Get the current quadrant of the robot
        Quadrants are labeled as:
        1|2
        ---
        3|4
        """
        x_mid = int(self.map[0] / 2)
        y_mid = int(self.map[1] / 2)
        
        if self.pos[0] == x_mid or self.pos[1] == y_mid:
            return None
    
        if self.pos[0] < x_mid:
            if self.pos[1] < y_mid:
                return 1
            else:
                return 3
        else:
            if self.pos[1] < y_mid:
                return 2
            else:
                return 4

def get_safety_margin( bots: list[robot], move_iterations:int ) -> int:
    for i in range(move_iterations):
        for bot in bots:
            bot.move()
    quad_counter = {1:0, 2:0, 3:0, 4:0}
    for bot in bots:
        quad = bot.get_quadrant()
        if quad:
            quad_counter[quad] += 1

    safety_margin = 1
    for _quad, count in quad_counter.items():
        safety_margin *= count
    
    return safety_margin

def calc_entropy( pos_map: list[list[int]], print_hist: bool ):
    flat_img = []
    for line in pos_map:
        flat_img.extend(line)
    
    # Get the value of each pixel and put it into a histogram
    hist = [0] * 256
    for value in flat_img:
        if value < 256:
            hist[value] += 1

    # Normalize by number of pixels
    pixel_cnt = len(flat_img)
    for i, _val in enumerate(hist):
        hist[i] /= pixel_cnt
    
    probabilities = []
    for val in hist:
        if val:
            probabilities.append(val)
    entropy = 0

    for prob in probabilities:
        entropy -= prob * math.log2(prob)
    
    return entropy


def make_img( bots: list[robot] ) -> list[list[int]]:
    map_dims = bots[0].map
    out_map = [[0] * map_dims[0] for j in range(map_dims[1])]
    for bot in bots:
        [x,y] = bot.pos
        out_map[y][x] += 1

    return out_map

def print_img( img: list[list[int]] ):
    for line in img:
        for val in line:
            if val:
                print(f"{val}", sep="", end="")
            else:
                print(".", sep="", end="")
        print("") # newline


def find_tree( bots: list[robot] ) -> int:
    map_dims = bots[0].map
    full_iters = map_dims[0] * map_dims[1]
    lowest_entropy = None
    lowest_loc = None

    for i in range(full_iters):
        img = make_img(bots)
        entropy = calc_entropy(img)
        if lowest_entropy is None or entropy < lowest_entropy:
            lowest_entropy = entropy
            lowest_loc = i


        for bot in bots:
            bot.move()

    return lowest_loc

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        inpt = test_input
        map_dims = [11,7]
    else:
        inpt = open("inputs/day14.txt").read()
        map_dims = [101,103]
    
    bots = []
    for line in inpt.splitlines():
        bots.append(robot(line, map_dims))

    margin = get_safety_margin( bots, 100 )
    print(f"Safety margin = {margin}")

    # Reset bots for part2
    bots = []
    for line in inpt.splitlines():
        bots.append(robot(line, map_dims))

    tree_time = find_tree(bots)
    print(f"Tree occurs at {tree_time}")

    # Reset bots for visualization
    bots = []
    for line in inpt.splitlines():
        bots.append(robot(line, map_dims))

    for i in range(tree_time):
        for bot in bots:
            bot.move()
    
    print_img(make_img(bots))
