import itertools
import sys 
from scipy import stats

class grid:
    def __init__(self, d = 2, p = 0.5, n = 20):
        self.d = d
        self.p = p
        self.n = n
        self.vertex = list(itertools.product(list(range(-n,n+1)), repeat = d))    
        temp = [tuple([-n]*d)]
        edge = {}
        while len(temp) > 0:
            vert = list(temp.pop(0))
            for i in range(len(vert)):
                vert_new = vert.copy()
                vert_new[i] = vert[i]+1
                if max(max(vert_new), -min(vert_new)) <= n:
                    edge[(tuple(vert), tuple(vert_new))] = stats.bernoulli.rvs(p, size=1)[0]
                    if tuple(vert_new) not in temp:
                        temp.append(tuple(vert_new))
        self.edge = edge
    
    # Find open edges from a specific point
    def open_edges(self, vert):
        vert_adj = []
        for i in range(len(vert)):
            vert_new_1 = list(vert).copy(); vert_new_2 = list(vert).copy()
            vert_new_1[i] = vert[i]+1; vert_new_2[i] = vert[i]-1
            if max(max(vert_new_1), -min(vert_new_1)) <= self.n:
                vert_adj.append(tuple(vert_new_1))
            if max(max(vert_new_2), -min(vert_new_2)) <= self.n:
                vert_adj.append(tuple(vert_new_2))
                
        res = []
        for i in vert_adj:
            if (vert, i) in self.edge:
                if self.edge[(vert, i)]:
                    res.append(i)
            if (i, vert) in self.edge:
                if self.edge[(i, vert)]:
                    res.append(i)           
        return res
    
    # Check if there is a path to the border from a specific point
    def check_path_to_border(self, vert):
        temp = [vert]
        visited = []
        while len(temp) > 0:
            vert_temp = temp.pop(0)
            visited.append(vert_temp)
            open_edge = self.open_edges(vert_temp)
            if len(open_edge) > 0:
                for i in range(len(open_edge)):
                    if max(open_edge[i]) == self.n or -min(open_edge[i]) == self.n:
                        return True
                    else:
                        if open_edge[i] not in visited and open_edge[i] not in temp:
                            temp.append(open_edge[i])
        return False
    

if __name__ == '__main__':
    my_grid = grid(n = 100)
    print(len(my_grid.vertex))
    print(len(my_grid.edge))
    print(sys.getsizeof(my_grid)/2**30)
    print(my_grid.open_edges((0,0)))
    print(my_grid.check_path_to_border((0,0)))

