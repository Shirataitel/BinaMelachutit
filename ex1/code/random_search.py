# Shira Taitelbaum 322207341
import math

from ways import load_map_from_csv
import csv
import random


def create100SearchProblem() :
    roads = load_map_from_csv()
    numJun = len(roads.junctions())
    file = open('problems.csv', 'w', newline='')
    writer = csv.writer(file)
    for i in range(0, 100) :
        startInt = random.randrange(numJun)
        startJun = roads[startInt]
        currentJun = startJun
        for j in range(0, 7) :
            if len(currentJun.links) != 0 :
                tInt = currentJun.links[len(currentJun.links) - 1].target
                tJun = roads[tInt]
                currentJun = tJun
            else :
                break
        line = [startInt, tInt]
        writer.writerow(line)
    file.close()


if __name__ == '__main__' :
    from sys import argv

    assert len(argv) == 1
    create100SearchProblem()
