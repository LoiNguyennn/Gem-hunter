def GenerateTruthTable(dnf_clauses):
    num_variables = len(set([abs(literal) for clause in dnf_clauses for literal in clause]))
    truth_table = []
    for i in range(2 ** num_variables):
        truth_table.append([])
        for j in range(num_variables):
            truth_table[-1].append((i >> j) & 1)
    return truth_table

def CheckingTruthTable(truth_table, dnf_clauses):
    #return an array of True/False values
    res = []
    for row in truth_table:
        OR = False
        for clause in dnf_clauses:
            AND = True
            for literal in clause:
                AND &= row[abs(literal) - 1] if literal > 0 else not row[abs(literal) - 1]
            OR |= AND
        res.append(OR)
    return res

def genInput(board):
    answer = [[0 for col in range(len(board[0]))] for row in range(len(board))]
    for row in board:
        print(row)

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 'T':
                for dir in DIRECTION:
                    x = i + dir[0]
                    y = j + dir[1]
                    if x >= 0 and x < len(board) and y >= 0 and y < len(board[0]):
                        answer[x][y] += 1
    
    
    for i in range(len(answer)):
        for j in range(len(answer[0])):
            if answer[i][j] == 0:
                answer[i][j] = '_'
            if board[i][j] != '0':
                answer[i][j] = '_'
    for row in answer:
        for col in row:
            print(col, end=', ')
        print()

def de_morgan(clause):
    return [-literal for literal in clause]

def cnf_generator(truth_table, result):
    cnf = []
    for i in range(len(truth_table)):
        if result[i] == False:
            cnf.append(de_morgan([literal + 1 if truth_table[i][literal] == 1 else -(literal + 1) for literal in range(len(truth_table[i]))]))
    return cnf

dnf_clauses = [[1, 2]]

truth_table = GenerateTruthTable(dnf_clauses)
truth_table_result = CheckingTruthTable(truth_table, dnf_clauses)

cnf_clauses = cnf_generator(truth_table, truth_table_result)

print(cnf_clauses)
for row in truth_table:
    print(row)
print(truth_table_result)