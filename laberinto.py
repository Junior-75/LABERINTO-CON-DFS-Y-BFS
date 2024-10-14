import os       # Manipulacion de directorios
import sys      # Eventos del sistema
import pygame   # Motor grafico
import random   # Random
from tkinter import messagebox, Tk  # Messagebox

rojo = (255, 0, 0)
azul = (0, 0, 255)
negro = (0, 0, 0)
indicador = (239, 48, 188)
fondo = (44, 62, 80)
laberinto = 'Laberinto_'
indice = 1
directorio = laberinto + str(indice) + '.txt'

size = (width, height) = 650, 650
columna, fila = 65, 65
w = h = 10

pygame.init()
win = pygame.display.set_mode(size)
pygame.display.set_caption(laberinto.replace('_', ' - ENTER'))
clock = pygame.time.Clock

mapa = []
lista = []
inicio = False
fin = False


class Spot:
    def __init__(self, i, j):
        self.x, self.y = i, j
        self.pared = True
        self.visitado = False

    def show(self, win, columna):
        if self.pared == True:
            columna = negro
        pygame.draw.rect(win, columna, (self.x*w, self.y*h, w-1, h-1))

def ParedEste(x, y):
    mapa[x+1][y].pared = False
    mapa[x+2][y].pared = False


def ParedOeste(x, y):
    mapa[x-1][y].pared = False
    mapa[x-2][y].pared = False


def ParedNorte(x, y):
    mapa[x][y-1].pared = False
    mapa[x][y-2].pared = False


def ParedSur(x, y):
    mapa[x][y+1].pared = False
    mapa[x][y+2].pared = False


def UnicaCelda(x, y):
    mapa[x][y].show(win, indicador)
    pygame.display.flip()


def Grafo():
    win.fill(negro)
    for i in range(columna):
        for j in range(fila):
            spot = mapa[i][j]
            spot.show(win, fondo)
            if spot == mapa[0][0]:
                spot.show(win, azul)
            if spot == mapa[columna-1][fila-1]:
                spot.show(win, rojo)
    pygame.display.flip()


def Maze(x, y):
    UnicaCelda(x, y)
    lista.append((x, y))
    while len(lista) > 0:
        celda = []
        if x < columna - 2:  
            if not(mapa[x+2][y].visitado):
                celda.append("Este")
        if x > 1:         
            if not(mapa[x-2][y].visitado):
                celda.append("Oeste")
        if y < fila - 2:   
            if not(mapa[x][y+2].visitado):
                celda.append("Sur")
        if y > 1:          
            if not(mapa[x][y-2].visitado):
                celda.append("Norte")

        if len(celda) > 0:
            current_cell = (random.choice(celda))

            if current_cell == "Este":
                ParedEste(x, y)
                x = x+2
                mapa[x-1][y].visitado = True
                mapa[x][y].visitado = True
                lista.append((x, y))

            elif current_cell == "Oeste":
                ParedOeste(x, y)
                x = x-2
                mapa[x+1][y].visitado = True
                mapa[x][y].visitado = True
                lista.append((x, y))

            elif current_cell == "Norte":
                ParedNorte(x, y)
                y = y - 2
                mapa[x][y+1].visitado = True
                mapa[x][y].visitado = True
                lista.append((x, y))

            elif current_cell == "Sur":
                ParedSur(x, y)
                y = y + 2
                mapa[x][y-1].visitado = True
                mapa[x][y].visitado = True
                lista.append((x, y))
        else:
            x, y = lista.pop()
        Grafo()
        UnicaCelda(x, y)
        pygame.display.flip()
    global fin
    fin = True


def EscribirArchivo():
    global directorio
    global indice
    while directorio in os.listdir():
        indice += 1
        directorio = laberinto + str(indice) + '.txt'

    with open(directorio, 'w') as wf:
        for i in range(columna):
            for j in range(fila):
                if mapa[j][i].pared:
                    wf.write("I")
                else:
                    wf.write("·")
            wf.write("\n")
    return directorio


# PROGRAMA PRINCIPAL
for i in range(columna):
    arr = []
    for j in range(fila):
        arr.append(Spot(i, j))
    mapa.append(arr)

start = mapa[0][0]
start.pared = False
end = mapa[columna-1][fila-1]
end.pared = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                inicio = True
    if inicio and not fin:
        Maze(0, 0)
        msg = EscribirArchivo()
        Tk().wm_withdraw()
        messagebox.showinfo("Generador de laberintos","El laberinto ha sido generado" + directorio)