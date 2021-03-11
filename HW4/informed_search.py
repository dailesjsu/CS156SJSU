# ----------------------------------------------------------------------
# Name:     informed_search
# Purpose:  Homework 4 - Implement astar and some heuristics
#
# Author(s): Dai Le, Ngan Luu
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
    # Enter your code here and remove the pass statement below
    closed = set()  # keep track of our explored states
    fringe = data_structures.PriorityQueue()
    state = problem.start_state()
    root = data_structures.Node(state, None, None)
    fringe.push(root, root.cumulative_cost + heuristic(state, problem))
    while not fringe.is_empty():
        node = fringe.pop()
        if problem.is_goal(node.state):
            return node.solution()  # we found a solution
        if node.state not in closed:  # we are implementing graph search
            closed.add(node.state)
            for child_state, action, action_cost in problem.expand(node.state):
                child_node = data_structures.Node(child_state, node, action)
                child_node.cumulative_cost = node.cumulative_cost + action_cost
                fringe.push(child_node, child_node.cumulative_cost + heuristic(child_state, problem))
    return None  # Failure -  no solution was found


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

def manhattan_distance(sammy, medal):
    """
    Find the Manhattan distance between sammy and medal.
    :param sammy: (tuple) representing the position of Sammy in the grid
    :param medal: (tuple) representing the position of medal in the grid
    :return: (integer) the manhattan distance between sammy and medal
    """
    return abs(sammy[0]-medal[0]) + abs(sammy[1]-medal[1])

def single_heuristic(state, problem):
    """
    Simple Admissible heuristic, based on the Manhattan distance
    Running A* with this single heuristic, gives us optimal solution a little faster than UCS
    This heuristic is admissible because the manhattan distance is calculated without include
    any cost (East, West, North, South).
    Therefore, it will be smaller than actual cost.
    :param
    state: A state is represented by a tuple containing:
                the current position of Sammy the Spartan
                a tuple containing the positions of the remaining medals
    problem: (a Problem object) representing the quest

    :return:
    """
    # Enter your code here and remove the pass statement below
    sammy, medal = state
    if len(medal):
        return manhattan_distance(sammy, medal[0])
    else:
        return 0

def manhattan_distance_cost(sammy, medal, problem):
    """
    Compute the number of carrot that Sammy eats to get to the medal
    :param sammy: (tuple) representing the position of Sammy in the grid
    :param medal: (tuple) representing the position of medal in the grid
    :param problem: (a Problem object) representing the quest
    :return: (integer) number of carrot Sammy eats to get to the medal
    """
    if sammy[0] >= medal[0]:
        if sammy[1] >= medal[1]:
            return ((sammy[0] - medal[0]) * problem.cost['W']) + ((sammy[1] - medal[1]) * problem.cost['N'])
        else:
            return ((sammy[0] - medal[0]) * problem.cost['W']) + ((medal[1] - sammy[1]) * problem.cost['N'])
    else:
        if sammy[1] >= medal[1]:
            return ((medal[0] - sammy[0]) * problem.cost['E']) + ((sammy[1] - medal[1]) * problem.cost['N'])
        else:
            return ((medal[0] - sammy[0]) * problem.cost['E']) + ((medal[1] - sammy[1]) * problem.cost['N'])

def better_heuristic(state, problem):
    """
    Better than single heuristic, based on the Manhattan distance and cost
    Running A* with this better heuristic, gives us optimal solution faster than single heuristic
    This heuristic is admissible and consistent because it use manhattan distance with cost of moves
    Thus, its calculation is closer to actual cost than single_heuristic, but it is still smaller than
    actual cost.
    :param
    state: A state is represented by a tuple containing:
                the current position of Sammy the Spartan
                a tuple containing the positions of the remaining medals
    problem: (a Problem object) representing the quest
    :return:
    """
    # Enter your code here and remove the pass statement below
    sammy, medal = state
    if len(medal):
        return manhattan_distance_cost(sammy, medal[0], problem)
    else:
        return 0

def gen_heuristic(state, problem):
    """
    Consistent and admissible heuristic, used for general problems with multiple medals.
    Running A* with this gen heuristic, gives us optimal solution faster than better heuristic
    This heuristic is admissible and consistent because the result is from the position of the medal
    that Sammy consumes the most carrot to reach.
    Thus, we can get the heuristic is at most close to the actual cost
    Also, because of max function, we get closer to the true cost, we will expand fewer nodes.
    :param
    state: A state is represented by a tuple containing:
                the current position of Sammy the Spartan
                a tuple containing the positions of the remaining medals
    problem: (a Problem object) representing the quest
    :return:
    """
    # Enter your code here and remove the pass statement below
    sammy, medal = state
    if medal:
        return max(manhattan_distance_cost(sammy, medl, problem) for medl in medal)
    else:
        return 0