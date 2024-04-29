from cnf import *

def brute_force_sat(cnf):
    # Get all the variables in the CNF
    variables = {abs(x) for clause in cnf for x in clause}

    # Generate all possible assignments
    for assignment in product([False, True], repeat=len(variables)):
        assignment = {var: val for var, val in zip(variables, assignment)}

        # Check if this assignment satisfies the CNF
        if all(any(assignment[abs(x)] == (x > 0) for x in clause) for clause in cnf):
            # If it does, return it
            answer = []
            for key in assignment:
                if assignment[key] == True:
                    answer.append(key)
                else:
                    answer.append(-key)
            return answer
    # If no satisfying assignment was found, return None
    return None

def bruteForce(board):
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
    
    clauses = []
    for cnf in cnfs:
        for clause in cnf:
            clauses.append(clause)

    assignment = brute_force_sat(clauses)

    if assignment is None:
        return None
    return assignment
