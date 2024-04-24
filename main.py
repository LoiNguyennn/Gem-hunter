import fileinput
from itertools import combinations
from pysat.solvers import Glucose3
import random
import pygame
import sys

TILE_SIZE = 70
GOLD_COLOR = (255, 255, 204)
TRAP_COLOR = (153, 255, 204)
BLANK_COLOR = (179, 175, 249)

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

def convertResult(answer, board):
    size = len(board[0])
    result = []
    for i in range(len(board)):
        line = []
        for j in range(size):
            if board[i][j] != '_':
                element = board[i][j]
            else:
                if (answer[i * len(board[0]) + j]):
                    element = 'T'
                else:
                    element = 'G'

            line.append(element)
        result.append(line)
    return result

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

def walksat(board, clauses, p=0.5, max_flips=10000):
    # Initialize a random assignment
    assignment = {}
    list_num = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != '_':
                assignment[(i * len(board[0]) + j) + 1] = False
            else:
                assignment[(i * len(board[0]) + j) + 1] = random.choice([True, False])
                list_num.append(i * len(board[0]) + j)
    assignment = list(assignment.values())
    print("Initial random assignment:", assignment)
    for i in range(max_flips):
        # Select an unsatisfied clause 
        unsatisfied = [c for c in clauses if not satisfies(c,assignment)]
        if not unsatisfied: 
            return assignment
        
        clause = random.choice(unsatisfied)
        
        # With probability p, flip a random variable 
        if random.random() < p:
            var = random.choice(list_num)
        else:
            # Otherwise, flip var that maximizes no. of satisfied clauses
            var = choose_var(clause, assignment)
        
        assignment[var] = not assignment[var]
        
    return None # Failed to satisfy

def satisfies(clause, assignment):
    for x in clause:
        if assignment[abs(x) - 1] == (x > 0):
            return True

    return False

def choose_var(clause, assignment):
    # Flip var that minimizes no. of broken clauses
    min_broken = len(clause) + 1
    var = None
    for x in clause:
        if x > 0:
            tmp = assignment[:]
            tmp[abs(x)-1] = False
        else:
            tmp = assignment[:]
            tmp[abs(x)-1] = True
            
        # clause is a single literal, so broken is 0 or 1
        if not satisfies(clause, tmp):
            broken = 1 
        else:
            broken = 0

        if broken < min_broken:
            min_broken = broken
            var = abs(x) - 1
    return var

def GetAnswer(board):
    cnfs = []
    existed = set() # remove duplicate
    for i in range(len(board)):
        for j in range(len(board[0])):
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
    num_variables = 0
    for cnf in cnfs:
        for clause in cnf:
            clauses.append(clause)
            num_variables = max(num_variables, max(abs(l) for l in clause))
    # solver = Glucose3()
    # for cnf in cnfs:
    #     for clause in cnf:
    #         solver.add_clause(clause)
    
    # if solver.solve():
    #     return solver.get_model()
    assignment = walksat(board, clauses)

    if assignment is None:
        return None
    
    return assignment

def display(_map):
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 22)
    col = len(_map[0])
    row = len(_map)
    win = pygame.display.set_mode((row * TILE_SIZE, col * TILE_SIZE))
    pygame.display.set_caption('Gem Hunter')
    clock = pygame.time.Clock()
    def draw_map():
        for i in range(row):
            for j in range(col):
                if _map[i][j] == 'T':
                   color = TRAP_COLOR
                elif _map[i][j] == 'G':
                    color = GOLD_COLOR
                else:
                    color = BLANK_COLOR
                pygame.draw.rect(win, color, (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2))
                letter = str(_map[i][j])
                text_surface = font.render(letter, True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(j * TILE_SIZE + TILE_SIZE // 2, i * TILE_SIZE + TILE_SIZE // 2))
                win.blit(text_surface, text_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        draw_map()
        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    board = InputBoard()
    print(board)
    answer = GetAnswer(board)

    fo = open('output.txt', 'w')
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != '_':
                fo.write(str(board[i][j]))
            else:
                if (answer[i * len(board[0]) + j]):
                    fo.write('T')
                else:
                    fo.write('G')
            if not (i == len(board) - 1 and j == len(board[0]) - 1):
                if j == len(board[0]) - 1:
                    fo.write("\n")
                else:
                    fo.write(", ")
    fo.close()

    display(convertResult(answer, board))