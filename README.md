# 15-Puzzle-Problem

Goal Node: [['1', '2', '3', '4'], ['5', '6', '7', '8'], ['9', '10', '11', '12'], ['13', '14', '15', '0']]
Initial Node: An arrangement of the numbers with one empty block entered by the user
State Space: All possible arrangements of the numbers and with one empty block
Edge Weight: 1

Heuristics tried: Manhattan distance, Number of misplaced numbers (Both are admissible because they donot 
over estimate the cost to reach the final state). Manhattan distance works the best.

Just for comparison, we also tried Permutation inversion and Manhattan*4 (both not admissible) as a hueristic. The 
result was obtained faster but as expected, it was not optimal.

A priority queue has been implemented with heapq to pop states with the maximum priority. The succesor function returns 
a set of states accounting for all possible moves that can be made in the parent state. The manhattan is computed
considering the additional allowed moves also.

The code assumes that the initial state entered is solvable.

Priority queues work faster than a list-dictionay system earlier implemented.
