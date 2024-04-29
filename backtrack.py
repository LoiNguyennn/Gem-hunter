from cnf import *

def backtracking(cnf, symbols, model):
    if len(cnf) == 0:
        return True, model
    
    if [] in cnf:
        return False, {}
    
    unassigned_symbols = deepcopy(symbols)                
    literal = unassigned_symbols.pop()

    model[abs(literal) - 1] = literal
    new_cnf = getNewClauses(literal, deepcopy(cnf))
    result, final_assignment = backtracking(new_cnf, unassigned_symbols, model)
    if result:
        return True, final_assignment
    
    model[abs(literal) - 1] = -literal
    new_cnf = getNewClauses(-literal, deepcopy(cnf))
    return backtracking(new_cnf, unassigned_symbols, model)

def getNewClauses(literal, clauses):
    new_cnf = []
    for clause in clauses:
        if literal not in clause:
            if -literal in clause:
                clause.remove(-literal)
            new_cnf.append(clause)
    return new_cnf

def backtrack(board):
    clauses = generate_clauses(board)
    #get all the symbol
    symbols = set()
    for clause in clauses:
        for literal in clause:
            symbols.add(abs(literal))
    symbols = list(symbols)
    symbols.reverse()

    model = list(range(-len(board)*len(board[0]), 0))
    model.reverse()

    satisfiable, model = backtracking(clauses, symbols, model)
    if satisfiable:
        return model
    return None

