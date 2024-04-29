from Gem_Hunter import *
import time

if __name__ == '__main__':
    # board = InputBoard("input9x9")
    # i = deepcopy(board)
    # # print(board)
    # runtime = time.time()
    # answer_py = getAnswer(board, PySat)
    # runtime = time.time() - runtime
    # print(f"pysat solution time: {runtime} s")
    # # Optimal solution (walksat)
    # run_time1 = time.time()
    # answer = getAnswer(board, optimal)
    # run_time1 = time.time() - run_time1
    # print(f"Optimal solution time: {run_time1} s")
    # if answer != answer_py:
    #     print("wrong answer")
    # # Backtracking
    # run_time2 = time.time()
    # answer = getAnswer(board, backtrack)
    # run_time2 = time.time() - run_time2
    # print(f"Backtracking solver time: {run_time2} s")
    # if answer != answer_py:
    #     print("wrong answer")
    # #Brute-force
    # run_time3 = time.time()
    # answer = getAnswer(board, bruteForce)
    # run_time3 = time.time() - run_time3
    # print(f"Brute-force solver time: {run_time3} s")
    # if answer != answer_py:
    #     print("wrong answer")

    # fo = open('output.txt', 'w')
    # for i in range(len(board)):
    #     for j in range(len(board[0]) - 1):
    #         fo.write(answer[i][j] + ", ")
    #     fo.write(answer[i][j+1] + "\n")
    # fo.close()
    
    # displayResult(answer)
    game = GemHunter()
