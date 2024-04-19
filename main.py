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

def GenerateCNFs(board):
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

if __name__ == '__main__':
    board = InputBoard()
    clauses = GenerateCNFs(board)
    solver = Solver(name='g4')
    for clause in clauses:
        solver.add_clause(clause)
    solver.solve()
    print(solver.get_model())