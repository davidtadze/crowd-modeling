def create1D(length, value=None):
    return [value] * length


def create2D(rowCount, colCount, value=None):
    a = [None] * rowCount
    for row in range(rowCount):
        a[row] = [value] * colCount
    return a