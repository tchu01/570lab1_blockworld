import sys, copy

class BlockWorld:
    INIT = 'INIT\n'
    GOAL = 'GOAL\n'
    ON = 'ON'
    CLEAR = 'CLEAR'
    TABLE = 'Table'
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
            while f.readline() != self.INIT:
                pass

            content = '.'
            while content != self.GOAL:
                content = f.readline()
                split = content.split()
                if len(split) > 0:
                    if split[0] == self.ON:
                        self.init_on[split[1]] = split[2]
                        self.init_block.add(split[1])
                        self.init_block.add(split[2])
                    elif split[0] == self.CLEAR:
                        self.init_clear.add(split[1])
                        self.init_block.add(split[1])

            content = '.'
            while content != '':
                content = f.readline()
                split = content.split()
                if len(split) > 0:
                    if split[0] == self.ON:
                        self.goal_on[split[1]] = split[2]
                        self.num_goals += 1
                    elif split[0] == self.CLEAR:
                        self.goal_clear.add(split[1])
                        self.num_goals += 1

            self.init_block.remove(self.TABLE)

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
            if x != self.TABLE:
                current_clear.add(x)

            print('Move succeeded')
            return self.MOVE_SUCCESS, current_clear, current_on
        else:
            print('Move failed')
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
            current_on[b] = self.TABLE
            if x != self.TABLE:
                current_clear.add(x)

            print('Move_to_table succeeded')
            return self.MOVE_TO_TABLE_SUCCESS, current_clear, current_on
        else:
            print('Move_to_table failed')
            return self.MOVE_TO_TABLE_FAIL, current_clear, current_on

    def goal_check(self, current_clear, current_on):
        if self.goal_clear.issubset(current_clear):
            goal_on_set = set(self.goal_on.items())
            current_on_set = set(current_on.items())
            if goal_on_set.issubset(current_on_set):
                print('Goal_check MET')
                return True

        print('Goal_check NOT MET')
        return False

    def num_goals_met(self, current_clear, current_on):
        set_clear_diff = self.goal_clear.difference(current_clear)

        goal_on_set = set(self.goal_on.items())
        current_on_set = set(current_on.items())
        set_on_diff = goal_on_set.difference(current_on_set)

        return len(set_clear_diff) + len(set_on_diff)

    def possible_moves(self, current_clear, current_on):
        ret = []
        for block1 in current_clear:
            for block2 in self.init_block:
                if self.can_move(block1, current_on[block1], block2, current_clear, current_on):
                    move = 'M ' + block1 + ' ' + current_on[block1] + ' ' + block2
                    ret.append(move)

            if self.can_move_to_table(block1, current_on[block1], current_clear, current_on):
                move = 'MTT ' + block1 + ' ' + current_on[block1]
                ret.append(move)

        return ret



    def find_solution(self):
        print('Starting: find_solution')
        if len(self.goal_on) == 0 and len(self.goal_clear) == 0:
            print('No goal conditions!')
            return

        if self.goal_check(self.init_clear, self.init_on):
            print('Initial conditions meet goal conditions')

        open = []
        close = []
        num_moves = 0
        print('Finding shortest path...')
        print()
        moves, solution = self.find_shortest_path(self.init_clear, self.init_on, open, close, num_moves)

    def find_shortest_path(self, current_clear, current_on, open, close, num_moves):
        moves = self.possible_moves(current_clear, current_on)
        print('Current num_moves: ' + str(num_moves) + ' | possible moves: ' + str(moves))
        children = {}
        for move in moves:
            child_clear = copy.deepcopy(current_clear)
            child_on = copy.deepcopy(current_on)
            child_open = copy.deepcopy(open)
            child_close = copy.deepcopy(close)

            split = move.split()
            if split[0] == 'M':
                if self.can_move(split[1], split[2], split[3], current_clear, current_on):
                    self.move(split[1], split[2], split[3], child_clear, child_on)

            if split[0] == 'MTT':
                if self.can_move_to_table(split[1],split[2], current_clear, current_on):
                    self.move_to_table(split[1], split[2], child_clear, child_on)

            child_close.append(move)
            children[move] = (self.f_score(num_moves + 1, child_clear, child_on), child_clear, child_on, child_open, child_close)

        return None, None



    def f_score(self, num_moves, current_clear, current_on):
        return num_moves + self.heuristic(current_clear, current_on)

    def heuristic(self, current_clear, current_on):
        return self.num_goals - self.num_goals_met(current_clear, current_on)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 blocks.py <input-file>")
    else:
        bw = BlockWorld()
        bw.parse_input()
        bw.find_solution()