import math
import time
from random import random, choice
import random

import numpy as np


def read_file(file):
    """
    Read an input file and returns a list of rows in a sudoku puzzle, assumes that each number belongs to a "cell", "."
    means an empty cell and "!" means a column separator that can be ignored
    :param file: The input file
    :return: A list of rows in a sudoku puzzle
    """
    sudoku = []
    for line in open(file, 'r'):
        row = []
        for cell in line:
            if cell in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                row.append(int(cell))
            elif cell == '.':
                # Sets non-given cells to zero
                row.append(0)
            else:
                # "!"s are ignored
                pass
        if row != []:
            # ignore "---!---!---" rows
            sudoku.append(row)
    return sudoku


class Sudoku:
    def __init__(self, sudoku_puzzle, population_size=None):
        self.sudoku_puzzle = sudoku_puzzle
        if population_size is None:
            self.population_size = 10000
        else:
            self.population_size = population_size

    def puzzle_np(self, puzzle=None):
        if puzzle is None:
            return np.array(self.sudoku_puzzle)
        else:
            return np.array(puzzle)

    def create_candidate(self, puzzle=None):
        """
        Fills in empty values of a given Sudoku puzzle
        :param puzzle: The given sudoku puzzle
        :return: A filled in sudoku puzzle with unique numbers on each row
        """

        if puzzle is None:
            puzzle = self.puzzle_np()
        else:
            puzzle = self.puzzle_np(puzzle)

        new_puzzle = []
        i = 0

        for row in puzzle:
            numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            # Remove zeros
            row_given_numbers = [i for i in row if i != 0]
            # Remove numbers that have already appeared in the row from number list
            legal_numbers = list(set(numbers).difference(row_given_numbers))
            # print(legal_numbers)

            # Assign numbers to unassigned cells
            for cell in range(len(row)):
                if row[cell] == 0:
                    rand_idx = random.randrange(len(legal_numbers))
                    number = legal_numbers[rand_idx]
                    row[cell] = number
                    legal_numbers.remove(number)
            new_puzzle.append(row.tolist())
            i += 1
        # print(self.fitness(new_puzzle))
        # print(self.puzzle_np(new_puzzle))

        return new_puzzle

    def seed_new_population(self):
        """
        Creates the original population
        :return: A list of created candidates
        """
        candidates = []
        for i in range(self.population_size):
            candidate = self.create_candidate(self.sudoku_puzzle)
            candidates.append(candidate)
        return candidates

    def is_cell_changeable(self, initial_puzzle, x, y):
        """
        Check is a cell was given in the initial puzzle
        :param initial_puzzle: The initial pizzle
        :param x: The row of the position to be checked
        :param y: The column that is being checked
        :return: True/False, depending on if the cell had a given value originally
        """
        initial_puzzle = self.puzzle_np(initial_puzzle)
        initial_puzzle = initial_puzzle == 0
        initial_puzzle[0][0]
        initial_puzzle[1][0]
        return initial_puzzle[x][y]


    def fitness(self, puzzle):
        """
        Calculates the total number of duplicates per row, column and subgrid (lower is better)
        :return: An integer fitness function value for the given puzzle
        """
        # Row
        fitness_row = 0
        # print(puzzle)
        for row in puzzle:
            fitness_row += len(row) - len(set(row))

        # Column
        fitness_column = 0
        puzzle_np = self.puzzle_np(puzzle)
        for column in range(len(puzzle)):
            column = (puzzle_np[:, [column]]).tolist()
            column = sum(column, [])
            fitness_column += len(column) - len(set(column))

        # Subgrid
        fitness_subgrid = 0
        subgrids = []
        subgrids.append(sum((puzzle_np[0:3, 0:3]).tolist(), []))
        subgrids.append(sum((puzzle_np[0:3, 3:6]).tolist(), []))
        subgrids.append(sum((puzzle_np[0:3, 6:]).tolist(), []))
        subgrids.append(sum((puzzle_np[3:6, 0:3]).tolist(), []))
        subgrids.append(sum((puzzle_np[3:6, 3:6]).tolist(), []))
        subgrids.append(sum((puzzle_np[3:6, 6:]).tolist(), []))
        subgrids.append(sum((puzzle_np[6:, 0:3]).tolist(), []))
        subgrids.append(sum((puzzle_np[6:, 3:6]).tolist(), []))
        subgrids.append(sum((puzzle_np[6:, 6:]).tolist(), []))

        for subgrid in subgrids:
            fitness_subgrid += len(subgrid) - len(set(subgrid))

        # Total
        return fitness_row + fitness_column + fitness_subgrid

    def sort_by_f(self, candidates):
        """
        Takes in a list of candidates and outputs the list of candidates sorted by their f value
        :param candidates: The input population
        :return: A sorted list of candidates in the form [f, puzzle list]
        """
        # Create list candidates and their fitness
        candidate_fitness_list = []
        for candidate in candidates:
            fitness = self.fitness(candidate)
            temp = [fitness, candidate]
            candidate_fitness_list.append(temp)

        # Sort candidates by fitness
        candidate_fitness_list.sort(key=lambda x: x[0])

        # Remove f values
        temp = []
        for candidate in candidate_fitness_list:
            temp.append(candidate[1])
        candidate_fitness_list = temp

        return candidate_fitness_list

    def select_best(self, candidates):
        """
        Selects the best candidates from a given list according to the truncation rate
        :param candidates: The list of candidates
        :return: The list of candidates without the ones that weren't selected in the form [puzzle list]
        """
        # Choose best candidates
        candidates_to_keep = math.ceil(population_size - population_size * truncation_rate)
        new_candidate_list = candidates[:candidates_to_keep]

        return new_candidate_list

    def crossover(self, parent_1, parent_2):
        # Choose two random parents from provided population
        child_1 = np.zeros((9, 9))
        child_2 = np.zeros((9, 9))

        for row in range(9):
            for column in range(9):
                if self.is_cell_changeable(self.sudoku_puzzle, row, column):
                    parent = random.choice([1, 2])
                    if parent == 1:
                        child_1[row][column] = parent_1[row][column]
                    else:
                        child_1[row][column] = parent_2[row][column]
                    parent = random.choice([1, 2])
                    if parent == 1:
                        child_2[row][column] = parent_1[row][column]
                    else:
                        child_2[row][column] = parent_2[row][column]
                else:
                    child_1[row][column] = self.puzzle_np()[row][column]
                    child_2[row][column] = self.puzzle_np()[row][column]
        return [self.mutate(child_1.tolist()), self.mutate(child_2.tolist())]

    def mutate(self, child):
        m_rate = mutation_rate * 10
        m = random.randint(1, 10)
        for i in range(2):
            if m > m_rate:
                random_row = random.randint(0, 8)
                random_column = random.randint(0, 8)
                if self.is_cell_changeable(self.sudoku_puzzle, random_row, random_column):
                    child[random_row][random_column] = random.randint(1, 9)
        return child

    def breed(self, mating_pool):
        """
        Breeds two random parents from the mating pool by performing crossover and mutation methods on them
        :param mating_pool: The pool of well performing parents
        :return: A list of children produced
        """
        children_list = []
        while len(children_list) < population_size:
            parents = []
            # Crossover cells from parents
            parents = random.sample(mating_pool, 2)
            children = self.crossover(parents[0], parents[1])

            # Perform random mutations on produced children
            child_1 = self.mutate(children[0])
            children_list.append(child_1)
            child_2 = self.mutate(children[1])
            children_list.append(child_2)
        #print(len(mating_pool))
        #print(len(children_list))
        return children_list

    def evolve(self, population=None):
        """
        Runs all the methods above to create the next generation
        :param population: The provided population (optional)
        :return: The next generation's population (in list form)
        """
        if population is None:
            population = self.seed_new_population()
            print("Generated population")

        # Sort population by f
        population = self.sort_by_f(population)
        #print("Sorted population by fitness")

        # Select best from population
        mating_pool = self.select_best(population)

        #print("Selected best candidates from population")

        # Breed new generation from mating pool
        child_candidates = self.breed(mating_pool)
        child_candidates = self.sort_by_f(child_candidates)

        #print("Successfully bread best candidates")

        # New generation made up of 25% best parents and 75% best children
        quarter = math.ceil(population_size/4)
        three_quarters = math.ceil(population_size * 0.75)
        children = child_candidates[:three_quarters]
        parents = mating_pool[:quarter]

        new_generation = parents + children
        return new_generation


def run():
    print("population_size: " + str(population_size) + "\n" +
          "provided_file: " + provided_file + "\n" +
          "generation_limit: " + str(generation_limit))
    start = time.time()
    generation_number = 0
    optimal_solution_found = False
    original_sudoku = Sudoku(read_file(provided_file), population_size)
    best_candidate = ""
    candidates = original_sudoku.seed_new_population()
    new_generation = original_sudoku.evolve(candidates)
    while generation_number <= generation_limit and not optimal_solution_found:
        new_generation = original_sudoku.evolve(new_generation)
        generation_number += 1
        # print(candidates)
        best_candidate = new_generation[0]
        print("Generation: " + str(generation_number))
        print("Best score for this generation: " + str(original_sudoku.fitness(best_candidate)) + " (lower is better)")
#        print(original_sudoku.puzzle_np(best_candidate))
        print("\n")
        if original_sudoku.fitness(best_candidate) == 0:
            end = time.time()
            optimal_solution_found = True

    if optimal_solution_found:
        print("Optimal solution found in " + str(end-start) + " seconds at generation " + str(generation_number))
        print(original_sudoku.puzzle_np(best_candidate))

    else:
        end = time.time()
        print("Generation limit reached, best solution score:" + str(original_sudoku.fitness(best_candidate)))
        print("Time elapsed: " + str(end-start) + " seconds")
        print(original_sudoku.puzzle_np(best_candidate))


# Global variables
truncation_rate = 0.4
mutation_rate = 0.6
population_size = 100
generation_limit = 50000

population_size = 10000
provided_file = "./grids/Grid1.ss"
run()

"""
for i in range(5):
    # Run tests

    generation_limit = 5000
    population_size = 10000
    provided_file = "./grids/Grid1.ss"
    run()
    provided_file = "./grids/Grid2.ss"
    run()
    provided_file = "./grids/Grid3.ss"
    run()

    population_size = 1000
    provided_file = "./grids/Grid1.ss"
    run()
    provided_file = "./grids/Grid2.ss"
    run()
    provided_file = "./grids/Grid3.ss"
    run()

    generation_limit = 10000
    population_size = 100
    provided_file = "./grids/Grid1.ss"
    run()
    provided_file = "./grids/Grid2.ss"
    run()
    provided_file = "./grids/Grid3.ss"
    run()

    generation_limit = 50000
    population_size = 10
    provided_file = "./grids/Grid1.ss"
    run()
    provided_file = "./grids/Grid2.ss"
    run()
    provided_file = "./grids/Grid3.ss"
    run()"""

