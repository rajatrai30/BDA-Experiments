import sys
from collections import OrderedDict

class MapReduce:
    def __init__(self):
        self.intermediate = OrderedDict()
        self.result = []

    def emitIntermediate(self, key, value):
        self.intermediate.setdefault(key, [])
        self.intermediate[key].append(value)

    def emit(self, value):
        self.result[value[0]][value[1]] = value[2]

    def execute(self, matrix1, matrix2, mapper, reducer):
        n = len(matrix1)
        m = len(matrix2[0])
        for i in range(0, n):
            self.result.append([0] * m)
        mapper(matrix1, matrix2)

        for key in self.intermediate:
            reducer(key, self.intermediate[key])
        for i in range(0, n):
            row = ""
            for j in range(0, m):
                row += str(self.result[i][j]) + " "
            print(row)

mapReducer = None

def mapper(matrix1, matrix2):
    n = len(matrix1)
    m = len(matrix2)
    l = len(matrix2[0])
    for i in range(0, n):
        for j in range(0, l):
            mapReducer.emitIntermediate((i, j), matrix1[i])
            column = []
            for k in range(0, m):
                column.append(matrix2[k][j])
            mapReducer.emitIntermediate((i, j), column)

def reducer(key, list_of_values):
    l1 = list_of_values[0]
    l2 = list_of_values[1]
    dot_product = 0
    m = len(l1)
    for i in range(0, m):
        dot_product += l1[i] * l2[i]
    mapReducer.emit((key[0], key[1], dot_product))

if __name__ == '__main__':
    testcases = int(sys.stdin.readline().strip())
    for t in range(0, testcases):
        mapReducer = MapReduce()
        dimensions = sys.stdin.readline().strip().split(" ")
        row = int(dimensions[0])
        column = int(dimensions[1])
        matrix1 = []
        matrix2 = []
        for i in range(0, row):
            read_row = sys.stdin.readline().strip()
            matrix1.append([])
            row_elems = read_row.strip().split()
            for j in range(0, len(row_elems)):
                matrix1[i].append(int(row_elems[j]))
        
        dimensions = sys.stdin.readline().strip().split(" ")
        row = int(dimensions[0])
        column = int(dimensions[1])
        
        for i in range(0, row):
            read_row = sys.stdin.readline().strip()
            matrix2.append([])
            row_elems = read_row.strip().split()
            for j in range(0, len(row_elems)):
                matrix2[i].append(int(row_elems[j]))
        
        mapReducer.execute(matrix1, matrix2, mapper, reducer)
