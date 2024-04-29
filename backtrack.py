import fileinput
from itertools import combinations
from copy import deepcopy

DIRECTION = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

def SurroundingBlankCells(board, x, y):
    surrounding_cells = []
    for dir in DIRECTION:
        x1 = x + dir[0]
        y1 = y + dir[1]
        if 0 <= x1 < len(board) and 0 <= y1 < len(board[0]) and board[x1][y1] == '_':
            surrounding_cells.append((x1, y1))
    return surrounding_cells

def CellID(board, cell):
    return cell[0] * len(board[0]) + cell[1] + 1

def GenerateDNF(board, i, j):
    dnf = []
    surrounding_cells = SurroundingBlankCells(board, i, j)
    for combination in combinations(surrounding_cells, int(board[i][j])):
        clause = []
        for cell in surrounding_cells:
            cell_id = CellID(board, cell)
            if cell in combination:
                clause.append(cell_id)  # cell is a trap
            else:
                clause.append(-cell_id)  # cell is not a trap
        dnf.append(clause)  
    return dnf

def check_valid(clauses, assignment: dict):
    if clauses == []:
        return True
    size_clause = len(clauses[0])
    for clause in clauses:
        i = 0
        for lit in clause:
            if abs(lit) in assignment:
                if assignment[abs(lit)] == (lit > 0):
                    i += 1
        if i == size_clause:
            return True
    return False

def DPLL(clauses, symbol, assignment={}):
    if all(check_valid(clause, assignment) for clause in clauses):
        return True, assignment
    if len(symbol) == 0:
        return False, {}

    #get all the literals that not in assignment
    unassigned_symbol = deepcopy(symbol)
    literal = unassigned_symbol.pop()
    new_assignment = deepcopy(assignment)
    new_assignment[abs(literal)] = literal > 0
    result, final_assignment = DPLL(clauses, unassigned_symbol, new_assignment)
    if result:
        return True, final_assignment
    new_assignment = deepcopy(assignment)
    new_assignment[abs(literal)] = literal < 0
    return DPLL(clauses, unassigned_symbol, new_assignment)

def backtrack(board):
    cnfs = []
    existed = set() 
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != '_':
                dnf = GenerateDNF(board, i, j)
                for clause in dnf:
                    if tuple(clause) in existed:
                        dnf.pop(dnf.index(clause))
                    else:
                        existed.add(tuple(clause))
                cnfs.append(dnf)
    
    clauses = []
    for cnf in cnfs:
        for clause in cnf:
            clauses.append(clause)

    assignment = {}
    satisfiable, assignment = DPLL(cnfs, list(set([abs(literal) for clause in clauses for literal in clause])), assignment)
    if satisfiable:
        result = [-1] * (len(board) * len(board[0]))
        for var, value in assignment.items():
            result[var - 1] = value
        return result
    else:
        return None
    
