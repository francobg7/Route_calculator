import heapq

# Solicitar al usuario que ingrese la cantidad de listas y sublistas
cantidad_listas = int(input("Ingrese la cantidad de listas: "))
cantidad_sublistas = int(input("Ingrese la cantidad de elementos en cada sublista: "))

# Crear la lista de listas con puntos
lista = [["." for _ in range(cantidad_sublistas)] for _ in range(cantidad_listas)]

# Solicitar al usuario las coordenadas de entrada y salida
entrada_x, entrada_y = map(int, input(f"Ingrese las coordenadas del primer punto(0 a {cantidad_listas - 1}, 0 a {cantidad_sublistas - 1}) separadas por espacio: ").split())
salida_x, salida_y = map(int, input(f"Ingrese las coordenadas del segundo punto(0 a {cantidad_listas - 1}, 0 a {cantidad_sublistas - 1}) separadas por espacio: ").split())

# Marcar las coordenadas de entrada y salida
lista[entrada_x][entrada_y] = "0"
lista[salida_x][salida_y] = "0"

def colocar_edificios(lista):
    num_edificios = int(input("Ingrese la cantidad de edificios: "))
    for _ in range(num_edificios):
        while True:
            x, y = map(int, input(f"Ingrese las coordenadas del edificio (0 a {cantidad_listas - 1}, 0 a {cantidad_sublistas - 1}) separadas por espacio: ").split())
            if lista[x][y] == ".":
                lista[x][y] = "E"
                break
            else:
                print("Celda ocupada. Intente en otra celda.")

def colocar_agua(lista):
    num_agua = int(input("Ingrese la cantidad de arroyos: "))
    for _ in range(num_agua):
        while True:
            x, y = map(int, input(f"Ingrese la coordenada inicial del arroyo (0 a {cantidad_listas - 1}, 0 a {cantidad_sublistas - 1}) separadas por espacio: ").split())
            orientacion = input("Ingrese la orientación del agua (H para horizontal, V para vertical): ").upper()
            if orientacion == "H":
                if y + 2 < cantidad_sublistas and lista[x][y] == "." and lista[x][y + 1] == "." and lista[x][y + 2] == ".":
                    for i in range(3):
                        lista[x][y + i] = "A"
                    break
                else:
                    print("Celdas ocupadas o fuera de límites. Intente en otras celdas.")
            elif orientacion == "V":
                if x + 2 < cantidad_listas and lista[x][y] == "." and lista[x + 1][y] == "." and lista[x + 2][y] == ".":
                    for i in range(3):
                        lista[x + i][y] = "A"
                    break
                else:
                    print("Celdas ocupadas o fuera de límites. Intente en otras celdas.")

def colocar_baches(lista):
    num_baches = int(input("Ingrese la cantidad de baches: "))
    for _ in range(num_baches):
        while True:
            x, y = map(int, input(f"Ingrese las coordenadas del bache (0 a {cantidad_listas - 1}, 0 a {cantidad_sublistas - 1}) separadas por espacio: ").split())
            if lista[x][y] == ".":
                lista[x][y] = "B"
                break
            else:
                print("Celda ocupada. Intente en otra celda.")

# Colocar los obstáculos en el mapa
colocar_edificios(lista)
colocar_agua(lista)
colocar_baches(lista)

# Algoritmo A*
def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def busqueda_a_estrella(mapa, inicio, objetivo): #parametros
    vecinos = [(0, 1), (0, -1), (1, 0), (-1, 0)] #derecha, izquierda, arriba, abajo
    lista_abierta = []
    heapq.heappush(lista_abierta, (0 + heuristica(inicio, objetivo), 0, inicio)) #f_score,g_score,nodo
    de_donde_vino = {}
    g_score = {inicio: 0} #costo real acumulado, coste actual
    f_score = {inicio: heuristica(inicio, objetivo)} #coste total estimado

    while lista_abierta:
        actual = heapq.heappop(lista_abierta)[2] #Extrae el nodo con la menor prioridad de lista_abierta y lo asigna a actual.

        if actual == objetivo:
            camino = []
            while actual in de_donde_vino:
                camino.append(actual)#Añade el nodo actual a la lista camino.
                actual = de_donde_vino[actual] #Actualiza actual para ser el nodo desde el cual llegamos al nodo actual.
            camino.append(inicio) #Añade el nodo inicial al final de la lista camino.
            camino.reverse()
            return camino

        for vecino in vecinos:
            vecino_pos = (actual[0] + vecino[0], actual[1] + vecino[1]) #nueva posicion
            if 0 <= vecino_pos[0] < len(mapa) and 0 <= vecino_pos[1] < len(mapa[0]):
                if mapa[vecino_pos[0]][vecino_pos[1]] in ["E", "A"]:
                    continue
                puntaje_tentativo_g = g_score[actual] + 1

                if vecino_pos not in g_score or puntaje_tentativo_g < g_score[vecino_pos]:
                    de_donde_vino[vecino_pos] = actual
                    g_score[vecino_pos] = puntaje_tentativo_g
                    f_score[vecino_pos] = puntaje_tentativo_g + heuristica(vecino_pos, objetivo)
                    heapq.heappush(lista_abierta, (f_score[vecino_pos], puntaje_tentativo_g, vecino_pos))

    return None

# Encontrar el camino usando A*
inicio = (entrada_x, entrada_y)
fin = (salida_x, salida_y)
camino = busqueda_a_estrella(lista, inicio, fin)

# Marcar el camino en el mapa
if camino:
    for paso in camino:
        if lista[paso[0]][paso[1]] == ".":
            lista[paso[0]][paso[1]] = "*"
else:
    print("No hay camino encontrado")

# Imprimir el mapa actualizado
for sublista in lista:
    print(' '.join(sublista))
