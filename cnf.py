import fileinput
from itertools import combinations, product
from copy import deepcopy
from pysat.solvers import Glucose3

TILE_SIZE = 70
GOLD_COLOR = (255, 255, 204)
TRAP_COLOR = (153, 255, 204)
BLANK_COLOR = (179, 175, 249)

DIRECTION = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

def InputBoard(filename):
    board = []
    for line in fileinput.input('input/' + filename + '.txt'):
        board.append(line.strip().split(', '))
    return board

def SurroundingCells(board, x, y):
    surrounding_cells = []
    for dir in DIRECTION:
        x1 = x + dir[0]
        y1 = y + dir[1]
        if x1 >= 0 and x1 < len(board) and y1 >= 0 and y1 < len(board[0]) and board[x1][y1] == '_':
            surrounding_cells.append((x1, y1))
    return surrounding_cells
        
def CellID(board, cell):
    return cell[0] * len(board[0]) + cell[1] + 1

def GenerateDNF(board, i, j):
    dnf = []
    surrounding_cells = SurroundingCells(board, i, j)
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

def GenerateTruthTable(dnf_clauses):
    num_variables = len(set([abs(literal) for clause in dnf_clauses for literal in clause]))
    truth_table = []
    for i in range(2 ** num_variables):
        truth_table.append([])
        for j in range(num_variables):
            truth_table[-1].append((i >> j) & 1)
    
    return truth_table

def GenerateCNF(truth_table, dnf_clauses):
    #return an array of True/False values
    cnf = []
    i = 0
    for row in truth_table:
        OR = False
        for clause in dnf_clauses:
            sorted_literal_index = sorted([abs(literal) for literal in clause])

            AND = True
            for literal in clause:
                idx = sorted_literal_index.index(abs(literal))
                AND &= row[idx] if literal > 0 else not row[idx]
            OR |= AND
        if OR == False:
            cnf.append(de_morgan([sorted_literal_index[literal] if truth_table[i][literal] == 1 else -1 * sorted_literal_index[literal] for literal in range(len(truth_table[i]))]))
        i += 1
    return cnf

def de_morgan(clause):
    return [-literal for literal in clause]

def cmp(e):
    return len(e)

def generate_clauses(board):
    row = len(board[0])
    cnfs = []
    existed = set() # remove duplicate
    for i in range(len(board)):
        for j in range(row):
            if board[i][j] != '_':
                dnf = GenerateDNF(board, i, j)
                truth_table = GenerateTruthTable(dnf)
                cnf = GenerateCNF(truth_table, dnf)
                for clause in cnf:
                    if tuple(clause) in existed:
                        cnf.pop(cnf.index(clause))
                    else:
                        existed.add(tuple(clause))
                cnfs.append(cnf)
    
    clauses = []
    for cnf in cnfs:
        for clause in cnf:
            clauses.append(clause)
    
    clauses.sort()
    clauses.sort(key=cmp)

    while len(clauses[0]) == 1:
        for clause in clauses:
            if len(clause) == 1:
                if clause[0] > 0:
                    if clause[0] % row == 0:
                        board[int(clause[0] / row) - 1][row - 1] = 'T'
                    else:
                        board[int(clause[0] / row)][clause[0] % row - 1] = 'T'
                else:
                    if abs(clause[0]) % row == 0:
                        board[int(abs(clause[0]) / row) - 1][row - 1] = 'G'
                    else:
                        board[int(abs(clause[0]) / row)][abs(clause[0]) % row - 1] = 'G'
                clauses.remove(clause)
                tmp = []
                tmp.append(-clause[0])
                for c in clauses:
                    if clause[0] in c:
                        clauses.remove(c)
                    if tmp[0] in c:
                        c.remove(tmp[0])
        clauses.sort()
        clauses.sort(key=cmp)
    return clauses

###Pysat solver####
def PySat(board):
    cnfs = []
    existed = set() # remove duplicate
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != '_':
                dnf = GenerateDNF(board, i, j)
                truth_table = GenerateTruthTable(dnf)
                cnf = GenerateCNF(truth_table, dnf)
                cnf.append([-CellID(board, (i, j))])
                for clause in cnf:
                    if tuple(clause) in existed:
                        cnf.pop(cnf.index(clause))
                    else:
                        existed.add(tuple(clause))
                cnfs.append(cnf)
    solver = Glucose3()
    for cnf in cnfs:
        for clause in cnf:
            solver.add_clause(clause)
    
    if solver.solve():
        assignment = solver.get_model()
        return assignment
    return None