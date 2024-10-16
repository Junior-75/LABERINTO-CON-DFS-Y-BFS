from bfs import ejecutar_bfs  # Importar: ejecutar BFS
from dfs import ejecutar_dfs  # Importar: ejecutar DFS
import sys      # System events

def elegir_algoritmo(): #Menu para seleccionar el algoritmo de busqueda
    print("Selecciona el algoritmo:")
    print("1. BFS")
    print("2. DFS")
    opcion = input("Introduce tu eleccion (1 o 2): ")

    laberinto = input("Introduce el nombre del archivo de laberinto (ejemplo: Laberinto_1.txt): ")

    if opcion == '1':
        print("Ejecutando BFS: ")
        ejecutar_bfs(laberinto)  # Ejecuta BFS solo cuando el usuario lo seleccione
    elif opcion == '2':
        print("Ejecutando DFS: ")
        ejecutar_dfs(laberinto)  # Ejecuta DFS solo cuando el usuario lo seleccione
    else:
        print("Intentar de nuevo.")
        sys.exit()

def mostrar_menu(): #Mostrar menu para elegir algoritmo
    while True:
        print("--- Menu ---")
        print("1. Seleccionar Algoritmo de Búsqueda (BFS o DFS)")
        print("2. Salir")
        eleccion = input("Selecciona una opcion: ")

        if eleccion == '1':
            elegir_algoritmo()
        elif eleccion == '2':
            print("Saliendo.")
            sys.exit()
        else:
            print("Intentar de nuevo.")

if __name__ == '__main__':
    mostrar_menu()
