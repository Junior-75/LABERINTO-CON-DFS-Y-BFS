# DFS
import pygame 
import sys
from tkinter import messagebox, Tk

RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
SHORTEST_PATH = (239, 48, 188)
COLOR_DE_FONDO = (44, 62, 80)

cols, rows = 65, 65
w = h = 10

grid = []
stack = []
startflag = False
end_maze = False

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

    def add_neighbors(self, grid):
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x+1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x-1][self.y])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y+1])
        if self.y > 0:
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

def Grafico(win):
    win.fill(BLACK)
    for i in range(cols):
        for j in range(rows):
            spot = grid[i][j]
            spot.show(win, COLOR_DE_FONDO)
            if spot.path:
                spot.show(win, COLOR_DE_FONDO)
                spot.show(win, SHORTEST_PATH)
            elif spot.visited:
                spot.show(win, GREEN)
            if spot in stack and not flag:
                spot.show(win, SHORTEST_PATH)
            if spot == grid[0][0]:
                spot.show(win, BLUE)
            if spot == grid[cols-1][rows-1]:
                spot.show(win, RED)
    pygame.display.flip()


def DFS():
    start = grid[0][0]
    end = grid[cols-1][rows-1]

    start.visited = True
    stack.append(start)

    global flag
    global noflag
    flag = False
    noflag = True

    while stack:
        current = stack.pop()  # LIFO
        if current == end:
            temp = current
            while temp.prev: 
                temp.prev.path = True 
                temp = temp.prev
            if not flag:
                flag = True
                noflag = False
                print("Camino encontrado")
            elif flag:
                continue

        if not flag:
            for neighbor in current.neighbors:
                if not neighbor.visited and not neighbor.wall:
                    neighbor.visited = True
                    neighbor.prev = current
                    stack.append(neighbor)
        
        Grafico()
        if flag and noflag:
            break

def ejecutar_dfs(laberinto): #Función para ejecutar BFS e iniciar pygame solo cuando sea lo soliciten
    pygame.init()
    win = pygame.display.set_mode((650, 650))
    pygame.display.set_caption("Algoritmo de DFS - Presione ENTER para comenzar")
    Tk().wm_withdraw()
    #messagebox.showinfo("Algoritmo de DFS", "No mueva la ventana mientras se ejecuta el algoritmo")

    Set_Spots()
    Get_Maze(laberinto)
    DFS(win)

    # Esperar a que el usuario cierre la ventana
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
