import sys, copy

class BlockWorld:
    MOVE_FAIL = 0
    MOVE_SUCCESS = 1
    MOVE_TO_TABLE_FAIL = 2
    MOVE_TO_TABLE_SUCCESS = 3

    def __init__(self):
        self.filename = sys.argv[1]
        self.init_clear = set()
        self.init_on = {}
        self.init_block = set()
        self.goal_clear = set()
        self.goal_on = {}
        self.num_goals = 0

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
                            self.init_clear.add(split[1])
                            self.init_block.add(split[1])
                        else:
                            print("Incorrect CLEAR condition")
                            print(split)

            # print("Reading goal conditions")
            content = '.'
            while content != '':
                content = f.readline()
                split = content.split()
                if len(split) > 0:
                    if split[0] == 'ON':
                        if len(split) == 3:
                            self.goal_on[split[1]] = split[2]
                            self.num_goals += 1
                        else:
                            print("Incorrect ON condition")
                            print(split)
                    elif split[0] == 'CLEAR':
                        if len(split) == 2:
                            self.goal_clear.add(split[1])
                            self.num_goals += 1
                        else:
                            print("Incorrect CLEAR condition")
                            print(split)

            self.init_block.remove('Table')

    def can_move(self, b, x, y, current_clear, current_on):
        '''
        Preconditions:
        b is block
        y is block
        b is clear
        y is clear
        b is on top of x
        b != x != y
        '''

        if b in self.init_block and y in self.init_block and b in current_clear and y in current_clear and \
                        current_on[b] == x and b != x and b!= y:
            return True

        return False

    def move(self, b, x, y, current_clear, current_on):
        '''
        Move block B which is currently on top of block X to be on top of block Y.

        can_move checks Preconditions

        Postconditions:
        b is now on top of y instead of x
        y is now no longer clear
        x is now clear (if it is not table)
        '''

        if self.can_move(b, x, y, current_clear, current_on):
            current_on[b] = y
            current_clear.remove(y)
            if x != 'Table':
                current_clear.add(x)

            print("Move succeeded")
            return self.MOVE_SUCCESS, current_clear, current_on
        else:
            print("Move failed")
            return self.MOVE_FAIL, current_clear, current_on

    def can_move_to_table(self, b, x, current_clear, current_on):
        '''
        Preconditions:
        b is block
        b is clear
        b is on top of x
        '''
        if b in self.init_block and b in current_clear and current_on[b] == x:
            return True

        return False

    def move_to_table(self, b, x, current_clear, current_on):
        '''
        Move block B which is currently on top of block X to the table.

        can_move_to_table checks Preconditions

        Postconditions:
        b is now on table instead of x
        x is now clear (if it is not table)
        '''

        if self.can_move_to_table(b, x, current_clear, current_on):
            current_on[b] = 'Table'
            if x != 'Table':
                current_clear.add(x)

            print("Move_to_table succeeded")
            return self.MOVE_TO_TABLE_SUCCESS, current_clear, current_on
        else:
            print("Move_to_table failed")
            return self.MOVE_TO_TABLE_FAIL, current_clear, current_on

    def goal_check(self, current_clear, current_on):
        if self.goal_clear.issubset(current_clear):
            goal_on_set = set(self.goal_on.items())
            current_on_set = set(current_on.items())
            if goal_on_set.issubset(current_on_set):
                print("GOAL MET")
                return True

        print("GOAL NOT MET")
        return False

    def find_solution(self):
        if len(self.goal_on) == 0 and len(self.goal_clear) == 0:
            print("No goal conditions!")
            return

        if self.goal_check(self.init_clear, self.init_on):
            print("Initial conditions meet goal conditions")

        moves, solution = self.find_shortest_path(self.init_clear, self.init_on)

    def find_shortest_path(self, current_clear, current_on):
        open = []
        closed = []

    def possible_moves(self, current_clear, current_on):
        pass

    def f_score(self, num_moves, current_clear, current_on):
        return num_moves + self.heuristic(current_clear, current_on)

    def heuristic(self, current_clear, current_on):
        return self.num_goals - self.num_goals_met(current_clear, current_on)

    def num_goals_met(self, current_clear, current_on):
        set_clear_diff = self.goal_clear.difference(current_clear)

        goal_on_set = set(self.goal_on.items())
        current_on_set = set(current_on.items())
        set_on_diff = goal_on_set.difference(current_on_set)

        return len(set_clear_diff) + len(set_on_diff)

    def run(self):
        self.parse_input()
        self.find_solution()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 blocks.py <input-file>")
    else:
        bw = BlockWorld()
        bw.run()