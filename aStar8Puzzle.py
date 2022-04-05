from random import shuffle, random, choice

import numpy as np
from scipy.spatial.distance import cityblock

manhattan = True

class Puzzle:
    """
    A puzzle is a list of 3 lists, which can be translated into a 3
    layer puzzle, the empty spot is represented by a 0
    """

    def __init__(self, puzzle_contents=None, parent=None):

        self.parent = parent
        # g = the number of moves (nodes) that have been done before
        if self.parent is None:
            self.g = 0
        else:
            self.g = parent.g + 1

        self.children = []

        # Does 50 random moves on the solved puzzle (to ensure the produced puzzle is solvable)
        if puzzle_contents is None:
            puzzle_contents = list(range(0, 9))
            puzzle = []
            puzzle.append(puzzle_contents[0:3])
            puzzle.append(puzzle_contents[3:6])
            puzzle.append(puzzle_contents[6:9])
            self.puzzle = puzzle
            for i in range(50):
                legal_moves = self.legal_moves()
                move_to_do = choice(legal_moves)
                self.puzzle = (self.move(move_to_do[1], move_to_do[2])).puzzle

        else:
            puzzle = []
            puzzle.append(puzzle_contents[0:3])
            puzzle.append(puzzle_contents[3:6])
            puzzle.append(puzzle_contents[6:9])
            self.puzzle = puzzle

    def __str__(self):
        to_string = ""
        for row in self.puzzle:
            for number in row:
                if number == 0:
                    number = "_"
                to_string += str(number) + " "
            to_string += "\n"
        return to_string

    @property
    def is_solved(self):
        if sum(self.puzzle, []) == [0, 1, 2, 3, 4, 5, 6, 7, 8]:
            return True
        else:
            return False

    @property
    def puzzle_2d(self):
        puzzle = sum(self.puzzle, [])
        puzzle_2d = np.array([[puzzle[0], puzzle[1], puzzle[2]],
                              [puzzle[3], puzzle[4], puzzle[5]],
                              [puzzle[6], puzzle[7], puzzle[8]]])
        return puzzle_2d

    @property
    def manhattan_distance(self):
        """
        Uses scipy's cityblock module to calculate manhattan distance
        values, used for heuristics
        :return: The manhattan distance
        """

        solved = np.array([[0, 1, 2],
                           [3, 4, 5],
                           [6, 7, 8]])

        original = self.puzzle_2d
        distance = 0
        for number in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
            og_pos = (np.asarray(np.where(original == number)).T.tolist())[0]
            solved_pos = (np.asarray(np.where(solved == number)).T.tolist())[0]
            distance += cityblock(og_pos, solved_pos)

        return distance

    @property
    def misplaced_tiles(self):
        """
        Checks how many misplaced tiles there are, used for heuristics
        :return: The misplaced tile count
        """
        solved_puzzle = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        puzzle = sum(self.puzzle, [])
        misplaced_tiles = 0
        for i in range(len(solved_puzzle)):
            if puzzle[i] != solved_puzzle[i]:
                misplaced_tiles += 1
        return misplaced_tiles

    @property
    def h(self):
        if manhattan:
            return self.manhattan_distance
        else:
            return self.misplaced_tiles

    @property
    def f(self):
        return str(self.g + self.h)

    def find_position(self, number):
        position = 0
        puzzle = sum(self.puzzle, [])
        while puzzle[position] != number:
            position += 1
            if position > 8:
                raise Exception(number + "not found in puzzle")
        return position

    def legal_moves_for_number(self, number):
        """
        Returns the moves that a number can make in the puzzle's current configuration
        :param number: The number to move
        :return: The moves that the number's spot is allowed to make
        """
        valid_moves_list = ['up', 'down', 'right', 'left']
        position = self.find_position(number)

        puzzle = sum(self.puzzle, [])
        if position in [0, 3, 6] or puzzle[position - 1] != 0:
            valid_moves_list.remove('left')
        if position in [2, 5, 8] or puzzle[position + 1] != 0:
            valid_moves_list.remove('right')
        if position in [6, 7, 8] or puzzle[position + 3] != 0:
            valid_moves_list.remove('down')
        if position in [0, 1, 2] or puzzle[position - 3] != 0:
            valid_moves_list.remove('up')

        return valid_moves_list

    def legal_moves(self):
        """
        Returns the legal moves that can be done to solve the puzzle, also create child nodes for possible moves
        :return: A list of moves that are allowed
        """
        temp_list = []
        for number in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
            if self.legal_moves_for_number(number):
                for move in self.legal_moves_for_number(number):
                    # Calculate f value for this movement
                    new_puzzle = self.move(int(number), move)
                    f_value = new_puzzle.f
                    temp_list.append([f_value, number, move])
                    # self.children.append(self.move(number, move))

        # print("Moves for " + str(self.puzzle))
        # print(temp_list)
        # print("Children for " + str(self.puzzle))
        # for child in self.children:
        #    print(child.puzzle)
        return temp_list

    def move(self, number, direction):
        """
        Creates a new puzzle object with the specified number being swapped with a zero value
        Assumes that the program has chosen a number which can be moved
        """
        position = self.find_position(number)
        puzzle_list = sum(self.puzzle, [])

        if direction == "left":
            puzzle_list[position - 1] = number
        elif direction == "right":
            puzzle_list[position + 1] = number
        elif direction == "down":
            puzzle_list[position + 3] = number
        elif direction == "up":
            puzzle_list[position - 3] = number
        else:
            raise Exception(direction + "is not a valid direction")
        puzzle_list[position] = 0

        return Puzzle(puzzle_list, self)


def successors(puzzle):
    successors = str(puzzle)
    while puzzle.parent is not None:
        puzzle = puzzle.parent
        successors = str(puzzle) + "  ↓\n" + successors
    return successors


class Solver:
    def __init__(self, original_puzzle, goal_puzzle=None):
        self.original_puzzle = original_puzzle
        if goal_puzzle is None:
            self.goal_puzzle = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        else:
            self.goal_puzzle = goal_puzzle
        self.open = []
        self.closed = []

    def solve(self):
        self.open.append(self.original_puzzle)
        iteration = 0

        current_puzzle = self.original_puzzle

        while sum(current_puzzle.puzzle, []) != self.goal_puzzle:
            # print(sum(current_puzzle.puzzle, []))
            # print(self.goal_puzzle)

            current_puzzle = self.open[0]
            self.open.pop(0)
            self.closed.append(sum(current_puzzle.puzzle, []))

            moves = current_puzzle.legal_moves()
            # print(moves)
            children = []
            for move in moves:
                temp = current_puzzle.move(move[1], move[2])
                children.append(temp)

            for child in children:
                if child.puzzle in self.closed:
                    continue
                if child.puzzle not in self.open:
                    self.open.append(child)

            self.open = sorted(self.open, key=lambda puzzle: int(puzzle.f), reverse=False)
            iteration += 1

        print(successors(current_puzzle))
        print("Puzzle solved in " + str(iteration) + " iterations")
        print("Final f cost:", current_puzzle.f)
        if manhattan:
            print("Using Manhattan as heuristic")
        else:
            print("Using misplaced tiles as heuristic\n")


def q1_2_3():
    # Sets the heuristic to Manhattan
    global manhattan
    manhattan = True

    # Creates a random puzzle (solved puzzle having had 50 random moves applied to it)
    puzzle = Puzzle([1, 2, 7, 6, 0, 4, 8, 3, 5])
    # Remove # below to generate a random puzzle, for comparison reasons I have left in a default puzzle
    # puzzle = Puzzle()

    Solver(puzzle).solve()

    # Sets the heuristic to missing tiles
    manhattan = False
    puzzle = Puzzle([1, 2, 7, 6, 0, 4, 8, 3, 5])

    Solver(puzzle).solve()


def q1_3():
    global manhattan
    manhattan = True

    inputPuzzle = input(
        "Please enter in the numbers you would like to use for the puzzle, you must enter 9 numbers, 0-8, only using each one once and separating them by a"
        "space\n eg. If you enter '0 1 2 3 4 5 6 7 8', you will create a puzzle that looks like this: \n"
        "_ 1 2\n"
        "3 4 5\n"
        "6 7 8")

    puzzleList = list(inputPuzzle.split())
    puzzleList = list(map(int, puzzleList))

    inputGoal = input("In the same format as above, please enter the goal state you'd like the puzzle to reach")

    goalList = list(inputGoal.split())
    goalList = list(map(int, goalList))

    puzzle = Puzzle(puzzleList)
    Solver(puzzle, goalList).solve()
