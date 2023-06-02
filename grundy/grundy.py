#!/usr/bin/env python3
import matplotlib.pyplot as plt
import networkx as nx
from time import sleep

class InvalidMatrixException(Exception):
    pass

class InvalidGraphException(Exception):
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
        set_line = set(first_line)
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
    levels.append([i+1 for i in range(n) if lmbd[i]==0])
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
                level.append(i+1)
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
            grundy_values[v-1] = 1
        for level in levels[2:]:
            for v in level:
                temp = [dv for i,dv in enumerate(grundy_values) if m[v-1][i] == 1]
                temp = set(temp)
                mex = 0
                while mex in temp:
                    mex += 1
                grundy_values[v-1] = mex
    return grundy_values 

def graph_display(m, grundy):
    G = nx.DiGraph()
    n = len(m[0])
    for i in range(n):
        G.add_node(str(i+1)+' ('+str(grundy[i]) +")")
        for j in range(n):
            if m[i][j] == 1:
                G.add_edge(str(i+1)+' ('+str(grundy[i]) + ')' ,str(j+1)+' ('+str(grundy[j]) + ')')
    nx.draw_shell(G, with_labels=True, node_size=1300,font_weight="bold")
    plt.show()


def rec_grundy(matrix, v0, vertex):
    if not any(matrix[vertex-1]):
        return 0
    
    if v0 == vertex:
        return 0
    
    values = [rec_grundy(matrix, v0, i+1) for i in range(len(matrix)) if matrix[vertex-1][i]]
    result = 0
    while result in values:
        result += 1
    return result

def main():
    m = input_digraph()
    l = digraph_levels(m)
    if l:
        g = grundy_from_levels(m,l)
        graph_display(m,g)
    else:
        for v0 in range(1, len(m[0])+1):
            for v in [i + 1 for i in range(len(m[0])) if m[v0-1][i]]:
                print(v)
                if rec_grundy(m,v0,v) == 1:
                    g = [rec_grundy(m,v0,i+1) for i in range(len(m[0]))]
                    graph_display(m,g)
                    return


if __name__ == "__main__":
    main()
