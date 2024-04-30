from pysat.solvers import Glucose3
from menu import GameMenu
from cnf import *
from optimal import optimal
from backtrack import backtrack
from bruteforce import bruteForce
import time
import pygame

method ={'Optimal': optimal, "Backtracking":backtrack, "Brute-force":bruteForce}

class GemHunter:
    def __init__ (self):
        self.menu = GameMenu()
        if self.menu.exit or self.menu.file_name is None or self.menu.method is None:
            pass
        else:
            self.run_game()
    def run_game(self):
        self.puzzle = InputBoard(self.menu.file_name)
        self.right_answer = getAnswer(self.puzzle, PySat)
        s_time = time.time()
        self.method_answer = getAnswer(self.puzzle, method.get(self.menu.method, None))
        s_time = time.time()- s_time

        #output to file
        fo = open('output.txt', 'w')
        for i in range(len(self.method_answer)):
            for j in range(len(self.method_answer[0]) - 1):
                fo.write(self.method_answer[i][j] + ", ")
            fo.write(self.method_answer[i][j+1] + "\n")
        fo.close()
        
        displayResult(self.method_answer, (self.method_answer == self.right_answer), s_time)

        return GemHunter()


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

###GET RESULT###
def getAnswer(board, function):
    puzzle = deepcopy(board)
    answer = convertResult(function(puzzle), puzzle)
    return answer

def convertResult(assignment, board):
    if assignment is None:
        return None
    result = [['G' for _ in range(len(board[0]))] for _ in range(len(board))]
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != '_':
                result[i][j] = board[i][j]
            else:
                if assignment[i * len(board[0]) + j] > 0:
                    result[i][j] = 'T'
    return result

def displayResult(board, is_correct = True, time = 0):
    pygame.init()
    pygame.font.init()
    col = len(board[0])
    row = len(board)
    tile_size = min(70, 750//col)
    font = pygame.font.SysFont('Arial', 22)
    win = pygame.display.set_mode((col * tile_size, row * tile_size + 30))
    pygame.display.set_caption('Gem Hunter')
    clock = pygame.time.Clock()

    def draw_map():
        for i in range(row):
            for j in range(col):
                if board[i][j] == 'T':
                   color = TRAP_COLOR
                elif board[i][j] == 'G':
                    color = GOLD_COLOR
                else:
                    color = BLANK_COLOR
                pygame.draw.rect(win, color, (j * tile_size, i * tile_size, tile_size - 2, tile_size - 2))
                letter = str(board[i][j])
                text_surface = font.render(letter, True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(j * tile_size + tile_size // 2, i * tile_size + tile_size // 2))
                win.blit(text_surface, text_rect)
        text = f"Alike to pysat: {is_correct}, time: {time:.3f}s"
        text_surface = font.render(text, True, (169, 205, 227))
        shadow_surface = font.render(text, True, (0, 0, 0))
        x, y = (10, row * tile_size+3)
        shadow_position = (x + 2, y + 2)
        win.blit(shadow_surface, shadow_position)
        win.blit(text_surface, (10, row * tile_size+3))
        
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        draw_map()
        pygame.display.flip()
        clock.tick(30)       


