##calculo distancia de manhattan
##Estado Inicial (S): (1, 1)
##Estado Objetivo (G): (5, 13)
## h(n)=∣x1 −x2∣ + ∣y1 − y2∣
## h(S)=∣1−5∣+∣1−13∣=∣−4∣+∣−12∣=4+12=16
## Vecino Derecha (1, 2): h(1, 2)=∣1−5∣+∣2−13∣=4+11=15
## Vecino de Abajo (2, 1): h(2, 1)=∣2−5∣+∣1−13∣=3+12=15
## No tiene mas vecinos adyacentes
import heapq

class Entorno():
    def __init__(self):
        self.mapa= [
        "###############",
        "#S      #     #",
        "# ##### # ### #",
        "#     # # #   #",
        "### # # # # ###",
        "#   #   #   #G#",
        "###############"
        ]

    def get_estado_inicial(self): ##devuelve donde se encuentra S
        for i in range(len(self.mapa)):
            for j in range(len(self.mapa[i])):
                if self.mapa[i][j] == 'S':
                    return (i, j)

    def get_estado_final(self): ##devuelve donde se encuentra G
        for i in range(len(self.mapa)):
            for j in range(len(self.mapa[i])):
                if self.mapa[i][j] == 'G':
                    return (i, j)

    def es_posicion_valida(self, posicion): ##devuelve si una posición es válida para estar
        fila, col = posicion
        if fila < 0 or fila >= len(self.mapa):
            return False
        if col < 0 or col >= len(self.mapa[fila]):
            return False
        return self.mapa[fila][col] != '#'
    
    def get_sucesores(self, posicion):
        fila, col = posicion
        candidatos = [
            (fila - 1, col), # Arriba
            (fila + 1, col), # Abajo
            (fila, col - 1), # Izquierda
            (fila, col + 1)  # Derecha
        ]
        #Retornar solo las posiciones que son validas segun el metodo de posicion valida
        return [p for p in candidatos if self.es_posicion_valida(p)]
    
    def marcar_paso(self, posicion):
        fila, col = posicion
        if self.mapa[fila][col] in ('S', 'G'):
            return
        fila_lista = list(self.mapa[fila])
        fila_lista[col] = "."
        self.mapa[fila] = "".join(fila_lista)

    def get_mapa(self):
        for fila in self.mapa:
            print(fila)

    
class Nodo():
    def __init__(self, estado, padre=None, g=0, h=0):
        self.estado = estado
        self.padre = padre
        self.g = g  # Costo acumulado
        self.h = h  # Estimación heurística
        self.f = g + h # Valor total para A*

    def __lt__(self, otro):
        return self.f < otro.f


class EstrategiaGreedy:
    def extraer(self, frontera):
        # Extrae el nodo con el costo acumulado g(n) más bajo
        return heapq.heappop(frontera)
    
    def agregar(self, frontera, nodo):
        # Inserta el nodo en la posición correcta según su costo
        heapq.heappush(frontera, nodo)