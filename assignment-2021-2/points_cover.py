import itertools
from pprint import pprint
import sys

def CreateMilkyWay(TextName):
    U = []
    with open(TextName) as f:
        lines = f.read().splitlines()
        for numbers in lines:
            U.append(numbers.split(" "))
    for i in range(0,len(U)):
        U[i][0]=int(U[i][0])
        U[i][1]=int(U[i][1])
    return U

def returnLines(U):
    Yaxis=0
    Xaxis=0
    for nodes in U:
        if nodes[0] > Xaxis:
            Xaxis =nodes[0]
        if nodes[1] > Yaxis:
            Yaxis = nodes[1]
    Lines=[]
    # X axis  parallel lines
    for y in range(1,Yaxis + 1):
        Line = []
        for node in U:
            if y ==node[1]:
                Line.append(node)
        if len(Line) == 1:
            Line.append([Line[0][0] + 1, Line[0][1]])
        Lines.append(sorted(Line))
    # Y axis parallel lines
    for x in range(1,Xaxis + 1):
        Line = []
        for node in U:
            if x ==node[0]:
                Line.append(node)
        if len(Line) > 1:
            Lines.append(sorted(Line))
    return Lines

def returnDiagonals(U):
    Diagonals = []
    for node in U:
        FirstLandings = U
        x1 = node[0]
        y1 = node[1]
        for FirstLand in FirstLandings:
            startX = FirstLand[0]
            startY = FirstLand[1]
            if x1 >= startX or y1 >= startY :
                continue
            Line = [node]
            Line.append(FirstLand)
            XStep = x1 - startX
            YStep = y1 - startY
            for additions in U:
                additionx = additions[0]
                additiony = additions[1]
                if Line[-1][0] - additionx == XStep and Line[-1][1] - additiony == YStep:
                    Line.append(additions)
                    if additions in FirstLand:
                     del FirstLand[additions]
            Diagonals.append(Line)
    # pprint(Diagonals)
    return Diagonals


def GreedyAlgorith(U,lines):
    Solution = []
    while U:
        SolutionItem = []
        MaxCoverage = 0
        MaxCoveragePos = 0
        for line in lines:
            Coverage = 0
            for node in U:
                if node in line:
                    Coverage = Coverage +1
            if Coverage >   MaxCoverage:
                MaxCoverage = Coverage
                SolutionItem = line
        Solution.append(SolutionItem)
        for nodes in SolutionItem:
            if nodes in U:
             U.remove(nodes)
    return Solution

def ImprovedAlgorith(U,lines):
    counter = 2
    #  no point starting from 1 , a single line cannot possible be my solution
    while True:
        SubSets = itertools.combinations(lines, counter)
        for Set in SubSets:
            # We check if the set returned from the subsets of lines covers the universe
            Solution = []
            for line in Set:
                    for node in line:
                        if node not in Solution and node in U :
                            Solution.append(node)
            Solution.sort()
            #  if the set does indeed cover the Universe i return the set , breaking the while true .
            U.sort()
            if Solution == U:
                return Set

        counter +=1


def PrintSolution(Solution):
    for Line in Solution:
        for node in Line:
            print(tuple(node), end=" ")
        print("")



if len(sys.argv) == 2:
    TextName = sys.argv[1]
    U = CreateMilkyWay(TextName)
    Lines = returnLines(U)
    Diagonals = returnDiagonals(U)
    Solution = GreedyAlgorith(U , sorted(Lines+Diagonals))
    PrintSolution(Solution)
elif len(sys.argv) == 4:
    TextName = sys.argv[-1]
    U = CreateMilkyWay(TextName)
    Lines = returnLines(U)
    Solution = ImprovedAlgorith(U, Lines )
    PrintSolution(Solution)
elif len(sys.argv) == 3:
    TextName = sys.argv[-1]
    U = CreateMilkyWay(TextName)
    Lines = returnLines(U)
    Solution = GreedyAlgorith(U, Lines )
    PrintSolution(Solution)



