from pysat.solvers import Glucose3
from backtrack import *
from cnf import *
from optimal import *
from bruteforce import *
import time
import pygame
import sys


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

###Brute force algorithm###    

###GET RESULT###
def getAnswer(board, function):
    puzzle = deepcopy(board)
    answer = convertResult(function(puzzle), puzzle)
    return answer

def convertResult(assignment, board):
    result = [['G' for _ in range(len(board[0]))] for _ in range(len(board))]
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != '_':
                result[i][j] = board[i][j]
            else:
                if assignment[i * len(board[0]) + j] > 0:
                    result[i][j] = 'T'
    return result

def displayResult(_map):
    pygame.init()
    pygame.font.init()
    col = len(_map[0])
    row = len(_map)
    tile_size = min(70, 800//col)
    font = pygame.font.SysFont('Arial', 22)
    win = pygame.display.set_mode((col * tile_size, row * tile_size))
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
                pygame.draw.rect(win, color, (j * tile_size, i * tile_size, tile_size - 2, tile_size - 2))
                letter = str(_map[i][j])
                text_surface = font.render(letter, True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(j * tile_size + tile_size // 2, i * tile_size + tile_size // 2))
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
    board = InputBoard("input50x50")
    i = deepcopy(board)
    # print(board)
    runtime = time.time()
    answer_py = getAnswer(board, PySat)
    runtime = time.time() - runtime
    print(f"pysat solution time: {runtime} s")
    # Optimal solution (walksat)
    run_time1 = time.time()
    answer = getAnswer(board, optimal)
    run_time1 = time.time() - run_time1
    print(f"Optimal solution time: {run_time1} s")
    if answer != answer_py:
        print("wrong answer")
    # Backtracking
    run_time2 = time.time()
    answer = getAnswer(board, backtrack)
    run_time2 = time.time() - run_time2
    print(f"Backtracking solver time: {run_time2} s")
    if answer != answer_py:
        print("wrong answer")
    # #Brute-force
    # run_time3 = time.time()
    # answer = getAnswer(board, bruteForce)
    # run_time3 = time.time() - run_time3
    # print(f"Brute-force solver time: {run_time3} s")
    # if answer != answer_py:
    #     print("wrong answer")

    fo = open('output.txt', 'w')
    for i in range(len(board)):
        for j in range(len(board[0]) - 1):
            fo.write(answer[i][j] + ", ")
        fo.write(answer[i][j+1] + "\n")
    fo.close()
    
    displayResult(answer)
    
