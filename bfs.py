#BFS 
import time
import pygame  # motor gráfico
import sys
import math
import random
from collections import deque
from tkinter import messagebox, Tk

RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SHORTEST_PATH = (239, 48, 188)
COLOR_DE_FONDO = (44, 62, 80)

size = (width, height) = 650, 650
cols, rows = 65, 65
w = h = 10

pygame.init()
win = pygame.display.set_mode(size)
pygame.display.set_caption("Algoritmo de BFS - Presione ENTER para comenzar")
Tk().wm_withdraw()
messagebox.showinfo("Algoritmo de BFS","No mueva la ventana mientras se ejecuta el algoritmo")
clock = pygame.time.Clock

grid = []
queue = deque()
#path = []

flag = noflag = startflag = False

class Spot:
    def __init__(self, i, j):
        self.x, self.y = i, j
        self.path = False
        self.neighbors = []
        self.prev = None
        self.wall = False
        self.visited = False

    def show(self, win, col, shape=1):
        
        if self.wall == True:
            col = (0, 0, 0)  
        if shape == 1:
            pygame.draw.rect(win, col, (self.x*w, self.y*h, w-1, h-1))
        elif shape == 2:
            pygame.draw.rect(win, col, (self.x*w-2, self.y*h-2, w-2, h-2))
        else:
            pygame.draw.circle(win, col, (self.x*w+w//2, self.y*h+h//2), w//3)

    def add_neighbors(self, grid):  # ← ↑ → ↓
        if self.x < cols - 1:   # East Cell:    → ■ 
            self.neighbors.append(grid[self.x+1][self.y])
        if self.x > 0:          # West Cell:    ← ■  
            self.neighbors.append(grid[self.x-1][self.y])
        if self.y < rows - 1:   # North Cell:    ■ ↓ 
            self.neighbors.append(grid[self.x][self.y+1])
        if self.y > 0:          # South Cell:    ■ ↑
            self.neighbors.append(grid[self.x][self.y-1])
def Set_Spots():
    for i in range(cols):
        arr = []
        for j in range(rows):
            arr.append(Spot(i, j)) 
        grid.append(arr)

    for i in range(cols):
        for j in range(rows):
            grid[i][j].add_neighbors(grid)

def Get_Maze(laberinto):
    with open(laberinto, 'r') as rf:
        for i in range(cols):
            line = rf.readline()
            for j in range(rows):
                if line[j] == 'I':
                    grid[j][i].wall = True


def Dijkstra():
    start = grid[0][0]
    end = grid[cols-1][rows-1]

    start.visited = True
    queue.append(start)
    global flag
    global noflag
    flag = False
    noflag = True
    while True:
        if len(queue) > 0: 
            current = queue.popleft() 
                                    
            if current == end:
                temp = current
                while temp.prev: 
                    temp.prev.path = True 
                    temp = temp.prev   
                if not flag:
                    flag = True
                    print("Done")
                elif flag:
                    continue
            if flag == False:
                for i in current.neighbors: 
                                            
                    if not i.visited and not i.wall:
                        i.visited = True
                        i.prev = current
                        queue.append(i)

        if flag and noflag:
            break


laberinto = "Laberinto_1.txt" #modificar el tex según el laberinto
end_maze = False
while True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    startflag = True
    if startflag and not end_maze:
        Set_Spots()
        Get_Maze(laberinto)
        Dijkstra()
        end_maze = True
