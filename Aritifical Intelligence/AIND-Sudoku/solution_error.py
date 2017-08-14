assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    """ Cross product of elements in A and elements in B. """
    # As seen before on utils
    cross_prod = [x+y for x in A for y in B]
    return cross_prod

# As seen before on utils:
# Define boxes (each cell)
boxes = cross(rows, cols)
# Define row units
row_units = [cross(r, cols) for r in rows]
# Define column units
column_units = [cross(rows, c) for c in cols]

# Define square units
# a `unit` is defined as each column, row, diagonal or 3x3 grid square
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# Define diagonal units
diagonal_units = [[x+y for x, y in zip(rows, cols)], [x+y for x, y in zip(rows, cols[::-1])]]
# Create a list of all units
unitlist = row_units + column_units + square_units + diagonal_units
# Create a dictionary of peers of each box. A peer is any cell from the same unit
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    #check for already solved values (length is one) and updating dictionary.
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        values(dict): the values dictionary with the naked twins eliminated from peers.
    """
    # Create naked twins dictionary.
    naked_twin_dict = {}
    for unit in unitlist:
        t_dict = {}
        for box in unit:
            # Naked twins have two possible values as belong to the same unit
            if len(values[box]) == 2:
                if not values[box] in t_dict:
                    t_dict[values[box]] = [box]
                else:
                    t_dict[values[box]].append(box)
        # Examine the dictionary to validate the candidates present as
        # naked twin pairs
        for key in t_dict:
            # Condition for the candidate to be a naked twin pair
            if len(t_dict[key]) == 2:
                if not key in naked_twin_dict:
                    naked_twin_dict[key] = [unit]
                else:
                    naked_twin_dict[key].append(unit)

    # Eliminate the naked twins as possibilities for their peers
    for key in naked_twin_dict:
        for unit in naked_twin_dict[key]:
            for box in unit:
                if values[box] != key:
                    assign_value(values, box, values[box].replace(key[0], ''))
                    assign_value(values, box, values[box].replace(key[1], ''))
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    sudoku_grid = {}
    for val, key in zip(grid, boxes):
        if val == '.':
            sudoku_grid[key] = '123456789' #if empty, all digits
        else: #if not empty, the value
            sudoku_grid[key] = val
    return sudoku_grid

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    #print the separatos por units and fill in
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Args:
        values(dict): A sudoku in dictionary form.
    Returns:
        evalues(dict): The resulting sudoku in dictionary form.
    """
    evalues = values.copy()
    for box in values:
        if len(values[box]) == 1:
            for p in peers[box]:
                assign_value(evalues, p, evalues[p].replace(values[box], ''))
    return evalues


def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Args:
        values(dict): A sudoku in dictionary form.
    Returns:
        values(dict): The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    """ Iterate eliminate(), naked_twins() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Args:
        values(dict): A sudoku in dictionary form.
    Returns:
        values(dict): The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = naked_twins(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        # If at some point, there is a box with no available values, return False.If the sudoku is solved, return the sudoku.
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """ Using depth-first search and constraint propagation, try all possible values.
    Args:
        values(dict): A sudoku in dictionary form.
    Returns:
        The values dictionary containing a solved sudoku or False if sudoku could not be solved
    """
    values = reduce_puzzle(values)
    if values is False:
        return False
    #if all values set are lenght q the sudoku is already solved
    if all(len(values[s]) == 1 for s in boxes):
        return values
    # if not, find the smallest value set lenght and iterate
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)
    return values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
