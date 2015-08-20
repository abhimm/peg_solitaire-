__author__ = 'Abhinav'

import copy
import time
import psutil
import os

max_state = 0
prune = ""


def main():
    input_state = list()
    # i = 1
    #    while (i <= 7):
    #       row_str = raw_input('Enter row:%d of intial state: ' % i)
    #       row_list = row_str.split(" ")
    #       input_state.append(row_list)
    #       i += 1
    global prune
    prune = raw_input("Do you want to prune, enter: Yes / No: ")
    input_state = [
        ["_", "_", "0", "0", "0", "_", "_"],
        ["_", "_", "0", "X", "0", "_", "_"],
        ["0", "0", "X", "X", "X", "0", "0"],
        ["0", "0", "0", "0", "X", "X", "0"],
        ["0", "0", "0", "X", "0", "X", "0"],
        ["_", "_", "X", "0", "0", "_", "_"],
        ["_", "_", "X", "0", "0", "_", "_"],
    ]
    start_time = time.time()
    ids(input_state)
    end_time = time.time()

    print "----------------------------------------"

    print "No of expanded state: %d" % max_state
    print "Execution time: %f ms" % ((end_time - start_time) * 1000)
    process = psutil.Process(os.getpid())
    mem = process.get_memory_info()[0] / float(2 ** 20)
    print "Memory: %f MB" % mem



def ids(input_state):
    global max_state
    depth = 0
    result = ""
    for depth in range(10000000):
        max_state = 0
        result = dls(input_state, depth)
        if result != "cutoff" and result != "":
            break
        depth += 1
    if result == "" or result == "cutoff":
        print "Solution could not be found after %d iteration" % depth
    elif result == "false":
        print "No solution exists"



def dls(input_state, depth):
    result = ""
    path = list()
    result = dls_util(input_state, 0, depth, path)
    return result


def dls_util(input_state, depth, limit, path):
    global max_state
    global prune
    cut_off_occurred = False
    if check_goal_state(input_state) == "true":
        print "Solution found"
        for step in path:
            print step
        return "true"
    elif depth == limit:
        return "cutoff"
    else:
        if get_pagoda_value(input_state) < 0 and prune == "Yes":
            return "false"
        successor_state = get_successor(input_state)
        max_state += 1
        if len(successor_state) == 0:
            return "false"

        for state in successor_state:
            local_path = copy.deepcopy(path)
            local_path.append(state[1])
            result = dls_util(state[0], depth + 1, limit, local_path)
            if result == "cutoff":
                cut_off_occurred = True
            elif result == "true":
                return result

    if cut_off_occurred:
        return "cutoff"
    else:
        return "false"


def get_pagoda_value(input_state):
    pagoda_function = [
        ["_", "_", 0, 1, 0, "_", "_"],
        ["_", "_", 0, 0, 0, "_", "_"],
        [-1, 1, 0, 1, 0, 1, -1],
        [0, 0, 0, 0, 0, 0, 0],
        [-1, 1, 0, 1, 0, 1, -1],
        ["_", "_", 0, 0, 0, "_", "_"],
        ["_", "_", 0, 1, 0, "_", "_"],
    ]

    pagoda_val = 0
    for i in range(7):
        for j in range(7):
            if input_state[i][j] == "X":
                pagoda_val += pagoda_function[i][j]

    return pagoda_val


def check_goal_state(input_state):
    i = 1
    for row in input_state:
        if i == 4:
            if cmp(row, ["0", "0", "0", "X", "0", "0", "0"]) != 0:
                return "false"
        elif i == 3 or i == 5:
            if cmp(row, ["0", "0", "0", "0", "0", "0", "0"]) != 0:
                return "false"
        else:
            if cmp(row, ["_", "_", "0", "0", "0", "_", "_"]) != 0:
                return "false"
        i += 1

    return "true"


def get_index(i, j):
    structure = [
        [0, 0, 0, 1, 2, 0, 0],
        [0, 0, 3, 4, 5, 0, 0],
        [6, 7, 8, 9, 10, 11, 12],
        [13, 14, 15, 16, 17, 18, 19],
        [20, 21, 22, 23, 24, 25, 26],
        [0, 0, 27, 28, 29, 0, 0],
        [0, 0, 30, 31, 32, 0, 0]
    ]
    return structure[i][j]


def get_successor(input_state):
    successor_state = list()

    for i in range(7):
        for j in range(7):
            if ((i < 2 and i >= 0 ) or ( i < 7 and i >= 5)) and (( j < 2 and j >= 0 ) or ( j < 7 and j >= 5)):
                continue
            if input_state[i][j] == "X":
                # move up
                if i - 2 >= 0 and input_state[i - 2][j] == "0" and input_state[i - 1][j] == "X":
                    copy_state = copy.deepcopy(input_state)
                    copy_state[i - 2][j] = "X"
                    copy_state[i][j] = "0"
                    copy_state[i - 1][j] = "0"
                    tup = (copy_state, (get_index(i, j), get_index(i - 2, j)))
                    successor_state.append(tup)
                    # move down
                if i + 2 < 7 and input_state[i + 2][j] == "0" and input_state[i + 1][j] == "X":
                    copy_state = copy.deepcopy(input_state)
                    copy_state[i + 2][j] = "X"
                    copy_state[i][j] = "0"
                    copy_state[i + 1][j] = "0"
                    tup = (copy_state, (get_index(i, j), get_index(i + 2, j)))
                    successor_state.append(tup)
                    # move left
                if j - 2 >= 0 and input_state[i][j - 2] == "0" and input_state[i][j - 1] == "X":
                    copy_state = copy.deepcopy(input_state)
                    copy_state[i][j - 2] = "X"
                    copy_state[i][j] = "0"
                    copy_state[i][j - 1] = "0"
                    tup = (copy_state, (get_index(i, j), get_index(i, j - 2)))
                    successor_state.append(tup)
                    # move right
                if j + 2 < 7 and input_state[i][j + 2] == "0" and input_state[i][j + 1] == "X":
                    copy_state = copy.deepcopy(input_state)
                    copy_state[i][j + 2] = "X"
                    copy_state[i][j] = "0"
                    copy_state[i][j + 1] = "0"
                    tup = (copy_state, (get_index(i, j), get_index(i, j + 2)))
                    successor_state.append(tup)
    return successor_state


if __name__ == '__main__':
    main()



