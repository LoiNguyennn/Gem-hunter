import fileinput
from itertools import combinations
from pysat.solvers import Glucose3
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
    for i in range(int(len(answer)/size)):
        line = []
        for j in range(size):
            
            if answer[i*size + j] > 0:
                element = 'T'
            elif board[i][j] != '_':
                element = board[i][j]
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
                
    solver = Glucose3()
    for cnf in cnfs:
        for clause in cnf:
            solver.add_clause(clause)
    if solver.solve():
        return convertResult(solver.get_model(), board)
    return None

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
    answer = GetAnswer(board)
    display(answer)