import random
import os
import re

class Spot:
    def __init__(self, i, j):
        self.x, self.y = i, j
        self.pared = True
        self.visitado = False

def crear_mapa(cols, rows):
    mapa = []
    for i in range(cols):
        arr = []
        for j in range(rows):
            arr.append(Spot(i, j))
        mapa.append(arr)
    return mapa

def quitar_pared_este(mapa, x, y):
    if x + 2 < len(mapa):
        mapa[x+1][y].pared = False
        mapa[x+2][y].pared = False
    else:
        print(f"No se puede quitar pared al Este desde ({x}, {y}) - Fuera de limites.")

def quitar_pared_oeste(mapa, x, y):
    if x - 2 >= 0:
        mapa[x-1][y].pared = False
        mapa[x-2][y].pared = False
    else:
        print(f"No se puede quitar pared al Oeste desde ({x}, {y}) - Fuera de limites.")

def quitar_pared_norte(mapa, x, y):
    if y - 2 >= 0:
        mapa[x][y-1].pared = False
        mapa[x][y-2].pared = False
    else:
        print(f"No se puede quitar pared al Norte desde ({x}, {y}) - Fuera de limites.")

def quitar_pared_sur(mapa, x, y):
    if y + 2 < len(mapa[0]):
        mapa[x][y+1].pared = False
        mapa[x][y+2].pared = False
    else:
        print(f"No se puede quitar pared al Sur desde ({x}, {y}) - Fuera de limites.")

def generar_laberinto(mapa, cols, rows):
    lista = []
    x, y = 0, 0
    lista.append((x, y))
    mapa[x][y].pared = False
    print(f"Generando laberinto")

    while lista:
        celda_actual = lista[-1]
        x, y = celda_actual
        mapa[x][y].visitado = True

        direcciones = []
        if x < cols - 2 and not mapa[x+2][y].visitado:
            direcciones.append("Este")
        if x > 1 and not mapa[x-2][y].visitado:
            direcciones.append("Oeste")
        if y < rows - 2 and not mapa[x][y+2].visitado:
            direcciones.append("Sur")
        if y > 1 and not mapa[x][y-2].visitado:
            direcciones.append("Norte")

        if direcciones:
            direccion = random.choice(direcciones)
            if direccion == "Este":
                quitar_pared_este(mapa, x, y)
                x += 2
            elif direccion == "Oeste":
                quitar_pared_oeste(mapa, x, y)
                x -= 2
            elif direccion == "Norte":
                quitar_pared_norte(mapa, x, y)
                y -= 2
            elif direccion == "Sur":
                quitar_pared_sur(mapa, x, y)
                y += 2
            lista.append((x, y))
        else:
            lista.pop()

    print("Generación del laberinto completada.")
    return mapa

def exportar_laberinto(mapa, cols, rows, filename):
    try:
        with open(filename, 'w') as wf:
            for y in range(rows):
                for x in range(cols):
                    if mapa[x][y].pared:
                        wf.write("I")
                    else:
                        wf.write("·")
                wf.write("\n")
        print(f"Laberinto exportado a '{filename}'.")
    except Exception as e:
        print(f"Error al exportar el laberinto: {e}")
    return filename

def obtener_siguiente_index(prefijo, extension=".txt"):
    pattern = re.compile(rf"{re.escape(prefijo)}(\d+){re.escape(extension)}$")
    max_index = 0
    for archivo in os.listdir('.'):
        match = pattern.match(archivo)
        if match:
            index = int(match.group(1))
            if index > max_index:
                max_index = index
    return max_index + 1

def main():
    try:
        cols, rows = 65, 65  # Ajustar el tamaño del laberinto
        mapa = crear_mapa(cols, rows)
        mapa = generar_laberinto(mapa, cols, rows)
        
        laberinto = 'Laberinto_'
        extension = '.txt'
        index = obtener_siguiente_index(laberinto, extension)
        filename = f"{laberinto}{index}{extension}"
        
        exportar_laberinto(mapa, cols, rows, filename)
    except Exception as e:
        print(f"Error durante la generación del laberinto: {e}")

if __name__ == "__main__":
    main()
