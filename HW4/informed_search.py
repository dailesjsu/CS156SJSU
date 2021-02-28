# ----------------------------------------------------------------------
# Name:     informed_search
# Purpose:  Homework 4 - Implement astar and some heuristics
#
# Author(s):
# ----------------------------------------------------------------------
"""
A* Algorithm and heuristics implementation

Your task for homework 4 is to implement:
1.  astar
2.  single_heuristic
3.  better_heuristic
4.  gen_heuristic
"""
import data_structures


def astar(problem, heuristic):
    """
    A* graph search algorithm
    returns a solution for the given search problem
    :param
    problem (a Problem object) representing the quest
            see Problem class definition in spartanquest.py
    heuristic (a function) the heuristic function to be used
    :return: list of actions representing the solution to the quest
                or None if there is no solution
    """
    closed = set()
    fringe = data_structures.PriorityQueue()
    state = problem.start_state()
    root = data_structures.Node(state)
    fringe.push(root, heuristic(state, problem))

    while True:
        if fringe.is_empty():
            return None
        node = fringe.pop()
        if problem.is_goal(node.state):
            return node.solution()
        if node.state not in closed:
            closed.add(node.state)
            for child_state, action, action_cost in problem.successors(node.state):
                # Tie Breaking
                h = heuristic(child_state, problem)

                h *= (1.0 + (1/100))
                # if child_state not in closed:
                child_node = data_structures.Node(child_state, node, action, action_cost + node.cumulative_cost)
                f = child_node.cumulative_cost + h
                fringe.push(child_node, f)


def null_heuristic(state, problem):
    """
    Trivial heuristic to be used with A*.
    Running A* with this null heuristic, gives us uniform cost search
    :param
    state: A state is represented by a tuple containing:
                the current position of Sammy the Spartan
                a tuple containing the positions of the remaining medals
    problem: (a Problem object) representing the quest
    :return: 0
    """
    return 0


def single_heuristic(state, problem):
    """
    Fill in the docstring here
    :param
    state: A state is represented by a tuple containing:
                the current position of Sammy the Spartan
                a tuple containing the positions of the remaining medals
    problem: (a Problem object) representing the quest

    :return:
    """
    if state[1]:
        return min_distance(state[0], state[1])
    return 0


def better_heuristic(state, problem):
    """
    Fill in the docstring here
    :param
    state: A state is represented by a tuple containing:
                the current position of Sammy the Spartan
                a tuple containing the positions of the remaining medals
    problem: (a Problem object) representing the quest
    :return:
    """
    # Enter your code here and remove the pass statement below
    if state[1]:
        start = problem.start_state()[0]
        goal = state[1][0]
        position = state[0]
        D = 1
        D2 = 1

        # Check where the state is in relation to the start state
        if position[1] > goal[1]: # Moved East
            D = 1
        if position[1] < goal[1]: # Moved West
            D = 6
        if position[0] > goal[0]: # Moved South
            D2 = 2
        if position[0] < goal[0]: # Moved North
            D2 = 1
        return (D2 * abs(position[0] - goal[0])) + (D * abs(position[1] - goal[1]))
    return 0




def gen_heuristic(state, problem):
    """
    Fill in the docstring here
    :param
    state: A state is represented by a tuple containing:
                the current position of Sammy the Spartan
                a tuple containing the positions of the remaining medals
    problem: (a Problem object) representing the quest
    :return:
    """
    if state[1]:
        goals = state[1]
        start = problem.start_state()[0]
        heru = []
        sum  = 0
        position = state[0]

        for goal in goals:
            D = 1
            D2 = 1
            # Check where the state is in relation to the start state
            if position[1] > goal[1]:  # Moved East
                D = 1
            if position[1] < goal[1]:  # Moved West
                D = 6
            if position[0] > goal[0]:  # Moved South
                D2 = 2
            if position[0] < goal[0]:  # Moved North
                D2 = 1

            sum += (D2 * abs(position[0] - goal[0])) + (D * abs(position[1] - goal[1]))
            #heru.sort()

        return sum / len(goals)
    return 0
