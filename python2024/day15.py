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


class factory( object ):
    def __init__( self, factory_map: list[str]):
        self.wall_pos = []
        self.rock_pos = []
        self.bot_pos = None
        self.map_size = (len(factory_map[0]), len(factory_map))

        for y, row in enumerate(factory_map):
            for x, obj in enumerate(row):
                position = (x,y)
                if obj == "@":
                    self.bot_pos = position
                elif obj == "#":
                    self.wall_pos.append(position)
                elif obj == "O":
                    self.rock_pos.append(position)

    def __repr__(self):
        return_str = ""
        output_map = [["."] * self.map_size[0] for i in range(self.map_size[1])]

        for wall in self.wall_pos:
            output_map[wall[1]][wall[0]] = "#"
        
        for rock in self.rock_pos:
            output_map[rock[1]][rock[0]] = "O"
        
        output_map[self.bot_pos[1]][self.bot_pos[0]] = "@"
        
        for line in output_map:
            return_str += str(line) + "\n"

        return return_str

    def get_next_pos( self, coord:tuple, dir: str ):
        match dir:
            case "<": return (coord[0] - 1, coord[1])
            case "^": return (coord[0], coord[1]-1)
            case "v": return (coord[0], coord[1]+1)
            case ">": return (coord[0] + 1, coord[1])

        assert(False)   # Shouldn't hit

    def move_bot( self, dir: str ):
        next_pos = self.get_next_pos( self.bot_pos, dir )

        if next_pos in self.wall_pos:
            # Nothing to do, bot is running into wall
            return
        
        if next_pos in self.rock_pos:
            # Check if the rocks can slide without hitting wall
            rock_pos = next_pos
            while rock_pos in self.rock_pos:
                next_rock_pos = self.get_next_pos(rock_pos, dir)
                if next_rock_pos in self.wall_pos:
                    # Nothing to do, rock is running into wall
                    return

                rock_pos = next_rock_pos
            
            # Didn't run into wall, thus place a rock in the next position and remove the bot's new position
            self.rock_pos.append(rock_pos)
            self.rock_pos.remove(next_pos)

        self.bot_pos = next_pos

    def calc_gps( self ) -> int:
        gps_sum = 0
        for (x,y) in self.rock_pos:
            gps_sum += 100* y + x

        return gps_sum


def parse_input( input_str: str ) -> tuple[factory, str]:
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
    
    return (factory(factory_str), move_str)

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "test_s":
        inp = test_input_small
    elif len(sys.argv) >= 2 and sys.argv[1] == "test":
        inp = test_input_large
    else:
        inp = open("inputs/day15.txt").read()

    fish_factory, moves = parse_input( inp )

    for move in moves:
        # print(fish_factory)
        # print( move )
        fish_factory.move_bot(move)
    
    print(fish_factory)
    print(f"GPS sum: {fish_factory.calc_gps()}")