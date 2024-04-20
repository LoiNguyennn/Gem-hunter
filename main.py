import fileinput
from itertools import combinations
from pysat.solvers import Solver

DIRECTION = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

def InputBoard():
    board = []
    for line in fileinput.input('input.txt'):
        board.append(line.strip().split(', '))
    return board

def SurroundingCells(board, x, y):
    surrounding_cells = []
    for dir in DIRECTION:
        x1 = x + dir[0]
        y1 = y + dir[1]
        if x1 >= 0 and x1 < len(board) and y1 >= 0 and y1 < len(board[0]):
            surrounding_cells.append((x1, y1))
    return surrounding_cells
        
def CellID(board, cell):
    return cell[0] * len(board[0]) + cell[1] + 1

def GenerateDNFs(board):
    clauses = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != '_':
                clauses.append([-CellID(board, (i, j))])

                surrounding_cells = SurroundingCells(board, i, j)
                for combination in combinations(surrounding_cells, int(board[i][j])):
                    clause = []
                    for cell in surrounding_cells:
                        cell_id = CellID(board, cell)
                        if cell in combination:
                            clause.append(cell_id)  # cell is a trap
                        else:
                            clause.append(-cell_id)  # cell is not a trap
                    clauses.append(clause)
               
    return clauses

def distribute_and_over_or(terms):
    result = [[]]
    for term in terms:
        new_result = []
        for clause in result:
            for literal in term:
                new_clause = clause.copy()
                new_clause.append(literal)
                new_result.append(new_clause)
        result = new_result
    return result

def dnf_to_cnf(dnf):
    cnf = []
    for clause in distribute_and_over_or(dnf):
        cnf.append(clause)
    return cnf

if __name__ == '__main__':
    board = InputBoard()
    dnfs = GenerateDNFs(board)
    cnfs = []
    #print dnf clauses to output.txt
    with open('output.txt', 'w') as f:
        for clause in dnfs:
            f.write(str(clause) + '\n')
    # Convert DNF to CNF
    cnfs = dnf_to_cnf(dnfs)
    #print cnf expression to output.txt
    with open('output.txt', 'a') as f:
        f.write(cnfs)