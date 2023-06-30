def getAdj(row, col, maxRow, maxCol) -> list:
  adj = []

  for i in range(-1, 2):
    for j in range(-1, 2):
      if i == 0 and j == 0:
        continue
        
      adj.append((row + i, col + j))

  adj = list(filter(lambda x: x[0] >= 0 and x[0] < maxRow and x[1] >= 0 and x[1] < maxCol, adj))

  return adj

def setWeights(lst):
  return dict(zip(lst, [1 for _ in range(len(lst))]))