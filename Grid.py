from utilis import *
import time
import tkinter as tk
import pprint
from collections import deque
import math
from queue import PriorityQueue

class Cell:
  presses = 0
  def __init__(self, row, col, maxRow, maxCol, canvas, window, width, height, x0, y0, xf, yf, blocker = False):
    self.blocker = blocker
    self.processed = False
    self.row = row
    self.col = col
    self.maxRow = maxRow
    self.maxCol = maxCol
    self.adj = setWeights(getAdj(row, col, maxRow, maxCol))
    self.origin = False
    self.goal = False
    self.x0 = x0
    self.y0 = y0
    self.xf = xf
    self.yf = yf
    self.canvas = canvas
    self.window = window
    self.already_pressed = False
    self.width = width
    self.height = height
    self.rectangle = self.canvas.create_rectangle(x0, y0, xf, yf, fill='white', width=0, tags="{}|{}".format(row, col))
    self.canvas.tag_bind(self.rectangle, '<Button-1>', self.downPress)
    self.canvas.tag_bind(self.rectangle, '<ButtonRelease-1>', self.upPress)
    self.canvas.tag_bind(self.rectangle, '<B1-Motion>', self.motion)

  def __eq__(self, other):
    return self.row == other.row and self.col == other.col

  def __str__(self):
    return "Row: {}\nCol: {}\n".format(self.row, self.col)

  def createRectangle(self):
    pass

  def downPress(self, event):
    if Cell.presses == 0:
      self.setOrigin()
      Cell.presses += 1
      print("Origin Set")
    elif self.presses == 1:
      self.setGoal()
      Cell.presses += 1
      print("Goal Set")
    else:
      Cell.presses = 3
      self.switch()

  def motion(self, event):
    if Cell.presses < 3:
      return

    y = event.y
    x = event.x

    # if (row < 0 or row > self.height) or (col < 0 or col > self.width):
    #   return

    cons = list(filter(lambda cell: (x >= cell.x0 and x <= cell.xf and y >= cell.y0 and y <= cell.yf) , sum(self.grid, [])))
    if cons:
      cons[0].switch()
    # self.grid[row // self.y_run][col // self.x_run].switch()row
          
  def upPress(self, event):
    for row in self.grid:
      for cell in row:
        cell.already_pressed = False

  def switch(self):
    if self.already_pressed:
      return
    self.already_pressed = True
    if self.origin or self.goal:
      return
    self.blocker = not self.blocker

    # it is now a blocker
    if self.blocker:
      for (row, col) in self.adj.keys():
        self.grid[row][col].adj.pop((self.row, self.col))
      self.adj = {}
      self.canvas.itemconfig(self.rectangle, fill="gray")
    else:
      self.adj = setWeights(getAdj(self.row, self.col, self.maxRow, self.maxCol))
      for (row, col) in self.adj.keys():
        self.grid[row][col].adj[(self.row, self.col)] = 1
      self.canvas.itemconfig(self.rectangle, fill="white")

  def stringAdj(self):
    return "\n".join(map(lambda cell: "Location: {}, Weight: {}".format(cell[0], cell[1]), self.adj.items()))

  def reset(self):
    self.blocker = False
    self.processed = False
    self.adj = setWeights(getAdj(self.row, self.col, self.maxRow, self.maxCol))
    self.canvas.itemconfig(self.rectangle, fill="white")
    if self.origin:
      self.setOrigin()
    if self.goal:
      self.setGoal()

  def resetWeights(self):
    for key in self.adj.keys():
      self.adj[key] = 1

  def setOrigin(self):
    self.origin = True
    self.canvas.itemconfig(self.rectangle, fill="green")

  def setGoal(self):
    self.goal = True
    self.canvas.itemconfig(self.rectangle, fill="red")

  def process(self):
    self.processed = True
    self.canvas.itemconfig(self.rectangle, fill="blue")

class Edge:
  def __init__(self):
    pass

class Grid:
  def __init__(self, width, height, maxRow, maxCol) -> None:
    self.width = width
    self.height = height
    self.maxRow = maxRow
    self.maxCol = maxCol
    self.window = tk.Tk()
    self.canvas = tk.Canvas(self.window, width=width, height=height)
    self.canvas.grid(row=0, column=0)
    self.struct = []
    self.processed = set()
    self.colors = ["white", "black", "red", "green", "blue", "cyan", "yellow"]
    self.alg_started = False
    self.running = False
    self.origin = (-1, -1)
    self.goal = (-1, -1)
    self.grid = []
    button = tk.Button(self.window, text="DFS", command=self.dfs)
    button.grid()
    button = tk.Button(self.window, text="BFS", command=self.bfs)
    button.grid()
    button = tk.Button(self.window, text="AStar", command=self.aStar)
    button.grid()
    button = tk.Button(self.window, text="Reset", command=self.resetGrid)
    button.grid()
    self.speedScale = tk.Scale(self.window, from_=1, to=200, orient=tk.HORIZONTAL)
    self.speedScale.set(100)
    self.speedScale.grid(row=0, column=1)
    self.edgeGrid = []
    self.isEdgeGrid = False
    self.enableEdgesButton = tk.Button(self.window, text="EnableEdges", command=self.enableEdges, state=tk.DISABLED)
    self.enableEdgesButton.grid()
    self.disableEdgesButton = tk.Button(self.window, text="Disable Edges", command=self.disableEdges)
    self.disableEdgesButton.grid()
    self.disableEdges()
  
  def enableEdges(self):
    self.canvas.delete(tk.ALL)
    Cell.presses = 0
    self.enableEdgesButton["state"] = tk.DISABLED
    self.disableEdgesButton["state"] = tk.NORMAL
    self.origin = (-1, -1)
    self.goal = (-1, -1)
    x_run = self.width // self.maxCol
    y_run = self.height // self.maxRow
    self.grid = [[Cell(row, col, self.maxRow, self.maxCol, self.canvas, self.window, self.width, self.height, 
                          x_run * col, y_run * row, x_run * (col + 1), y_run * (row + 1)) for col in range(self.maxCol)] for row in range(self.maxRow)]
    for row in self.grid:
      for cell in row:
        cell.grid = self.grid

  def disableEdges(self):
    self.canvas.delete(tk.ALL)
    Cell.presses = 0

    self.enableEdgesButton["state"] = tk.NORMAL
    self.disableEdgesButton["state"] = tk.DISABLED
    self.origin = (-1, -1)
    self.goal = (-1, -1)
    x_run = self.width // self.maxCol
    y_run = self.height // self.maxRow
    self.grid = [[Cell(row, col, self.maxRow, self.maxCol, self.canvas, self.window, self.width, self.height, 
                          x_run * col, y_run * row, x_run * (col + 1), y_run * (row + 1)) for col in range(self.maxCol)] for row in range(self.maxRow)]
    for row in self.grid:
      for cell in row:
        cell.grid = self.grid


  def setOriginAndGoal(self):
    for row in range(self.maxRow):
      for col in range(self.maxCol):
        if self.grid[row][col].origin:
          self.origin = (row, col)
        if self.grid[row][col].goal:
          self.goal = (row, col)

  def dfs(self):
    if not self.alg_started:
      self.setOriginAndGoal()
      self.processed = set()
      self.struct = deque()
      self.struct.append(self.origin)
      self.dfs_process(self.struct, self.processed)

  def dfs_process(self, stack, processed):
    (row, col) = stack.pop()
    processed.add((row, col))
    self.grid[row][col].process()
    adj = list(filter(lambda x: (x not in processed), self.grid[row][col].adj.keys()))
    stack = list(filter(lambda x: not x in adj, stack))
    stack.extend(adj)

    if not (row, col) == self.goal and not len(stack) == 0:
      self.window.after(201 - self.speedScale.get(), self.dfs_process, stack, processed)

  def aStar(self):
    if not self.alg_started:
      self.setOriginAndGoal()
      self.processed = set()
      self.struct = PriorityQueue()
      self.heur = {}
      self.travCost = {}
      for lst in self.grid:
        for cell in lst:
          self.heur[(cell.row, cell.col)] = math.sqrt((self.goal[0] - cell.row)**2 + (self.goal[1] - cell.col)**2)
      self.struct.put((self.heur[self.origin], self.origin))
      self.travCost[self.origin] = 0
      self.aStar_process(self.struct, self.processed)

  def aStar_process(self, pQueue, processed):
    (c, (row, col)) = pQueue.get()

    # print("Cost:{} for ({}, {})".format(c, row, col))


    if (row, col) in processed:
      self.window.after(0, self.aStar_process, pQueue, processed)
      return
    processed.add((row, col))
    self.grid[row][col].process()
    adj = list(filter(lambda x: (x[0] not in processed), list(self.grid[row][col].adj.items())))

    for (adjacency, cost) in adj:
      if adjacency in processed:
        continue
        
      self.travCost[adjacency] = min(self.travCost[adjacency], self.travCost[(row, col)] + cost) if self.travCost.get(adjacency) else self.travCost[(row, col)] + cost
      pQueue.put((self.travCost[adjacency] + self.heur[adjacency], adjacency))

    if not (row, col) == self.goal and not pQueue.empty():
      self.window.after(201 - self.speedScale.get(), self.aStar_process, pQueue, processed)

  def resetGrid(self):
    self.struct = []
    self.processed = set()

    for row in range(self.maxRow):
      for col in range(self.maxCol):
        self.grid[row][col].reset()

  def bfs(self):
    if not self.alg_started:
      self.setOriginAndGoal()
      self.processed = set()
      self.struct = []
      self.struct.append(self.origin)
      self.bfs_process(self.struct, self.processed)

  def bfs_process(self, queue, processed):
    (row, col) = queue.pop(0)
    if (row, col) in processed:
      self.window.after(0, self.bfs_process, queue, processed)
      return
    processed.add((row, col))
    self.grid[row][col].process()
    adj = list(filter(lambda x: (x not in processed) and (x not in queue), self.grid[row][col].adj.keys()))
    queue.extend(adj)
    # print(queue)

    if not (row, col) == self.goal and not len(queue) == 0:
      self.window.after(201 - self.speedScale.get(), self.bfs_process, queue, processed)

  def clearWeights(self):
    for lst in self.grid:
      for cell in lst:
        cell.resetWeights()

  
def runner():
  # Max Row and Col need to be odd for the edge rep
  maxRow = 25
  maxCol = 25
  width = 500
  height = 500
  grid = Grid(width=width, height=height, maxRow=maxRow, maxCol=maxCol)

  tk.mainloop()



if __name__ == "__main__":
  runner()