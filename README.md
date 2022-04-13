
# A* 8-puzzle, Genetic Algorithm Sudoku Solver

This project is what was submitted for my second year AI module at the University of Exeter. It consisted of two main sections, an A* 8-puzzle solver section and a Genetic algorithm section.

## 8-puzzle solver using A* search

In my 8-puzzle implementation (A_star_8_Puzzle.py) I represented the puzzle as a 9 item list (with numbers 0-8, 0 represents the empty slot)

I implemented A* search using two heuristics: manhattan distance and the count of misplaced tiles. Manhattan was a much better heuristic in my code. I used a test list of [1, 2, 7, 6, 0, 4, 8, 3, 5] which was solved in 649 iterations with manhattan and 4109 iterations with the missing tiles heuristic. Both ended up using the same steps with the same final f cost produced (14)

You can solve an example puzzle to be solved by running the q1_2_3() method, you can also input your own original puzzle and target puzzle by running the q1_3() method.

## Genetic algorithm Sudoku Solver

As of when I am writing this I haven't gotten round to optimising my code and as such most configurations take up to 45 mins to process.

My working (but not optimised) code can be found in the Sudoku_evolutionary_algorithm.py file.

It is currently setup to have a population of 10000 and to run based on the Grid1.ss file, however you can change the variables at the bottom of the file (truncation_rate, mutation_rate, population_size, generation_limit, provided_file) to optimise/run the file as needed.


- I represented Sudoko puzzles as a list of lists, with each list representing a row of 'cells'. Each 'cell' corresponds to a position on the Sudoko puzzle. Each 'candidate' will represent a potential completed Sudoko puzzle, and these candidates will make up the defined population size.
- The solution space is the set of all possible numbers, initial imperfect solutions can be represented by their score, the final results can be represented as a 2d array of the completed sudoko.
- I used the sum of the repeats per subgrid, column and row, to make a function to measure how good/bad a candidate is doing.
- As my crossover function I created two new child candidates from productive parent candidates using uniform crossover, where at random, a random cell is either taken or not taken from one of the parents.
- For the mutation operator, it will randomly swap two legal cells in random rows, this will only occur in a certain amount of candidates as defined by a mutation rate.
- Initially, find what numbers can go in each cell, then, in all non given cells, put random numbers from the calculated suitable numbers. Produce as many of these candidates as is specified.
- The program terminates when fitness function yields a perfect score, or when the generation count gets too high 

## License
[MIT](https://choosealicense.com/licenses/mit/)
