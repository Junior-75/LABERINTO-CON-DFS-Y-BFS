import pytest
import os
from app.laberinto import crear_mapa, generar_laberinto, exportar_laberinto, Spot

@pytest.fixture
def mapa_vacio():
    cols, rows = 5, 5
    mapa = crear_mapa(cols, rows)
    return mapa, cols, rows

def test_crear_mapa(mapa_vacio):
    mapa, cols, rows = mapa_vacio
    assert len(mapa) == cols, f"Mapa debería tener {cols} columnas."
    for columna in mapa:
        assert len(columna) == rows, f"Cada columna debería tener {rows} filas."
        for spot in columna:
            assert isinstance(spot, Spot), "Cada celda debe ser una instancia de Spot."

def test_generar_laberinto(mapa_vacio):
    mapa, cols, rows = mapa_vacio
    mapa_generado = generar_laberinto(mapa, cols, rows)
    
    assert not mapa_generado[0][0].pared, "La celda de inicio debería estar abierta."
    assert not mapa_generado[cols-1][rows-1].pared, "La celda de fin debería estar abierta."
    
    from collections import deque
    
    queue = deque()
    queue.append((0, 0))
    visitados = set()
    visitados.add((0, 0))
    
    while queue:
        x, y = queue.popleft()
        if (x, y) == (cols-1, rows-1):
            break
        # Obtener vecinos accesibles
        vecinos = []
        if x < cols - 1 and not mapa_generado[x+1][y].pared:
            vecinos.append((x+1, y))
        if x > 0 and not mapa_generado[x-1][y].pared:
            vecinos.append((x-1, y))
        if y < rows - 1 and not mapa_generado[x][y+1].pared:
            vecinos.append((x, y+1))
        if y > 0 and not mapa_generado[x][y-1].pared:
            vecinos.append((x, y-1))
        for vecino in vecinos:
            if vecino not in visitados:
                visitados.add(vecino)
                queue.append(vecino)
    
    assert (cols-1, rows-1) in visitados, "Debe existir al menos un camino desde inicio hasta fin."

def test_exportar_laberinto(mapa_vacio, tmp_path):
    mapa, cols, rows = mapa_vacio
    generar_laberinto(mapa, cols, rows)
    filename = tmp_path / "test_laberinto.txt"
    exportar_laberinto(mapa, cols, rows, filename)
    
    assert os.path.exists(filename), "El archivo de laberinto no fue creado."
    
    with open(filename, 'r') as f:
        lines = f.readlines()
        assert len(lines) == rows, f"El archivo debería tener {rows} filas."
        for line in lines:
            line = line.strip()
            assert len(line) == cols, f"Cada fila en el archivo deberia tener {cols} caracteres."
            for char in line:
                assert char in ['I', '·'], "Los caracteres deben ser 'I' o '·'."
    
    with open(filename, 'r') as f:
        lines = f.readlines()
        assert lines[0][0] != 'I', "La celda de inicio está bloqueada."
        assert lines[-1][cols-1] != 'I', "La celda de fin está bloqueada."
