import heapq ##permite implementar colas de prioridad, util para el UCS

class Entorno():
    def __init__(self):
        self.mapa= [
        "###########", #8filasx11cols
        "#S#     #G#",
        "# # ### # #",
        "# # #   # #",
        "#   # ### #",
        "### #     #",
        "#     #####",
        "###########",
        ]
        self.estado_inicial=self.get_estado_inicial()
    
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
    def __init__(self, estado, padre=None, accion=None, costo_acumulado=0, profundidad=0):
        self.estado = estado            # La tupla (fila, col)
        self.padre = padre              # El objeto Nodo anterior (no solo la coordenada)
        self.accion = accion            # La acción que se ejecutó para llegar aquí
        self.costo_acumulado = costo_acumulado # g(n): suma de costos desde el inicio
        self.profundidad = profundidad  # Nivel en el árbol
    
    def __lt__(self, otro):##le enseño al objeto que es lo que comparo de el cuando le aplico el operador <
        return self.costo_acumulado < otro.costo_acumulado ##me permite hacer nodo1<nodo2 y que se comparen los costos
    



class Agente():
    def __init__(self, entorno, estrategia):
        self.entorno = entorno
        self.estrategia = estrategia
        # Inicializamos la frontera con el nodo raíz
        self.frontera = [Nodo(self.entorno.get_estado_inicial())]
        self.explorados = set()##es un elemento de tipo conjunto, que es una coleccion de elementos unicos y no ordenados (si lo imprimo no me lo va a mostrar en orden!)
        self.recorrido = []
        self.cantidad_visitada = 0
    def busqueda(self):
        while self.frontera:
            # La estrategia decide qué nodo extraer
            nodo_actual = self.estrategia.extraer(self.frontera)
            
            # 1. Test Objetivo
            if nodo_actual.estado == self.entorno.get_estado_final():
                return nodo_actual # Aquí luego reconstruyes el camino
            
            # 2. Evitar estados repetidos
            if nodo_actual.estado not in self.explorados:
                self.explorados.add(nodo_actual.estado)
                self.recorrido.append(nodo_actual.estado)
                self.cantidad_visitada +=1
                self.entorno.marcar_paso(nodo_actual.estado)
                
                # 3. Expandir sucesores, sucesores tiene una lista de coordenadas y para cada hijo creo un nodo
                sucesores = self.entorno.get_sucesores(nodo_actual.estado)
                for estado_hijo in sucesores:
                    # g(n) del hijo = g(n) del padre + costo del paso (1 en este lab)
                    costo_hijo = nodo_actual.costo_acumulado + 1 
                    profundidad_hija = nodo_actual.profundidad + 1
                    
                    nuevo_hijo = Nodo(
                        estado_hijo, 
                        padre=nodo_actual, 
                        costo_acumulado=costo_hijo, 
                        profundidad=profundidad_hija
                    )
                    self.estrategia.agregar(self.frontera, nuevo_hijo)
        return None # No hay solución
    
    def get_recorridos(self):
        print("cantidad de pasos: "+ str(self.cantidad_visitada))
        print(self.recorrido)

    def imprimir_mapa(self):
        self.entorno.get_mapa()

class EstrategiaBFS:##busqueda en achura, expande primero los nodos menos profundos
    def extraer(self, frontera):
        # BFS usa FIFO (cola): saca el primero que entró
        return frontera.pop(0)
    
    def agregar(self, frontera, nodo):
        # BFS agrega al final
        frontera.append(nodo)

class EstrategiaDFS:##busqueda en profundidad, expande el recorrido hasta el ultimo nodo de la tira y luego regresa en caso de no haber llegado a la solucion y repite con el siguiente
    def extraer(self, frontera):
        # LIFO: saca el último nodo agregado a la lista
        return frontera.pop()
    
    def agregar(self, frontera, nodo):
        # Agrega el nodo al final de la lista
        frontera.append(nodo)

class EstrategiaUCS:
    def extraer(self, frontera):
        # Extrae el nodo con el costo acumulado g(n) más bajo
        return heapq.heappop(frontera)
    
    def agregar(self, frontera, nodo):
        # Inserta el nodo en la posición correcta según su costo
        heapq.heappush(frontera, nodo)
        


print("-----------BFS-----------")  

entorno= Entorno()        
estrategia= EstrategiaBFS()
agente= Agente(entorno,estrategia)
agente.imprimir_mapa()
agente.busqueda()
print("----------------------")
agente.imprimir_mapa()
agente.get_recorridos()

print("-----------DFS-----------")

entorno2= Entorno()        
estrategia2= EstrategiaDFS()## se puede observar que de casualidad realiza el recorrido mas optimo
agente2= Agente(entorno2,estrategia2)##pero esto esta influenciado por 1) el orden en el que se almacnan las posiciones en get_sucesores                                   
agente2.imprimir_mapa()## 2)el orden en que se agregan los nodos a la pila
agente2.busqueda()##termina avanzando siempre siguiendo este patron de prioridad : Derecha, luego Izquierda, luego Abajo, luego Arriba.
print("----------------------")##y justo con esa prioridad se llega de la manera mas optima al ojetivo
agente2.imprimir_mapa()
agente2.get_recorridos()


print("-----------UCS-----------")

entorno3= Entorno()##para esta caso el UCS y BFS dan  el mismo camino       
estrategia3= EstrategiaUCS()##ya que no hay costos variables entre pasos de un nodo a otro 
agente3= Agente(entorno3,estrategia3)
agente3.imprimir_mapa()
agente3.busqueda()
print("----------------------")
agente3.imprimir_mapa()
agente3.get_recorridos()