import matplotlib.pyplot as plt
import networkx as nx


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

def digraph_levels(m: list[list[int]]) -> list[list[int]]:
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

def graph_display(m: list[list[int]]):
    G = nx.DiGraph()
    n = len(m[0])
    for i in range(n):
        G.add_node(i+1)
        for j in range(n):
            if m[i][j] == 1:
                G.add_edge(i+1,j+1)
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()

def main():
    m = input_digraph()
    print(digraph_levels(m))
    graph_display(m)

if __name__ == "__main__":
    main()

#nx.draw(G, with_labels=True, font_weight='bold')
#plt.show()