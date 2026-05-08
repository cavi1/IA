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
        self.fijos = tablero_inicial # Posiciones que no se pueden cambiar (0 = vacío)

    def generar_estado_inicial(self):
        """Rellena las celdas vacías (0) con valores aleatorios del 1 al 4"""
        n = len(self.fijos)
        estado = [fila[:] for fila in self.fijos]
        for i in range(n):
            for j in range(n):
                if estado[i][j] == 0:
                    estado[i][j] = random.randint(1, n)
        return estado

    def calcular_conflictos(self, estado):
        """Implementa h(estado) = repeticiones en columnas + bloques"""
        conflictos = 0
        n = len(estado)

        # 1. Contar repeticiones en cada columna
        for col in range(n):
            columna = [estado[fila][col] for fila in range(n)]
            conflictos += n - len(set(columna))

        # 2. Contar repeticiones en cada bloque de 2x2
        for bi in range(0, n, 2):
            for bj in range(0, n, 2):
                bloque = [estado[bi+di][bj+dj] for di in range(2) for dj in range(2)]
                conflictos += 4 - len(set(bloque))

        # El objetivo es que h(estado) == 0
        return conflictos

    def generar_vecino(self, estado):
        """Genera un vecino modificando una celda no fija al azar"""
        nuevo_estado = [fila[:] for fila in estado]
        n = len(estado)

        # Posiciones que no son fijas (el tablero original tenía un 0 ahí)
        no_fijas = [(i, j) for i in range(n) for j in range(n) if self.fijos[i][j] == 0]
        if not no_fijas:
            return nuevo_estado

        fi, fj = random.choice(no_fijas)
        valor_actual = nuevo_estado[fi][fj]
        opciones = [v for v in range(1, n + 1) if v != valor_actual]
        nuevo_estado[fi][fj] = random.choice(opciones)
        return nuevo_estado

    def imprimir_tablero(self, estado):
        for fila in estado:
            print(fila)


class AgenteLocal:
    def __init__(self, entorno):
        self.entorno = entorno

    def hill_climbing(self, estado_inicial):
        """Algoritmo de ascenso de colinas (en este caso, descenso de conflictos)"""
        actual = Nodo(estado_inicial, self.entorno.calcular_conflictos(estado_inicial))
        pasos = 0

        while True:
            # 1. Generar el mejor vecino
            vecino_estado = self.entorno.generar_vecino(actual.estado)
            h_vecino = self.entorno.calcular_conflictos(vecino_estado)

            # 2. Si el vecino no mejora (o no es igual en caso de terrazas), terminar
            if h_vecino >= actual.h:
                return actual.estado, pasos

            actual = Nodo(vecino_estado, h_vecino)
            pasos += 1

    def simulated_annealing(self, estado_inicial, T=100.0, alpha=0.95):
        """Temple Simulado para escapar de óptimos locales"""
        actual = Nodo(estado_inicial, self.entorno.calcular_conflictos(estado_inicial))
        pasos = 0

        while T > 0.01:
            # 1. Elegir un vecino al azar
            proximo_estado = self.entorno.generar_vecino(actual.estado)
            h_proximo = self.entorno.calcular_conflictos(proximo_estado)

            delta_e = actual.h - h_proximo # Diferencia de energía (positivo = mejora)

            # 2. Si es mejor, aceptarlo. Si es peor, aceptarlo con Probabilidad de Boltzmann
            if delta_e > 0 or random.random() < math.exp(delta_e / T):
                actual = Nodo(proximo_estado, h_proximo)

            T *= alpha # Factor de enfriamiento
            pasos += 1

            if actual.h == 0: break # Éxito total

        return actual.estado, pasos


# Sudoku 4x4: 0 = celda vacía (no fija), resto = valores fijos
tablero_fijo = [
    [0, 4, 0, 2],
    [2, 0, 0, 3],
    [0, 3, 0, 4],
    [4, 0, 3, 0]
]

entorno = EntornoSudoku(tablero_fijo)
agente = AgenteLocal(entorno)

resultados = []
ejecuciones = 50

for i in range(ejecuciones):
    sudoku_inicial = entorno.generar_estado_inicial()

    # 1. Ejecutar Hill Climbing
    estado_final_hc, pasos_hc = agente.hill_climbing(sudoku_inicial)
    h_hc = entorno.calcular_conflictos(estado_final_hc)
    resultados.append({'Algoritmo': 'HC', 'Conflictos': h_hc, 'Pasos': pasos_hc})

    # 2. Ejecutar Simulated Annealing (mismo punto de partida)
    estado_final_sa, pasos_sa = agente.simulated_annealing(sudoku_inicial)
    h_sa = entorno.calcular_conflictos(estado_final_sa)
    resultados.append({'Algoritmo': 'SA', 'Conflictos': h_sa, 'Pasos': pasos_sa})

# Crear DataFrame para el análisis
df = pd.DataFrame(resultados)

print("=== Resumen estadístico ===")
print(df.groupby('Algoritmo').agg(
    Conflictos_promedio=('Conflictos', 'mean'),
    Conflictos_minimos=('Conflictos', 'min'),
    Veces_solucion=('Conflictos', lambda x: (x == 0).sum()),
    Pasos_promedio=('Pasos', 'mean')
))

print("\n=== Ejemplo de solución (SA) ===")
entorno.imprimir_tablero(estado_final_sa)
print(f"Conflictos finales: {h_sa}")
