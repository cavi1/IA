import pandas as pd
import random
import math

class Nodo: ##va a contener la configuración actual del tablero
    def __init__(self, estado, h=0): ##en bk solo es importante el estado actual
        self.estado = estado  # La grilla 4x4 (matriz o lista)
        self.h = h            # Cantidad de conflictos (función objetivo)

    def __lt__(self, otro):
        # Para Hill Climbing, queremos el que tenga MENOS conflictos
        return self.h < otro.h
    

class EntornoSudoku:
    def __init__(self, tablero_inicial):
        self.fijos = tablero_inicial # Posiciones que no se pueden cambiar [4]

    def calcular_conflictos(self, estado):
        """Implementa h(estado) = repeticiones en columnas + bloques [5]"""
        conflictos = 0
        # 1. Contar repeticiones en cada columna
        # 2. Contar repeticiones en cada bloque de 2x2
        # El objetivo es que h(estado) == 0 [5]
        return conflictos

    def generar_vecino(self, estado):
        """Genera un vecino modificando una celda no fija [1]"""
        nuevo_estado = [fila[:] for fila in estado]
        # Elegir una posición aleatoria que no sea fija y cambiar su valor
        # o intercambiar dos valores en una fila
        return nuevo_estado

class AgenteLocal:
    def __init__(self, entorno):
        self.entorno = entorno

    def hill_climbing(self, estado_inicial):
        """Algoritmo de ascenso de colinas (en este caso, descenso de conflictos) [3, 6]"""
        actual = Nodo(estado_inicial, self.entorno.calcular_conflictos(estado_inicial))
        pasos = 0
        
        while True:
            # 1. Generar el mejor vecino
            vecino_estado = self.entorno.generar_vecino(actual.estado)
            h_vecino = self.entorno.calcular_conflictos(vecino_estado)
            
            # 2. Si el vecino no mejora (o no es igual en caso de terrazas), terminar [6, 7]
            if h_vecino >= actual.h:
                return actual.estado, pasos
            
            actual = Nodo(vecino_estado, h_vecino)
            pasos += 1

    def simulated_annealing(self, estado_inicial, T=100.0, alpha=0.95):
        """Temple Simulado para escapar de óptimos locales [3, 7]"""
        actual = Nodo(estado_inicial, self.entorno.calcular_conflictos(estado_inicial))
        pasos = 0
        
        while T > 0.01:
            # 1. Elegir un vecino al azar [7]
            proximo_estado = self.entorno.generar_vecino(actual.estado)
            h_proximo = self.entorno.calcular_conflictos(proximo_estado)
            
            delta_e = actual.h - h_proximo # Diferencia de energía
            
            # 2. Si es mejor, aceptarlo. Si es peor, aceptarlo con Probabilidad de Boltzmann [7]
            if delta_e > 0 or random.random() < math.exp(delta_e / T):
                actual = Nodo(proximo_estado, h_proximo)
            
            T *= alpha # Factor de enfriamiento [7]
            pasos += 1
            
            if actual.h == 0: break # Éxito total
            
        return actual.estado, pasos

resultados = []
ejecuciones = 50 # Número de veces para obtener una muestra estadística [5]
agente=AgenteLocal()
entorno=EntornoSudoku()

for i in range(ejecuciones):
    # 1. Ejecutar Hill Climbing
    estado_final_hc, pasos_hc = agente.hill_climbing(sudoku_inicial)
    h_hc = entorno.calcular_conflictos(estado_final_hc)
    resultados.append({'Algoritmo': 'HC', 'Conflictos': h_hc, 'Pasos': pasos_hc})
    
    # 2. Ejecutar Simulated Annealing
    estado_final_sa, pasos_sa = agente.simulated_annealing(sudoku_inicial)
    h_sa = entorno.calcular_conflictos(estado_final_sa)
    resultados.append({'Algoritmo': 'SA', 'Conflictos': h_sa, 'Pasos': pasos_sa})

# Crear DataFrame para el análisis [4]
df = pd.DataFrame(resultados)