#!/usr/bin/env python3
import matplotlib.pyplot as plt
import networkx as nx
from itertools import product

class InvalidMatrixException(Exception):
    pass

def input_digraph() -> list[list[int]]:
    first_line = list(map(int, input().split()))
    set_line = set(first_line)

    if set_line != set([1]) and set_line != set([0]) and set_line != set([0,1]):
        raise InvalidMatrixException("Adjacency matrix can only contain 0 or 1")
    n = len(first_line)

    m = [first_line]

    for _ in range(n-1):
        line =list(map(int, input().split()))
        set_line = set(line)
        if set_line != set([1]) and set_line != set([0]) and set_line != set([0,1]):
            raise InvalidMatrixException("Adjacency matrix can only contain 0 or 1")
        if len(line) != n:
            raise InvalidMatrixException("Invalid matrix line size")
        m.append(line)
    return m

def digraph_levels(m: list[list[int]]):
    levels=[]
    n = len(m[0])
    lmbd = [sum(i) for i in m]
    levels.append([i for i in range(n) if lmbd[i]==0])
    if lmbd == [0]*n: return [lmbd]
    while (set(lmbd) != set([0]) ):
        new_lmbd = [0]*n
        level = []
        has_circuit = True
        for i in range(n):
            s = 0
            for j in range(n):
                if lmbd[j]!=0:
                    s+=m[i][j]
            new_lmbd[i] = s
            if lmbd[i] != 0 and s == 0:
                level.append(i)
                has_circuit=False
        if has_circuit: return False
        lmbd = new_lmbd
        levels.append(level)
    return levels

def grundy_from_levels(m, levels):
    n = len(m[0])
    grundy_values = [0]*n
    if len(grundy_values) > 1:
        for v in levels[1]:
            grundy_values[v] = 1
        for level in levels[2:]:
            for v in level:
                temp = [dv for i,dv in enumerate(grundy_values) if m[v][i] == 1]
                temp = set(temp)
                mex = 0
                while mex in temp:
                    mex += 1
                grundy_values[v] = mex
    return grundy_values 

def graph_cores(m):
    n = len(m)
    cnf1 = []
    for i in range(n):
        for j in range(n):
            if m[i][j] == 1:
                cnf1.append((i,j))
    
    cnf2 = []
    for i in range(n):
        dis = [i]
        for j in range(n):
            if m[i][j] == 1:
                dis.append(j)
        cnf2.append(dis)
    
    cores = []

    for line in product([0,1], repeat=n):
        res = True
        for dis in cnf1:
            res = res and (not line[dis[0]] or not line[dis[1]])
        for dis in cnf2:
            res = res and any(line[i] for i in dis)
        if res == True:
            cores.append(line)
    
    for i in range(len(cores)):
        cores[i] = [j for j,v in enumerate(cores[i]) if v==1]
    return cores

def rec_grundy(matrix, vertex, core):
    if vertex in core:
        return 0
    values = [rec_grundy(matrix, i, core) for i in range(len(matrix)) if matrix[vertex][i]]
    result = 0
    while result in values:
        result += 1
    return result

def graph_display(m, grundy):
    G = nx.DiGraph()
    n = len(m[0])
    for i in range(n):
        G.add_node(str(i+1)+' ('+str(grundy[i]) +")")
        for j in range(n):
            if m[i][j] == 1:
                G.add_edge(str(i+1)+' ('+str(grundy[i]) + ')' ,str(j+1)+' ('+str(grundy[j]) + ')')
    nx.draw_planar(G, with_labels=True, node_size=1300,font_weight="bold")
    plt.show()

def main():
    m = input_digraph()
    l = digraph_levels(m)
    n=len(m)
    if l:
        grundy = grundy_from_levels(m,l)
        graph_display(m, grundy)
    else:
        print("Орграф содержит контуры, переходим к поиску ядер.")
        cores = graph_cores(m)
        if cores == []:
            print("Функция Гранди недопустима для этого графа")
        else:
            for core in cores:
                grundy = [rec_grundy(m,i,core) for i in range(n)]
                graph_display(m, grundy)

if __name__ == "__main__":
    main()
