import sys

test_input = "\
Register A: 729\n\
Register B: 0\n\
Register C: 0\n\
\n\
Program: 0,1,5,4,3,0"

# Register references
A=0
B=1
C=2

class computer(object):
    def __init__(self, registerA:int, programList ):
        self.regs = [registerA,0,0]
        self.instructions = programList
        self.instPointer = 0
        self.output = []

    def get_combo_op( self, operand: int ) -> int:
        if operand <= 3:
            return operand
        return self.regs[operand-4]

    def run_op( self ) -> bool:
        """Returns false when the program is finished"""
        opCode = self.instructions[self.instPointer]
        opVal = self.instructions[self.instPointer+1]
        self.instPointer += 2

        match opCode:
            case 0:
                num = self.regs[A]
                denom = 2 ** self.get_combo_op(opVal)
                self.regs[A] = int(num/denom)
            case 1:
                self.regs[B] = self.regs[B] ^ opVal
            case 2:
                self.regs[B] = self.get_combo_op(opVal) % 8
            case 3:
                if self.regs[A]:
                    # Jump instruction
                    self.instPointer = opVal
            case 4:
                self.regs[B] = self.regs[B] ^ self.regs[C]
            case 5:
                self.output.append(str(self.get_combo_op(opVal)%8))
            case 6:
                num = self.regs[A]
                denom = 2 ** self.get_combo_op(opVal)
                self.regs[B] = int(num/denom)
            case 7:
                num = self.regs[A]
                denom = 2 ** self.get_combo_op(opVal)
                self.regs[C] = int(num/denom)
    
        return self.instPointer < len( self.instructions ) - 1


    def get_ouput( self ) -> str:
        return ",".join(self.output)



def parse_input( inp: str ) -> tuple[int, list[int]]:
    regVal = 0
    programList = []
    for line in inp.splitlines():
        if "Register A" in line:
            regVal = int(line.split(":")[1])
        elif "Program" in line:
            programList = [int(x) for x in line.split(":")[1].split(",")]
    return regVal, programList

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "test":
        inp = test_input
    else:
        inp = open("inputs/day17.txt").read()
    
    registerA, program = parse_input(inp)
    comp = computer(registerA, program)

    while( comp.run_op() ):
        # Wait for the computer to finish its instructions
        pass

    print("Computer output: " + comp.get_ouput())