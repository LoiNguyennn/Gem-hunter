from itertools import combinations

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

def de_morgan(clause):
    return [-literal for literal in clause]

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

def simpleDPLL(clauses, symbols, assignment={}):
    if all(check_valid(clause, assignment) for clause in clauses):
        return True, assignment
    if len(symbols) == 0:
        return False, {}
    
    unassigned_symbols = set(symbols)
                    
    literal = unassigned_symbols.pop()
    assignment[abs(literal)] = True
    result, final_assignment = simpleDPLL(clauses, unassigned_symbols, assignment)
    if result:
        return True, final_assignment
    assignment[abs(literal)] = False
    return simpleDPLL(clauses, unassigned_symbols, assignment)

def backtrack(board):
    cnf = []
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
                cnf.append(dnf)

    assignment = {}
    pure_symbols = {}
    impure_symbols = []

    # Find pure symbols
    for dnf in cnf:
        for clause in dnf:
            for lit in clause:
                if abs(lit) not in impure_symbols:
                    if abs(lit) in pure_symbols:
                        if pure_symbols[abs(lit)] != (lit > 0):
                            del pure_symbols[abs(lit)]
                            impure_symbols.append(abs(lit))
                    else:
                        pure_symbols[abs(lit)] = (lit > 0)
    # Remove pure symbols from clauses and unassigned symbols
    for lit, value in pure_symbols.items():
        assignment[lit] = value
        for dnf in cnf:
            for i, clause in enumerate(dnf):
                dnf[i] = [lit for lit in clause if abs(lit) not in pure_symbols]
                
    satisfiable, assignment = simpleDPLL(cnf, impure_symbols, assignment)
    if satisfiable:
        result = [-1] * (len(board) * len(board[0]))
        for var, value in assignment.items():
            result[var - 1] = value
        return result
    else:
        return None
    
