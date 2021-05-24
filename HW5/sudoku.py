# ----------------------------------------------------------------------
# Name:     sudoku
# Purpose:  Homework5
# Author(s): Dai Le, Ngan Luu
# ----------------------------------------------------------------------
"""
Sudoku puzzle solver implementation

q1:  Basic Backtracking Search
q2:  Backtracking Search with AC-3
q3:  Backtracking Search with MRV Ordering and AC-3
"""
import csp

# Enter your helper functions here
numbers = list(range(0, 9))

def combine(list1, list2):
    """
    Combine two lists with each element of list1 takes 
    turn to combine with every element of list2
    :param: list1: first list
            list2: second list
    :return: a list containing possibilities such that each element of list1 takes 
    turn to combine with every element of list2
    """
    combined_list = []
    for i in list1:
        for j in list2:
            combined_list.append((i,j))
    return combined_list


def check_constraint(var1, value1, var2, value2):
    """ 
    Checks if 2 variables satisfy the constraint. 
    Return True if variable 1's value is different from variable 2's value
    :param: var1: variable 1
            value1: variable 1's value
            var2: variable 2
            value2: variable 2's value
    :return: True or False
    """
    return value1 != value2

def get_neighbors(cells):
    """ 
    Returns a dictionary with with keys are the cell and 
    values containing the list of keys' corresponding neighbors
    Neighbors of a cell are all other cells in the same row, column, and box (eliminate repeated cells)
    :param cells: list of all possible cells generated
    :return: neighbors dictionary
    """
    neighbors = {}      # dictinary storing cells and their corresponding neighbors building 9 big boxes, each box contains 9 cells
    boxes = [combine(row, col) for row in ([0, 1, 2], [3, 4, 5], [6, 7, 8]) for col in ([0, 1, 2], [3, 4, 5], [6, 7, 8])]
    for cell in cells:
        (row, col) = cell
        # list of all other cells in the same column of a particular cell
        col_neighbors = [(num, col) for num in numbers if num != row]
        # list of all other cells in the same row of a particular cell
        row_neighbors = [(row, num) for num in numbers if num != col]
        for box in boxes:
            if cell in box:
                # list of all other cells in the same box of a particular cell
                box_neighbors = [b for b in box if (b != cell) and (b not in col_neighbors) and (b not in row_neighbors)]
                # adding all neighbors to the dictionary with key is the cell and value containing the list of its neighbors
                neighbors[cell] = col_neighbors + row_neighbors + box_neighbors
                break
    return neighbors

def build_csp(puzzle):
    """
    Create a CSP object representing the puzzle.
    :param puzzle (dictionary): The dictionary keys are tuples
    (row, column) representing the filled puzzle squares and the values
    are the corresponding numbers assigned to these squares.
    :return: CSP object
    """
    cells = combine(numbers, numbers)
    domains = {cell: [int(puzzle[cell])] if cell in puzzle else list(range(1, 10)) for cell in cells}
    neighbors = get_neighbors(cells)

    return csp.CSP(domains, neighbors, check_constraint)


def q1(puzzle):
    """
    Solve the given puzzle with basic backtracking search
    :param puzzle (dictionary): The dictionary keys are tuples
    (row, column) representing the filled puzzle squares and the values
    are the corresponding numbers assigned to these squares.
    :return: a tuple consisting of a solution (dictionary) and the
    CSP object.
    """
    sudoku = build_csp(puzzle)
    result = (sudoku.backtracking_search(), sudoku)
    return result

def q2(puzzle):
    """
    Solve the given puzzle with backtracking search and AC-3 as
    a preprocessing step.
    :param puzzle (dictionary): The dictionary keys are tuples
    (row, column) representing the filled puzzle squares and the values
    are the corresponding numbers assigned to these squares.
    :return: a tuple consisting of a solution (dictionary) and the
    CSP object.
    """
    sudoku = build_csp(puzzle)
    sudoku.ac3_algorithm()
    result = (sudoku.backtracking_search(), sudoku)
    return result

def q3(puzzle):
    """
    Solve the given puzzle with backtracking search and MRV ordering and
    AC-3 as a preprocessing step.
    :param puzzle (dictionary): The dictionary keys are tuples
    (row, column) representing the filled puzzle squares and the values
    are the corresponding numbers assigned to these squares.
    :return: a tuple consisting of a solution (dictionary) and the
    CSP object.
    """
    # Enter your code here and remove the pass statement below
    #pass
    sudoku = build_csp(puzzle)
    sudoku.ac3_algorithm()
    result = (sudoku.backtracking_search("MRV"), sudoku)
    return result
