import sys


test_input_small = "\
########\n\
#..O.O.#\n\
##@.O..#\n\
#...O..#\n\
#.#.O..#\n\
#...O..#\n\
#......#\n\
########\n\
\n\
<^^>>>vv<v>>v<<"

test_input_large = "\
##########\n\
#..O..O.O#\n\
#......O.#\n\
#.OO..O.O#\n\
#..O@..O.#\n\
#O#..O...#\n\
#O..O..O.#\n\
#.OO.O.OO#\n\
#....O...#\n\
##########\n\
\n\
<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^\n\
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v\n\
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<\n\
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^\n\
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><\n\
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^\n\
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^\n\
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>\n\
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>\n\
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"

def get_next_pos( coord:tuple, dir: str ):
    match dir:
        case "<": return (coord[0] - 1, coord[1])
        case "^": return (coord[0], coord[1]-1)
        case "v": return (coord[0], coord[1]+1)
        case ">": return (coord[0] + 1, coord[1])

    assert(False)   # Shouldn't hit ever

class wide_rock( object ):
    def __init__( self, coord: tuple[int,int]):
        self.left = coord
        self.right = (coord[0] + 1, coord[1])

    def is_in( self, coord: tuple[int,int] ) -> bool:
        return coord == self.left or coord == self.right
    
    def pos( self ) -> list[tuple[int,int]]:
        return [self.left, self.right]

    def next_pos( self, dir: str ) -> list[tuple[int,int]]:
        return [ get_next_pos(self.left, dir), get_next_pos(self.right, dir) ]

    def move( self, dir: str ) -> bool:
        self.left = get_next_pos(self.left, dir)
        self.right = get_next_pos(self.right, dir)

class factory( object ):
    def __init__( self, factory_map: list[str], wide_factory: bool ):
        self.wall_pos = []
        self.rock_pos = []
        self.bot_pos = None
        self.map_size = (len(factory_map[0]), len(factory_map))
        
        # part 2 considerations
        self.wide_rocks = []
        if wide_factory:
            self.map_size = (self.map_size[0]*2, self.map_size[1])

        for y, row in enumerate(factory_map):
            for x, obj in enumerate(row):
                if wide_factory:
                    position = (2*x,y)
                else:
                    position = (x,y)

                if obj == "@":
                    self.bot_pos = position
                elif obj == "#":
                    self.wall_pos.append(position)
                    if wide_factory:
                        self.wall_pos.append((position[0]+1, position[1]))
                elif obj == "O":
                    if wide_factory:
                        self.wide_rocks.append(wide_rock(position))
                    else:
                        self.rock_pos.append(position)

    def __repr__(self):
        return_str = ""
        output_map = [["."] * self.map_size[0] for i in range(self.map_size[1])]

        for wall in self.wall_pos:
            output_map[wall[1]][wall[0]] = "#"
        
        for rock in self.rock_pos:
            output_map[rock[1]][rock[0]] = "O"
        
        for rock in self.wide_rocks:
            left = rock.left
            right = rock.right
            output_map[left[1]][left[0]] = "["
            output_map[right[1]][right[0]] = "]"

        output_map[self.bot_pos[1]][self.bot_pos[0]] = "@"
        
        for line in output_map:
            return_str += "".join(line) + "\n"

        return return_str


    def move_bot( self, dir: str ):
        next_pos = get_next_pos( self.bot_pos, dir )

        if next_pos in self.wall_pos:
            # Nothing to do, bot is running into wall
            return
        
        # part 1
        if next_pos in self.rock_pos:
            # Check if the rocks can slide without hitting wall
            rock_pos = next_pos
            while rock_pos in self.rock_pos:
                next_rock_pos = get_next_pos(rock_pos, dir)
                if next_rock_pos in self.wall_pos:
                    # Nothing to do, rock is running into wall
                    return

                rock_pos = next_rock_pos
            
            # Didn't run into wall, thus place a rock in the next position and remove the bot's new position
            self.rock_pos.append(rock_pos)
            self.rock_pos.remove(next_pos)

        # part 2
        rocks_to_check = [] # Rocks that must be checked to see if they can move
        rocks_to_move = []  # Rocks that must be moved as a result of bot or other rocks moving
        for rock in self.wide_rocks:
            if rock.is_in(next_pos):
                rocks_to_check.append(rock)

        while rocks_to_check:
            rock: wide_rock = rocks_to_check.pop()
            rocks_to_move.append(rock)
            next_rock_positions = set(rock.next_pos(dir))

            if next_rock_positions.intersection(self.wall_pos):
                return # nothing to do rock is running into wall

            for check_rock in self.wide_rocks:
                if check_rock in rocks_to_move or check_rock in rocks_to_check:
                    continue
                if next_rock_positions.intersection(check_rock.pos()):
                    rocks_to_check.append(check_rock)

        for rock in rocks_to_move:
            rock.move(dir)

        self.bot_pos = next_pos

    def calc_gps( self ) -> int:
        gps_sum = 0

        # Part 1
        for (x,y) in self.rock_pos:
            gps_sum += 100* y + x

        # part 2
        for rock in self.wide_rocks:
            gps_sum += 100* rock.left[1] + rock.left[0]

        return gps_sum


def parse_input( input_str: str ) -> tuple[factory, factory, str]:
    factory_str = []
    move_str = ""

    parse_moves = False 
    for line in input_str.splitlines():
        if line == "":
            parse_moves = True
            continue
        
        if parse_moves:
            move_str += line
        else:
            factory_str.append(line)
    
    return (factory(factory_str, False), factory(factory_str, True), move_str)

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "test_s":
        inp = test_input_small
    elif len(sys.argv) >= 2 and sys.argv[1] == "test":
        inp = test_input_large
    else:
        inp = open("inputs/day15.txt").read()

    fish_factory, wide_factory, moves = parse_input( inp )

    for move in moves:
        # print(fish_factory)
        # print(wide_factory)
        # print( move )
        fish_factory.move_bot(move)
        wide_factory.move_bot(move)
    
    print(f"GPS sum: {fish_factory.calc_gps()}")
    print(f"Wide GPS Sum: {wide_factory.calc_gps()}")
