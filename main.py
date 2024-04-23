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

def GenerateTruthTable(dnf_clauses):
    num_variables = len(set([abs(literal) for clause in dnf_clauses for literal in clause]))
    truth_table = []
    for i in range(2 ** num_variables):
        truth_table.append([])
        for j in range(num_variables):
            truth_table[-1].append((i >> j) & 1)
    
    return truth_table

def CheckingTruthTable(truth_table, dnf_clauses):
    #return an array of True/False values
    return [all([any([truth_table[i][abs(literal) - 1] if literal > 0 else not truth_table[i][abs(literal) - 1] for literal in clause]) for clause in dnf_clauses]) for i in range(len(truth_table))]

def de_morgan(clause):
    return [-literal for literal in clause]

def cnf_generator(truth_table, result):
    cnf = []
    for i in range(len(truth_table)):
        if result[i] == False:
            cnf.append(de_morgan([literal + 1 if truth_table[i][literal] == 1 else -(literal + 1) for literal in range(len(truth_table[i]))]))
    return cnf

if __name__ == '__main__':
    board = InputBoard()
    dnfs = GenerateDNFs(board)
    cnfs = []
    truth_table = GenerateTruthTable(dnfs)
    result = CheckingTruthTable(truth_table, dnfs)
    cnfs = cnf_generator(truth_table, result)
    print(cnfs)