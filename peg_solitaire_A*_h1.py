__author__ = 'Abhinav'
import copy
import time
import psutil
import os

max_state = 0

traversed_path = list()


def main():
    global max_state
    heuristic_function_case = raw_input(
        "Select heuristic: 1 - mahattan distance, 2 - move possibility, 3 - state panelty:")
    heuristic_function = ""

    if heuristic_function_case == "1":
        heuristic_function = "manhattan"
    elif heuristic_function_case == "2":
        heuristic_function = "move_possibility"
    elif heuristic_function_case == "3":
        heuristic_function = "state_penalty"
    else:
        print "Please enter correct heuristic"
        return
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
    result = a_star(input_state, heuristic_function, prune)
    end_time = time.time()
    if (result == "success"):
        print "Solution found"
        print traversed_path
    else:
        print "Solution was not found"
    print "----------------------------------------"
    print "Execution time: %f ms" % ((end_time - start_time) * 1000)

    print "No of expanded state: %d" % max_state
    process = psutil.Process(os.getpid())
    mem = process.get_memory_info()[0] / float(2 ** 20)
    print "Memory: %f MB" % mem


def a_star(input_state, heuristic_function, prune):
    global max_state
    visited_list = [input_state]
    closed_list = list()
    came_from = dict()
    g_score = dict()
    f_score = dict()
    g_score[getKey(input_state)] = 0

    f_score[getKey(input_state)] = g_score[getKey(input_state)] + get_heuristic_cost(input_state, heuristic_function)
    base_pagoda_val = get_pagoda_value(input_state)
    while len(visited_list) != 0:
        current_node = get_best_node(visited_list, f_score)
        if check_goal_state(current_node) == "true":
            reconstruct_path(came_from, current_node)
            max_state = len(closed_list)
            return "success"
        visited_list.remove(current_node)
        closed_list.append(current_node)
        successors = get_successor(current_node)

        for successor in successors:
            if closed_list.count(successor[0]) > 0:
                continue
            elif get_pagoda_value(successor[0]) < 0 and prune == "Yes":
                continue

            tentative_g_score = g_score[getKey(current_node)] + 1
            if visited_list.count(successor[0]) == 0 or tentative_g_score < g_score[getKey(successor[0])]:
                came_from[getKey(successor[0])] = (getKey(current_node), successor[1])
                g_score[getKey(successor[0])] = tentative_g_score
                f_score[getKey(successor[0])] = g_score[getKey(successor[0])] + get_heuristic_cost(successor[0],
                                                                                                   heuristic_function)
                if visited_list.count(successor[0]) == 0:
                    visited_list.append(successor[0])
    max_state = len(closed_list)
    return "failure"


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


def get_heuristic_cost(input_state, heuristic_function):
    state_penalty = [
        ["_", "_", 4, 0, 4, "_", "_"],
        ["_", "_", 0, 0, 0, "_", "_"],
        [4, 0, 3, 0, 3, 0, 4],
        [0, 0, 0, 1, 0, 0, 0],
        [4, 0, 3, 0, 3, 0, 4],
        ["_", "_", 0, 0, 0, "_", "_"],
        ["_", "_", 4, 0, 4, "_", "_"],
    ]

    cost = 0
    for i in range(7):
        for j in range(7):
            if input_state[i][j] == "X":
                if heuristic_function == "manhattan":
                    cost += abs(i - 3) + abs(j - 3)
                elif heuristic_function == "move_possibility":
                    if i - 2 >= 0 and input_state[i - 2][j] == "0" and input_state[i - 1][j] == "X":
                        cost += 1
                    if i + 2 < 7 and input_state[i + 2][j] == "0" and input_state[i + 1][j] == "X":
                        cost += 1
                    if j - 2 >= 0 and input_state[i][j - 2] == "0" and input_state[i][j - 1] == "X":
                        cost += 1
                    if j + 2 < 7 and input_state[i][j + 2] == "0" and input_state[i][j + 1] == "X":
                        cost += 1
                elif heuristic_function == "state_penalty":
                    cost += state_penalty[i][j]
    return cost


def get_best_node(visited_list, f_score):
    best_node = visited_list[0]
    for node in visited_list:
        if f_score[getKey(node)] < f_score[getKey(best_node)]:
            best_node = node
    return best_node


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


def reconstruct_path(came_from, goal):
    global traversed_path
    state_key = getKey(goal)
    path = list()
    while came_from.has_key(state_key):
        path.append(came_from[state_key][1])
        state_key = came_from[state_key][0]

    path.reverse()
    traversed_path = path


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


def getKey(input_state):
    state_key = ""
    for i in range(7):
        state_key = state_key + "".join(input_state[i])
    return state_key


if __name__ == '__main__':
    main()