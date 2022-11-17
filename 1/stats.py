'''
This file should be runnable to print map_statistics using 
$ python stats.py
'''

from collections import namedtuple
from ways import load_map_from_csv


def map_statistics(roads) :
    '''return a dictionary containing the desired information
    You can edit this function as you wish'''
    LinkTypeHistog = {}
    numJun = len(roads.junctions())
    numLinks = 0
    minBF = 0
    maxBF = 0
    sumBF = 0
    minLD = 1
    maxLD = 0
    sumLD = 0
    for link in roads.iterlinks() :
        numLinks += 1
        k = link.distance
        sumLD += k
        if k < minLD :
            minLD = k
        if k > maxLD :
            maxLD = k
        highwayType = link.highway_type
        if highwayType in LinkTypeHistog :
            LinkTypeHistog[highwayType] += 1
        else :
            LinkTypeHistog[highwayType] = 1
    avgLD = sumLD / numLinks
    for junction in roads.junctions() :
        i = len(junction.links)
        sumBF += i
        if i < minBF :
            minBF = i
        if i > maxBF :
            maxBF = i
    avgBF = sumBF / numJun

    Stat = namedtuple('Stat', ['max', 'min', 'avg'])
    return {
        'Number of junctions' : numJun,
        'Number of links' : numLinks,
        'Outgoing branching factor' : Stat(max=maxBF, min=minBF, avg=avgBF),
        'Link distance' : Stat(max=maxLD, min=minLD, avg=avgLD),
        # value should be a dictionary
        # mapping each road_info.TYPE to the no' of links of this type
        'Link type histogram' : LinkTypeHistog,  # tip: use collections.Counter
    }


def print_stats() :
    for k, v in map_statistics(load_map_from_csv()).items() :
        print('{}: {}'.format(k, v))


if __name__ == '__main__' :
    from sys import argv

    assert len(argv) == 1
    print_stats()
