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
        self.mapa= [##el mapa no tiene un camino para llegar a la meta
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

class Agente():
    def __init__(self, entorno, estrategia):
        self.entorno = entorno
        self.estrategia = estrategia
        self.meta = self.entorno.get_estado_final() # Guardamos la meta para la heurística
        
        # Inicializamos con el h del estado inicial
        estado_inicial = self.entorno.get_estado_inicial()
        h_inicial = self._calcular_manhattan(estado_inicial)
        f_inicial = self.estrategia.calcular_f(0, h_inicial)
        self.frontera = [Nodo(estado_inicial, f=f_inicial, h=h_inicial)]
        
        self.explorados = set()
        self.recorrido = []
        self.cantidad_visitada = 0

    def _calcular_manhattan(self, estado_actual):
        """Calcula h(n) como |x1 - x2| + |y1 - y2|"""
        (x1, y1) = estado_actual
        (x2, y2) = self.meta
        return abs(x1 - x2) + abs(y1 - y2)

    def busqueda(self):
        while self.frontera:
            # en greedy saca el que tiene menor manhattan, en A* el de menor manhattan y menor costo acumulado
            nodo_actual = self.estrategia.extraer(self.frontera)
            
            if nodo_actual.estado == self.meta:
                return nodo_actual 
            
            if nodo_actual.estado not in self.explorados:
                self.explorados.add(nodo_actual.estado)
                self.recorrido.append(nodo_actual.estado)
                self.cantidad_visitada += 1
                self.entorno.marcar_paso(nodo_actual.estado)
                
                sucesores = self.entorno.get_sucesores(nodo_actual.estado)
                for estado_hijo in sucesores:
                    # g(n) es el costo real acumulado [1]
                    costo_hijo = nodo_actual.g + 1 
                    
                    # h(n) es la estimación heurística hasta la meta [2]
                    h_hijo = self._calcular_manhattan(estado_hijo)
                    
                    f_hijo = self.estrategia.calcular_f(costo_hijo, h_hijo)
                    nuevo_hijo = Nodo(
                        estado_hijo,
                        f=f_hijo,
                        padre=nodo_actual,
                        g=costo_hijo,
                        h=h_hijo
                    )
                    self.estrategia.agregar(self.frontera, nuevo_hijo)##agrega cada uno de los nodos sucesores a la frontera y les calcula el manhattan
        return None
    
    def get_recorridos(self):
        print("cantidad de pasos: "+ str(self.cantidad_visitada))
        print(self.recorrido)

    def imprimir_mapa(self):
        self.entorno.get_mapa()

    
class Nodo():
    def __init__(self, estado, f, padre=None, g=0, h=0):
        self.estado = estado
        self.padre = padre
        self.g = g  # Costo real acumulado
        self.h = h  # Estimación heurística
        self.f = f  # Evaluación según la estrategia

    def __lt__(self, otro):
        return self.f < otro.f


class EstrategiaGreedy:
    def calcular_f(self, _g, h):
        return h

    def extraer(self, frontera):
        return heapq.heappop(frontera)

    def agregar(self, frontera, nodo):
        heapq.heappush(frontera, nodo)


class EstrategiaAStar:
    def calcular_f(self, g, h):
        return g + h  # f(n) = g(n) + h(n)

    def extraer(self, frontera):
        return heapq.heappop(frontera)

    def agregar(self, frontera, nodo):
        heapq.heappush(frontera, nodo)


print("Greedy")
entorno1 = Entorno()
estrategia1 = EstrategiaGreedy()
agente1 = Agente(entorno1, estrategia1)
agente1.busqueda()
agente1.get_recorridos()
agente1.imprimir_mapa()

print("A*")
entorno2 = Entorno()
estrategia2 = EstrategiaAStar()
agente2 = Agente(entorno2, estrategia2)
agente2.busqueda()
agente2.get_recorridos()
agente2.imprimir_mapa()