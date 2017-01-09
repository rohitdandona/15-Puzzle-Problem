import os
import sys
import copy
import time
import heapq
import sys


class MyPriorityQueue:
    def __init__(self):
        # private variables
        self.queue = []
        self.index = 0

    def push(self, item, priority):
        heapq.heappush(self.queue, (priority, self.index, item))
        self.index += 1

    def pop(self):
        return heapq.heappop(self.queue)[-1]

    def is_empty(self):
        return len(self.queue) == 0

    def remove_item(self, item):
        for tup in self.queue:
            if item in tup:
                self.queue.remove(tup)
        heapq.heapify(self.queue)

def generate_state(parent_state, empty_block_row, empty_block_column, state_index, type):

    if (type is "row"):
        successor = copy.deepcopy(parent_state)
        successor[empty_block_row][empty_block_column] = parent_state[state_index][empty_block_column]
        successor[state_index][empty_block_column] = parent_state[empty_block_row][empty_block_column]
    else:
        successor = copy.deepcopy(parent_state)
        successor[empty_block_row][empty_block_column] = parent_state[empty_block_row][state_index]
        successor[empty_block_row][state_index] = parent_state[empty_block_row][empty_block_column]

    return successor

def get_move(last_state, current_state):
    last_state_block_row = 0
    last_state_block_column = 0
    current_state_block_row = 0
    current_state_block_column = 0
    for row in last_state:
        if '0' in row:
            last_state_block_row = last_state.index(row)
            last_state_block_column = row.index('0')

    for row in current_state:
        if '0' in row:
            current_state_block_row = current_state.index(row)
            current_state_block_column = row.index('0')

    if ((last_state_block_column - 1) >= 0) and ((last_state_block_column - 1) == current_state_block_column):
        return ("L")
    if ((last_state_block_column + 1) <= 3) and ((last_state_block_column + 1) == current_state_block_column):
        return ("R")
    if ((last_state_block_row - 1) >= 0) and ((last_state_block_row - 1) == current_state_block_row):
        return ("U")
    if ((last_state_block_row + 1) <= 3) and ((last_state_block_row + 1) == current_state_block_row):
        return ("D")

    if ((last_state_block_column - 3) >= 0) and ((last_state_block_column - 3) == current_state_block_column):
        return ("L")
    if ((last_state_block_column + 3) <= 3) and ((last_state_block_column + 3) == current_state_block_column):
        return ("R")
    if ((last_state_block_row - 3) >= 0) and ((last_state_block_row - 3) == current_state_block_row):
        return ("U")
    if ((last_state_block_row + 3) <= 3) and ((last_state_block_row + 3) == current_state_block_row):
        return ("D")

def get_path(initial_state, child, parent_child_dict):
    state_path = []
    state_move = []
    depth = 0

    while child != initial_state:
        child_tuple = tuple(tuple(y) for y in child)
        depth +=1
        state_path.append(child)
        parent_state = [list(x) for x in parent_child_dict[child_tuple]]
        state_move.append(get_move(parent_state,child))
        child = copy.deepcopy(parent_state)

    state_path.append(initial_state)
    print "Total Depth: ", depth
    print "\t"
    print "Path States:"
    while len(state_path)>0:
        print state_path.pop()
    print "\t"
    print "Moves: "
    while len(state_move) > 0:
        print state_move.pop(),


def create_successor_states(parent_state):
    empty_block_row = 0
    empty_block_column = 0
    for row in parent_state:
        if '0' in row:
            empty_block_row = parent_state.index(row)
            empty_block_column = row.index('0')

    successor_states = []
    if empty_block_row == 0:
        successor_states.append(generate_state(parent_state, empty_block_row, empty_block_column, 3, "row"))

    if empty_block_row == 3:
        successor_states.append(generate_state(parent_state, empty_block_row, empty_block_column, 0, "row"))

    if empty_block_column == 0:
        successor_states.append(generate_state(parent_state, empty_block_row, empty_block_column, 3, "col"))

    if empty_block_column == 3:
        successor_states.append(generate_state(parent_state, empty_block_row, empty_block_column, 0, "col"))

    if (empty_block_row - 1) >= 0:
        successor_states.append(generate_state(parent_state, empty_block_row, empty_block_column, empty_block_row - 1, "row"))

    if (empty_block_column - 1) >= 0:
        successor_states.append(generate_state(parent_state, empty_block_row, empty_block_column, empty_block_column - 1, "col"))

    if (empty_block_row + 1) <= 3:
        successor_states.append(generate_state(parent_state, empty_block_row, empty_block_column, empty_block_row + 1, "row"))

    if (empty_block_column + 1) <= 3:
        successor_states.append(generate_state(parent_state, empty_block_row, empty_block_column, empty_block_column + 1, "col"))

    return successor_states


def calculate_manhattan_distance(state):

    goal_state = {'1':[0,0],'2':[0,1],'3':[0,2],'4':[0,3],'5':[1,0],'6':[1,1],'7':[1,2],'8':[1,3],'9':[2,0],'10':[2,1],'11':[2,2],'12':[2,3],'13':[3,0],'14':[3,1],'15':[3,2],'0':[3,3]}
    distance = 0
    for row in state:
        for value in row:
            if value != '0':

                d1 = abs(goal_state[value][0] - state.index(row)) + abs(goal_state[value][1] - row.index(value))

                if (state.index(row) == 0 and row.index(value) == 0) or (state.index(row) == 3 and row.index(value) == 0):
                    d = abs(goal_state[value][0] - state.index(row)) + abs(goal_state[value][1] - (row.index(value)+3))
                    d2 = 2 if d == 3 else (1 + d)
                    if d2 < d1:
                        distance = distance + d2
                        continue

                    if state.index(row) == 0:
                        d = abs(goal_state[value][0] - (state.index(row)+3)) + abs(goal_state[value][1] - row.index(value))
                        d2 = 2 if d == 3 else (1 + d)
                        if d2 < d1:
                            distance = distance + d2
                            continue
                    else:
                        d = abs(goal_state[value][0] - (state.index(row)-3)) + abs(goal_state[value][1] - row.index(value))
                        d2 = 2 if d == 3 else (1 + d)
                        if d2 < d1:
                            distance = distance + d2
                            continue

                    distance = distance + d1
                    continue

                if (state.index(row) == 3 and row.index(value) == 3) or (state.index(row) == 0 and row.index(value) == 3):
                    d = abs(goal_state[value][0] - state.index(row)) + abs(goal_state[value][1] - (row.index(value) - 3))
                    d2 = 2 if d == 3 else (1 + d)
                    if d2 < d1:
                        distance = distance + d2
                        continue

                    if state.index(row) == 0:
                        d = abs(goal_state[value][0] - (state.index(row)+3)) + abs(goal_state[value][1] - row.index(value))
                        d2 = 2 if d == 3 else (1 + d)
                        if d2 < d1:
                            distance = distance + d2
                            continue
                    else:
                        d = abs(goal_state[value][0] - (state.index(row)-3)) + abs(goal_state[value][1] - row.index(value))
                        d2 = 2 if d == 3 else (1 + d)
                        if d2 < d1:
                            distance = distance + d2
                            continue

                    distance = distance + d1
                    continue

                if state.index(row) == 0:
                    d2 = 1 + abs(goal_state[value][0] - (state.index(row)+3)) + abs(goal_state[value][1] - row.index(value))
                    if d2 < d1:
                        distance = distance + d2
                        continue
                if state.index(row) == 3:
                    d2 = 1 + abs(goal_state[value][0] - (state.index(row)+3)) + abs(goal_state[value][1] - row.index(value))
                    if d2 < d1:
                        distance = distance + d2
                        continue
                if row.index(value) == 0:
                    d2 = 1 + abs(goal_state[value][0] - state.index(row)) + abs(goal_state[value][1] - (row.index(value) + 3))
                    if d2 < d1:
                        distance = distance + d2
                        continue
                if row.index(value) == 3:
                    d2 = 1 + abs(goal_state[value][0] - state.index(row)) + abs(goal_state[value][1] - (row.index(value) - 3))
                    if d2 < d1:
                        distance = distance + d2
                        continue

                distance = distance + d1
    return distance

def get_total_numbers_misplaced(states):
    goal_state = {'1': [0, 0], '2': [0, 1], '3': [0, 2], '4': [0, 3], '5': [1, 0], '6': [1, 1], '7': [1, 2],
                  '8': [1, 3], '9': [2, 0], '10': [2, 1], '11': [2, 2], '12': [2, 3], '13': [3, 0], '14': [3, 1],
                  '15': [3, 2], '0': [3, 3]}
    count = 0
    for row in states:
        for value in row:
            if (states.index(row) != goal_state[value][0]) or (row.index(value) != goal_state[value][1]):
                count = count + 1

    return count

def get_no_of_permutation_inversions(initial_state):

    count = 0
    flat_list = [item for sublist in initial_state for item in sublist]
    flat_list.remove('0')
    for number in flat_list:
        for index in range(flat_list.index(number), (len(flat_list))):
            if int(flat_list[index]) < int(number):
                count += 1
    return count

def solve(initial_state):
    # Declarations
    goal_state = [['1', '2', '3', '4'], ['5', '6', '7', '8'], ['9', '10', '11', '12'], ['13', '14', '15', '0']]
    g_s = 0
    cost_dict = {}
    parent_child_dict = {}
    open_states= {}
    closed_states = []
    initial_state_tuple = tuple(tuple(x) for x in initial_state)

    # Start from the initial states and populate collections
    open_states_queue = MyPriorityQueue()
    f_s = g_s + calculate_manhattan_distance(initial_state)
    open_states_queue.push(initial_state, f_s)
    open_states[initial_state_tuple]=f_s

    # Initial state confs
    cost_dict[initial_state_tuple] = g_s

    while not open_states_queue.is_empty():

        # Get the element with the highest priority and check if it is the goal state
        parent_state = open_states_queue.pop()
        if parent_state == goal_state:
            print "Goal state reached !!\t"
            print("Time taken: %s seconds" % (time.time() - start_time))
            print "\t"
            print "Displaying path states, depth and moves..."
            print "\t"
            get_path(initial_state, parent_state, parent_child_dict)
            return (True)

        parent_tuple = tuple(tuple(x) for x in parent_state)
        del open_states[parent_tuple]

        # Add popped state to the closed states
        closed_states.append(parent_state)

        # Create successors from the parent state
        successor = create_successor_states(parent_state)

        # Process successor states
        for child in successor:
            if child not in closed_states:

                # Calculate priority of the child
                child_tuple = tuple(tuple(y) for y in child)
                parent_child_dict[child_tuple] = parent_tuple

                cost = cost_dict[parent_tuple]+1
                f_s = cost + calculate_manhattan_distance(child)

                # Add to open states:
                if child_tuple in open_states:
                    if open_states[child_tuple] > f_s:
                        open_states[child_tuple] = f_s
                        open_states_queue.remove_item(child)
                        open_states_queue.push(child, f_s)
                else:
                    open_states_queue.push(child, f_s)
                    open_states[child_tuple] = f_s

                # Update cost dictionary
                cost_dict[child_tuple] = cost

    return False

filename = sys.argv[1]
with open(filename) as f:
    initial_state = []
    for line in f.read().splitlines():
        initial_state.append(line.split(" "))

print "Getting path to goal state..."
print"\t"
start_time = time.time()
solution = solve(initial_state)

if not solution:
    print "Sorry, no solution found. :("
