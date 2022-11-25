# Shira Taitelbaum 322207341
'''
Parse input and run appropriate code.
Don't use this file for the actual work; only minimal code should be here.
We just parse input and call methods from other modules.
'''

from search_algorithms import *
from ways.tools import *

MAX_SPEED = 110


# do NOT import ways. This should be done from other files
# simply import your modules and call the appropriate functions

def huristic_function(lat1, lon1, lat2, lon2) :
    return compute_distance(lat1, lon1, lat2, lon2) / MAX_SPEED


def find_ucs_rout(source, target) :
    return uniform_cost_search(source, target)


def find_astar_route(source, target) :
    return astar_search(source, target, h=huristic_function)


def find_idastar_route(source, target) :
    return idastar_search(source, target, h=huristic_function)


def dispatch(argv) :
    from sys import argv
    source, target = int(argv[2]), int(argv[3])
    path = []
    if argv[1] == 'ucs' :
        path, ucstime = find_ucs_rout(source, target)
    elif argv[1] == 'astar' :
        path, astartime, htime = find_astar_route(source, target)
    elif argv[1] == 'idastar' :
        path = find_idastar_route(source, target)
    print(' '.join(str(j) for j in path))


if __name__ == '__main__' :
    from sys import argv

    #createimg()
    #uniform_cost_search_100_problems()
    #astar_search_100_problems(h=huristic_function)
    dispatch(argv)
    # to create 100 pair of s,t run the func create100SearchProblem() in random_search
