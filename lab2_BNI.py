class Entorno():
    def __init__(self):
        self.mapa= [
        "###########",
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
        self.explorados = set()##es un elemento de tipo conjunto, que es una coleccion de elementos unicos y no ordenados
        while self.frontera:
            # La estrategia decide qué nodo extraer
            nodo_actual = self.estrategia.extraer(self.frontera)
            
            # 1. Test Objetivo
            if nodo_actual.estado == self.entorno.get_estado_final():
                return nodo_actual # Aquí luego reconstruyes el camino
            
            # 2. Evitar estados repetidos
            if nodo_actual.estado not in self.explorados:
                self.explorados.add(nodo_actual.estado)
                
                # 3. Expandir sucesores, sucesores tiene una lista de coordenadas y para cada hijo creo un nodo
                sucesores = self.entorno.get_sucesores(nodo_actual.estado)
                for estado_hijo in sucesores:
                    # Crear nuevo objeto Nodo y añadir a la frontera
                    nuevo_hijo = Nodo(estado_hijo, padre=nodo_actual)
                    self.estrategia.agregar(self.frontera, nuevo_hijo)
        return None # No hay solución

class EstrategiaBFS:##busqueda en achura, expande primero los nodos menos profundos
    def extraer(self, frontera):
        # BFS usa FIFO (cola): saca el primero que entró [5]
        return frontera.pop(0)
    
    def agregar(self, frontera, nodo):
        # BFS agrega al final [5]
        frontera.append(nodo)
        
        
        
