from cnf import *
import random

def walksat(board, clauses, p=0.5, max_flips=100000):
    # Initialize a random assignment
    assignment = {}
    list_num = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != '_' and board[i][j] != 'T':
                assignment[(i * len(board[0]) + j) + 1] = False
            elif board[i][j] == 'T':
                assignment[(i * len(board[0]) + j) + 1] = True
            else:
                assignment[(i * len(board[0]) + j) + 1] = random.choice([True, False])
                list_num.append(i * len(board[0]) + j)
    assignment = list(assignment.values())
    
    for i in range(max_flips):
        # Select an unsatisfied clause 
        unsatisfied = [c for c in clauses if not satisfies(c, assignment)]
        if not unsatisfied: 
            return assignment
        
        clause = random.choice(unsatisfied)
        
        # With probability p, flip a random variable 
        if random.random() < p:
            var = abs(random.choice(clause)) - 1
        else:
            # Otherwise, flip var that maximizes no. of satisfied clauses
            var = choose_var(clause, clauses, assignment)
        
        assignment[var] = not assignment[var]
        
    return None # Failed to satisfy

def satisfies(clause, assignment):
    for x in clause:
        if assignment[abs(x) - 1] == (x > 0):
            return True

    return False

def choose_var(clause, clauses, assignment):
    # Flip var that minimizes no. of broken clauses
    min_broken = len(clauses)
    var = None
    broken = 0

    for x in clause:
        if x > 0:
            tmp = assignment[:]
            tmp[abs(x) - 1] = False
        else:
            tmp = assignment[:]
            tmp[abs(x) - 1] = True
            
        for c in clauses:
            if not satisfies(c, tmp):
                broken += 1

        if broken < min_broken:
            min_broken = broken
            var = abs(x) - 1
    return var

def optimal(board):
    clauses = []
    clauses = generate_clauses(board)

    assignment = walksat(board, clauses)

    if assignment is None:
        return None
    return assignment
