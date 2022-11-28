# Shira Taitelbaum 322207341
import csv
import math

from node_queue import *
from ways.draw import *
from ways.tools import *
from ways import load_map_from_csv
from ways.info import SPEED_RANGES

roads = load_map_from_csv()
MAX_SPEED = 110


# I used some code from the class' github and from the tirgul
def gUCS(node) :
    parent = node.parent
    if parent == None :
        return 0
    links = roads[parent.junction_inx].links
    link = childlink(links, node.junction_inx)
    v = link.distance / 1000
    s = SPEED_RANGES[link.highway_type][1]
    return v / s


def gIDASTAR(link) :
    v = link.distance / 1000
    s = SPEED_RANGES[link.highway_type][1]
    return v / s


def huristic_function(lat1, lon1, lat2, lon2) :
    return compute_distance(lat1, lon1, lat2, lon2) / MAX_SPEED


def childlink(links, child) :
    for l in links :
        if l.target == child :
            return l


def best_first_graph_search_usc(source, target, f) :
    node = Node(source)
    frontier = PriorityQueue(f)  # Priority Queue
    frontier.append(node)
    closed_list = set()
    while frontier :
        node = frontier.pop()
        if node.junction_inx == target :
            return node.path(), node.path_cost
        closed_list.add(node.junction_inx)
        for child in node.expand(roads[node.junction_inx], f) :
            if child.junction_inx not in closed_list and child not in frontier :
                frontier.append(child)
            elif child in frontier and f(child) < frontier[child] :
                del frontier[child]
                frontier.append(child)
    return None


# f = gUCS:
def uniform_cost_search(source, target) :
    return best_first_graph_search_usc(source, target, f=gUCS)


def uniform_cost_search_100_problems() :
    file = open('results/UCSRuns.txt', 'w', newline='')
    fileproblem = open('problems.csv', 'r')
    lines = fileproblem.readlines()
    fileproblem.close()
    for line in lines :
        x = line.split(",")
        path, ucstime = uniform_cost_search(int(x[0]), int(x[1].replace("\n", "")))
        newline = ' '.join(str(j) for j in path) + " - " + str(round(ucstime, 4)) + "\n"
        file.write(newline)
    file.close()


def best_first_graph_search_astar(source, target, f, g) :
    node = Node(source)
    frontier = PriorityQueue(f)  # Priority Queue
    frontier.append(node)
    closed_list = set()
    while frontier :
        node = frontier.pop()
        if node.junction_inx == target :
            return node.path(), node.real_path_cost
        closed_list.add(node.junction_inx)
        for child in node.expandastar(roads[node.junction_inx], f, g) :
            if child.junction_inx not in closed_list and child not in frontier :
                frontier.append(child)
            elif child in frontier and f(child) < frontier[child] :
                del frontier[child]
                frontier.append(child)
    return None


def astar_search(source, target, h) :
    def gASTAR(node) :
        g = gUCS(node)
        lat1 = roads[source].lat
        lat2 = roads[target].lat
        lon1 = roads[source].lon
        lon2 = roads[target].lon
        return h(lat1, lon1, lat2, lon2) + g

    return best_first_graph_search_astar(source, target, f=gASTAR, g=gUCS)


def astar_search_100_problems(h) :
    file = open('results/AStarRuns.txt', 'w', newline='')
    #filec = open('results/AStarRuns.csv', 'w', newline='')
    #writer = csv.writer(filec)
    fileproblem = open('problems.csv', 'r')
    lines = fileproblem.readlines()
    fileproblem.close()
    # i = 0
    for line in lines :
        x = line.split(",")
        source = int(x[0])
        target = int(x[1].replace("\n", ""))
        path, astartime = astar_search(source, target, h)
        lat1 = roads[source].lat
        lat2 = roads[target].lat
        lon1 = roads[source].lon
        lon2 = roads[target].lon
        htime = h(lat1, lon1, lat2, lon2)
        newline = ' '.join(str(j) for j in path) + " - " + str(round(astartime, 4)) + " - " + str(
            round(htime, 4)) + "\n"
        #row = [str(round(astartime, 4)), str(round(htime, 4))]
        #writer.writerow(row)
        file.write(newline)
        #print(i)
        #i += 1
    file.close()
    #filec.close()


new_limit = -1


def idastar_search(source, target, h) :
    global new_limit
    lat1 = roads[source].lat
    lat2 = roads[target].lat
    lon1 = roads[source].lon
    lon2 = roads[target].lon
    new_limit = h(lat1, lon1, lat2, lon2)
    while True :
        f_limit = new_limit
        new_limit = math.inf
        sol = dfs_f(source, target, h, 0, [], f_limit)
        if sol is not None :
            return sol


def dfs_f(source, target, h, g, path, f_limit) :
    global new_limit
    lat1 = roads[source].lat
    lat2 = roads[target].lat
    lon1 = roads[source].lon
    lon2 = roads[target].lon
    new_f = g + h(lat1, lon1, lat2, lon2)
    if new_f > f_limit :
        new_limit = min(new_f, new_limit)
        return None
    if source == target :
        return path
    for link in roads[source].links :
        if path == [] :
            path.append(source)
        path.append(link.target)
        sol = dfs_f(link.target, target, h, g + gIDASTAR(link), path, f_limit)
        if sol is not None :
            return sol
    return None


def createimg() :
    fileproblem = open('problems.csv', 'r')
    content = fileproblem.readlines()
    fileproblem.close()
    for row in range(10) :
        x = content[row].split(",")
        # print(row)
        path = idastar_search(int(x[0]), int(x[1].replace("\n", "")), huristic_function)
        plot_path(roads, path)
        name = 'sulotions_img/' + 'img' + str(row + 1) + '.png'
        plt.savefig(name)
        plt.close()
        plt.clf()
