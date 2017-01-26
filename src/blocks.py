import sys, re

class BlockWorld:
    def __init__(self):
        self.filename = sys.argv[1]
        self.init_clear = []
        self.init_on = {}
        self.init_block = set()
        self.goal_clear = []
        self.goal_on = {}

    def parse_input(self):
        with open(self.filename, 'r') as f:
            while f.readline() != 'INIT\n':
                pass

            # print("Reading initial conditions")
            content = '.'
            while content != 'GOAL\n':
                content = f.readline()
                split = content.split()
                if len(split) > 0:
                    if split[0] == 'ON':
                        if len(split) == 3:
                            self.init_on[split[1]] = split[2]
                            self.init_block.add(split[1])
                            self.init_block.add(split[2])
                        else:
                            print("Incorrect ON condition")
                            print(split)
                    elif split[0] == 'CLEAR':
                        if len(split) == 2:
                            self.init_clear.append(split[1])
                            self.init_block.add(split[1])
                        else:
                            print("Incorrect CLEAR condition")
                            print(split)
                else:
                    print("len(split) <= 0")


            # print("Reading goal conditions")
            content = '.'
            while content != '':
                content = f.readline()
                split = content.split()
                if len(split) > 0:
                    if split[0] == 'ON':
                        if len(split) == 3:
                            self.goal_on[split[1]] = split[2]
                        else:
                            print("Incorrect ON condition")
                            print(split)
                    elif split[0] == 'CLEAR':
                        if len(split) == 2:
                            self.goal_clear.append(split[1])
                        else:
                            print("Incorrect CLEAR condition")
                            print(split)

            self.init_block.remove('Table')

    def can_move(self, b, x, y, block, clear, on):
        if b in block and y in block and b in clear and y in clear and on[b] == x and b != x and b!= y:
            return True

        return False

    def move(self, b, x, y):
        '''
        Move block B which is currently on top of block X to be on top of block Y.

        PRECONDITIONS:
        b != x != y
        b is block
        y is block
        b is clear
        y is clear
        b is on top of x

        POSTCONDITIONS:
        b is now on top of y
        y is now no longer clear
        x is now clear (if it is not table)
        '''

        return

    def can_move_to_table(self, b, x, block, clear, on):
        if b in block and b in clear and on[b] == x:
            return True

        return False

    def move_to_table(self, b, x):
        '''
        Move block B which is currently on top of block X to the table.

        PRECONDITIONS:
        b is block
        b is clear
        b is on top of x

        POSTCONDITIONS:
        b is now on table
        x is now clear (if it is not table)
        '''

        return

    def solution(self):
        if len(self.goal_on) == 0 and len(self.goal_clear) == 0:
            print("No goal conditions!")
            return



    def run(self):
        self.parse_input()
        self.solution()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 blocks.py <input-file>")
    else:
        bw = BlockWorld()
        bw.run()