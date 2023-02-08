'''
Trisha Mae Beleta
Unblock Me Puzzle solver using Depth Limited Search
CSC171 Introduction to Artificial Intelligence: Research Project

References: 
     DLS implementation   : (pseudocode)  https://github.com/aimacode/aima-pseudocode/blob/master/md/Depth-Limited-Search.md (from book: http://aima.cs.berkeley.edu/ )
                            (python code) https://github.com/AshishBora/unblock-me-solver < -- breadth-first search (but one block/square per move)
                                          https://github.com/pard1s/rush-hour <- iterative depth first search
    Puzzle representation : https://www.dc.fi.udc.es/~cabalar/kr/current/ex2.html
                            https://github.com/karakanb/unblock-me-solver
'''

import copy

# Define the Node
class Node:
    def __init__(self, puzzle):
        self.puzzle = copy.deepcopy(puzzle)
        self.parent = None
        self.depth = 0
        self.identify_blocks()

    # identify block properties like ( name/identifier , row and column position, length, orientation)
    def identify_blocks(self):
        block = set()
        length = {}
        row_position = {}
        col_position = {}
        orientation = {}

        # add all elements from the puzzle into the block
        for i in self.puzzle:
            for j in i:
                block.add(j)
        # remove blank elements (the periods) 
        block.remove('.')

        for element in block: # block = set of all block identifiers in the puzzle
            count = 1
            changed_orientation = False
            for i in self.puzzle:
                for j, value in enumerate(i):
                    if value == element:
                        if count == 1:
                            # set block row and column position
                            row_position[element] = self.puzzle.index(i)
                            col_position[element] = j
                        else:
                            # set block length
                            length[element] = count

                        count += 1

                        # set block orientation -- vertical / horizontal
                        if changed_orientation:
                            orientation[element] = 'v'
                        else:
                            orientation[element] = 'h'
                if count > 1:      
                    # meaning squares of same name are on different rows -- block is vertical
                    changed_orientation = True
        
        #define block properties
        self.block = block   # set of all block identifiers (letters)
        self.length = length # set of all block identifier w/ their correspinding length
        self.row_position = row_position  # set of all block identifier w/ their correspinding x_position (if vertical block -- topmost)
        self.col_position = col_position # set of all block identifier w/ their correspinding  y_position (if horizontal -- leftmost)
        self.orientation = orientation # set of all block identifier w/ their correspinding orientation (h -> horizontal ; v -> vertical)

    # check if prisoner block already reached the goal
    def goal_test(self):
        if self.orientation['x'] == 'h':
            if self.col_position['x'] + self.length['x'] == len(self.puzzle[0]):
                return True
        return False

    def __eq__(self, other):
        return isinstance(other, Node) and self.puzzle == other.puzzle and self.row_position == other.row_position and self.col_position == other.col_position and self.block == other.block and self.length == other.length and self.orientation == other.orientation
    
    def __hash__(self):
        return hash((tuple(i) for i in self.puzzle))


# create new set of puzzle configurations
def expand(parent):
    children = []
    for child in parent.block:

        if parent.orientation[child] == 'h':                
            # Move to right
            puzzle_f = copy.deepcopy(parent.puzzle)   
            i = parent.row_position[child]
            j = parent.col_position[child]
            c = parent.col_position[child] + parent.length[child]
            dots = 0
            while c < len(parent.puzzle[0]) and parent.puzzle[i][c] == '.':
                dots += 1
                c += 1
            if(dots >= 1):
                for x in range(dots):
                    for l in range(parent.length[child] - 1, -1, -1):
                        puzzle_f[i][j+l+1] = child
                        puzzle_f[i][j+l] = '.'
                    j += 1
                new_s = Node(puzzle_f)
                new_s.parent = parent
                new_s.depth = parent.depth + 1
                children.append(new_s)
                
            # Move to left
            puzzle_b =  copy.deepcopy(parent.puzzle)     
            i = parent.row_position[child]
            j = parent.col_position[child]
            c =  parent.col_position[child] - 1
            dots = 0
            while c >= 0 and parent.puzzle[i][c] == '.':  
                dots += 1
                c -= 1
            if(dots >= 1):
                for x in range(dots):
                    for l in range(parent.length[child]):
                        puzzle_b[i][j+l-1] = child
                        puzzle_b[i][j+l] = '.'
                    j -= 1
                new_s = Node(puzzle_b)
                new_s.parent = parent
                new_s.depth = parent.depth + 1
                children.append(new_s)

        elif parent.orientation[child] == 'v':

            # Move Downward
            puzzle_d =  copy.deepcopy(parent.puzzle)   
            i = parent.row_position[child]
            j = parent.col_position[child]
            c =  parent.row_position[child] + parent.length[child]
            dots = 0
            while c < len(parent.puzzle) and parent.puzzle[c][j] == '.':
                dots += 1
                c += 1
            if(dots >= 1):
                for x in range(dots):
                    for l in range(parent.length[child] - 1, -1, -1):
                        puzzle_d[i+l+1][j] = child
                        puzzle_d[i+l][j] = '.'
                    i += 1
                new_s = Node(puzzle_d)
                new_s.parent = parent
                new_s.depth = parent.depth + 1
                children.append(new_s)

            # Move upward
            puzzle_u = copy.deepcopy(parent.puzzle)    
            i = parent.row_position[child]
            j = parent.col_position[child]
            c =  parent.row_position[child] - 1
            dots = 0
            while c >= 0 and parent.puzzle[c][j] == '.':  
                dots += 1
                c -= 1
            if(dots >= 1):
                for x in range(dots):
                    for l in range(parent.length[child]):
                        puzzle_u[i + l - 1][j] = child
                        puzzle_u[i + l][j] = '.'
                    i -= 1
                new_s = Node(puzzle_u)
                new_s.parent = parent
                new_s.depth = parent.depth + 1
                children.append(new_s)

    return children


# Depth limited Search
def depth_limited_search(puzzle, l):         # returns a solution, failure, or cutoff

    print("\nSolving...Please Wait...")
    frontier = []
    frontier.append(puzzle)
    result = None

    while len(frontier) != 0:
        parent = frontier.pop()

        if parent.depth > l:
            result = 'cutoff'
        else:
            children = expand(parent)
            for child in children:
                if child.goal_test():
                    return child
                frontier.append(child)
    return result

# Prints Solutions by backtracking
def solution(goal):
    path = []
    path.append(goal)
    parent = goal.parent
    while parent:
        if parent not in path:
            path.append(parent)
        parent = parent.parent
    i = 1
    while i <= len(path):
        parent_2 = path[len(path) - i]
        print("Move #", i , "\n")
        i += 1
        for element in parent_2.puzzle:
            print(element , "\n")

# Run code 
def main():

    print('\n══════════════════ Unblock Me Puzzle Solver ══════════════════')
    print('\nPrisoner block should be marked as x.\nEnter Puzzle below:')

    # Puzzle Input
    input_puzzle = ""
    for i in range(6):
        input_puzzle+=input()+"\n"
    puzzle_array = [list(line) for line in input_puzzle.strip().splitlines()]

    # Defining the problem
    problem = Node(puzzle_array)

    # Solving
    goal = depth_limited_search(problem, 50)

    # Printing of Solution
    if goal == 'cutoff'or goal == None:
        print('\nFAILED: Max Depth Reached. No solution found. Try increasing depth limit.')
    else:
        solution(goal)

if __name__ == '__main__':
    main()