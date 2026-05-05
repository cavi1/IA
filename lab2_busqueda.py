# -*- coding: utf-8 -*-
"""
LAB 2 - AGENTES DE BUSQUEDA - INTELIGENCIA ARTIFICIAL 2026
===========================================================
Parte 1: Busqueda No Informada  -> BFS, DFS, UCS
Parte 2: Busqueda Informada     -> Greedy, A*
Parte 3: Busqueda Local         -> Hill Climbing, Simulated Annealing (Sudoku)
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import heapq
import math
import random
import time
from collections import deque

# -------------------------------------------------------------
#  LABERINTOS
# -------------------------------------------------------------

# Laberinto 1 - búsqueda no informada  (8 filas x 11 cols)
# S=(1,1)  G=(1,9)
MAZE1 = [
    "###########",
    "#S#     #G#",
    "# # ### # #",
    "# # #   # #",
    "#   # ### #",
    "### #     #",
    "#     #####",
    "###########",
]

# Laberinto 2 - búsqueda informada  (7 filas x 15 cols)
# S=(1,1)  G=(5,13)
MAZE2 = [
    "###############",
    "#S    #   #   #",
    "# ##### # ### #",
    "#     # # #   #",
    "### # # # #   #",
    "#   #   #   #G#",
    "###############",
]

# -------------------------------------------------------------
#  UTILIDADES PARA LABERINTOS
# -------------------------------------------------------------

def parse_maze(maze):
    start = goal = None
    for r, row in enumerate(maze):
        for c, ch in enumerate(row):
            if ch == 'S':
                start = (r, c)
            elif ch == 'G':
                goal = (r, c)
    return start, goal


def neighbors(maze, pos):
    r, c = pos
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]) and maze[nr][nc] != '#':
            yield (nr, nc)


def print_maze_path(maze, path, title=""):
    grid = [list(row) for row in maze]
    for r, c in path:
        if grid[r][c] not in ('S', 'G'):
            grid[r][c] = '*'
    print(f"\n{'-'*40}")
    print(f"  {title}")
    print(f"{'-'*40}")
    for row in grid:
        print('  ' + ''.join(row))


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# -------------------------------------------------------------
#  PARTE 1 - BÚSQUEDA NO INFORMADA
# -------------------------------------------------------------

def bfs(maze, start, goal):
    """Breadth-First Search - completo y óptimo (costo uniforme)."""
    queue = deque([(start, [start])])
    visited = {start}
    expanded = 0
    while queue:
        node, path = queue.popleft()
        expanded += 1
        if node == goal:
            return path, expanded
        for nb in neighbors(maze, node):
            if nb not in visited:
                visited.add(nb)
                queue.append((nb, path + [nb]))
    return None, expanded


def dfs(maze, start, goal):
    """Depth-First Search - no garantiza optimalidad."""
    stack = [(start, [start])]
    visited = set()
    expanded = 0
    while stack:
        node, path = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        expanded += 1
        if node == goal:
            return path, expanded
        for nb in neighbors(maze, node):
            if nb not in visited:
                stack.append((nb, path + [nb]))
    return None, expanded


def ucs(maze, start, goal):
    """Uniform Cost Search - óptimo, usa cola de prioridad por costo."""
    pq = [(0, start, [start])]
    visited = set()
    expanded = 0
    while pq:
        cost, node, path = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        expanded += 1
        if node == goal:
            return path, expanded, cost
        for nb in neighbors(maze, node):
            if nb not in visited:
                heapq.heappush(pq, (cost + 1, nb, path + [nb]))
    return None, expanded, float('inf')


def run_uninformed(maze, label="Laberinto 1"):
    start, goal = parse_maze(maze)
    print(f"\n{'='*55}")
    print(f"  PARTE 1 - BÚSQUEDA NO INFORMADA  |  {label}")
    print(f"  Estado inicial: {start}   Estado objetivo: {goal}")
    print(f"{'='*55}")

    path_bfs, exp_bfs = bfs(maze, start, goal)
    path_dfs, exp_dfs = dfs(maze, start, goal)
    path_ucs, exp_ucs, cost_ucs = ucs(maze, start, goal)

    for tag, path, exp in [("BFS", path_bfs, exp_bfs),
                            ("DFS", path_dfs, exp_dfs),
                            ("UCS", path_ucs, exp_ucs)]:
        print(f"\n[{tag}]")
        print(f"  Nodos expandidos : {exp}")
        print(f"  Longitud camino  : {len(path) - 1} pasos")
        print(f"  Camino           : {path}")
        print_maze_path(maze, path, tag)

    print(f"\n{'-'*45}")
    print(f"  {'Algoritmo':<10}  {'Nodos exp.':<14}  {'Pasos'}")
    print(f"  {'-'*40}")
    print(f"  {'BFS':<10}  {exp_bfs:<14}  {len(path_bfs)-1}")
    print(f"  {'DFS':<10}  {exp_dfs:<14}  {len(path_dfs)-1}")
    print(f"  {'UCS':<10}  {exp_ucs:<14}  {len(path_ucs)-1}")

    print("""
  ANÁLISIS DE COMPLEJIDAD (b=factor ramificación, d=profundidad solución, m=profundidad máxima):
  +----------+-----------------+----------------+----------+-------------+
  | Algo.    | Tiempo          | Espacio        | Completo | Óptimo      |
  +----------+-----------------+----------------+----------+-------------+
  | BFS      | O(b^d)          | O(b^d)         | Sí       | Sí (c=1)    |
  | DFS      | O(b^m)          | O(b·m)         | No       | No          |
  | UCS      | O(b^(C*/ε))     | O(b^(C*/ε))    | Sí       | Sí          |
  +----------+-----------------+----------------+----------+-------------+

  CONCLUSIÓN:
  * BFS: garantiza camino más corto en grafos con costo uniforme. Usa mucha memoria.
  * DFS: eficiente en memoria O(b·m), pero puede perderse en ramas largas sin solución.
  * UCS: óptimo para cualquier costo de paso; en laberinto (todos costo=1) = BFS.
  -> Para este laberinto se recomienda BFS o UCS por garantizar optimalidad.
""")


# -------------------------------------------------------------
#  PARTE 2 - BÚSQUEDA INFORMADA
# -------------------------------------------------------------

def greedy(maze, start, goal):
    """Greedy Best-First - elige siempre el nodo con menor h(n)."""
    pq = [(manhattan(start, goal), start, [start])]
    visited = set()
    expanded = 0
    while pq:
        h, node, path = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        expanded += 1
        if node == goal:
            return path, expanded
        for nb in neighbors(maze, node):
            if nb not in visited:
                heapq.heappush(pq, (manhattan(nb, goal), nb, path + [nb]))
    return None, expanded


def astar(maze, start, goal):
    """A* - f(n) = g(n) + h(n), óptimo con heurística admisible."""
    g_cost = {start: 0}
    pq = [(manhattan(start, goal), 0, start, [start])]
    visited = set()
    expanded = 0
    while pq:
        f, g, node, path = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        expanded += 1
        if node == goal:
            return path, expanded, g
        for nb in neighbors(maze, node):
            if nb not in visited:
                ng = g + 1
                if nb not in g_cost or ng < g_cost[nb]:
                    g_cost[nb] = ng
                    heapq.heappush(pq, (ng + manhattan(nb, goal), ng, nb, path + [nb]))
    return None, expanded, float('inf')


def run_informed(maze, label="Laberinto 2"):
    start, goal = parse_maze(maze)
    print(f"\n{'='*55}")
    print(f"  PARTE 2 - BÚSQUEDA INFORMADA  |  {label}")
    print(f"  Estado inicial: {start}   Estado objetivo: {goal}")
    print(f"{'='*55}")

    # Cálculo manual de h(n)
    nbs_start = list(neighbors(maze, start))
    print(f"\n  Heurística Manhattan h(n) = |Δfila| + |Δcol|")
    print(f"  h({start}) = {manhattan(start, goal)}  -> estado inicial")
    for nb in nbs_start[:3]:
        print(f"  h({nb}) = {manhattan(nb, goal)}")

    print("""
  a) Admisibilidad: h(n) es admisible si NUNCA sobreestima el costo real al objetivo.
     Garantiza que A* encuentre siempre el camino óptimo.

  b) Manhattan es admisible porque en un laberinto el costo real entre dos celdas
     es siempre ≥ distancia Manhattan (no se puede ir en diagonal ni atravesar paredes).
     Por tanto h(n) ≤ costo_real(n, meta).
""")

    # Greedy paso a paso
    path_g, exp_g = greedy(maze, start, goal)
    print(f"\n[Greedy Best-First]")
    print(f"  Nodos expandidos : {exp_g}")
    print(f"  Longitud camino  : {len(path_g) - 1} pasos")
    print(f"  Camino           : {path_g}")
    print_maze_path(maze, path_g, "GREEDY")

    # A* con tabla g/h/f
    path_a, exp_a, cost_a = astar(maze, start, goal)
    print(f"\n[A*]")
    print(f"  Nodos expandidos : {exp_a}")
    print(f"  Costo óptimo g*  : {cost_a}")
    print(f"  Longitud camino  : {len(path_a) - 1} pasos")
    print(f"  Camino           : {path_a}")
    print_maze_path(maze, path_a, "A*")

    # Tabla g/h/f de los primeros nodos expandidos por A*
    print(f"\n  Primeros nodos expandidos por A* (g, h, f):")
    g_cost = {start: 0}
    pq2 = [(manhattan(start, goal), 0, start)]
    vis2 = set()
    shown = 0
    while pq2 and shown < 8:
        f, g, node = heapq.heappop(pq2)
        if node in vis2:
            continue
        vis2.add(node)
        h = manhattan(node, goal)
        print(f"    nodo={node}  g={g}  h={h}  f={f}")
        shown += 1
        for nb in neighbors(maze, node):
            if nb not in vis2:
                ng = g + 1
                if nb not in g_cost or ng < g_cost[nb]:
                    g_cost[nb] = ng
                    heapq.heappush(pq2, (ng + manhattan(nb, goal), ng, nb))

    print(f"\n{'-'*45}")
    print(f"  {'Algoritmo':<12}  {'Nodos exp.':<14}  {'Pasos'}")
    print(f"  {'-'*40}")
    print(f"  {'Greedy':<12}  {exp_g:<14}  {len(path_g)-1}")
    print(f"  {'A*':<12}  {exp_a:<14}  {len(path_a)-1}")

    print("""
  CONCLUSIÓN:
  * Greedy expande menos nodos pero NO garantiza camino óptimo (puede retroceder).
  * A* garantiza optimalidad con h admisible y generalmente es más eficiente que BFS/UCS.
  -> Para este laberinto se recomienda A* por su balance óptimo entre eficiencia y calidad.
""")


# -------------------------------------------------------------
#  PARTE 3 - BÚSQUEDA LOCAL: SUDOKU
# -------------------------------------------------------------

# Sudoku 4x4 inicial  (0 = vacío)
SUDOKU_4x4 = [
    [1, 0, 0, 0],
    [0, 0, 0, 4],
    [0, 0, 3, 0],
    [2, 0, 0, 0],
]

# Sudoku 9x9 clásico de ejemplo
SUDOKU_9x9 = [
    [5, 3, 0,  0, 7, 0,  0, 0, 0],
    [6, 0, 0,  1, 9, 5,  0, 0, 0],
    [0, 9, 8,  0, 0, 0,  0, 6, 0],
    [8, 0, 0,  0, 6, 0,  0, 0, 3],
    [4, 0, 0,  8, 0, 3,  0, 0, 1],
    [7, 0, 0,  0, 2, 0,  0, 0, 6],
    [0, 6, 0,  0, 0, 0,  2, 8, 0],
    [0, 0, 0,  4, 1, 9,  0, 0, 5],
    [0, 0, 0,  0, 8, 0,  0, 7, 9],
]


def make_fixed(grid):
    return [[v != 0 for v in row] for row in grid]


def fill_rows_randomly(grid, fixed, n):
    """Inicializa: cada fila contiene exactamente 1..n (sin repetir), respetando fijos."""
    state = [row[:] for row in grid]
    for r in range(n):
        used = {state[r][c] for c in range(n) if fixed[r][c]}
        missing = list(set(range(1, n + 1)) - used)
        random.shuffle(missing)
        idx = 0
        for c in range(n):
            if not fixed[r][c]:
                state[r][c] = missing[idx]
                idx += 1
    return state


def count_conflicts(state, n):
    """
    Función objetivo h = conflictos en columnas + conflictos en bloques.
    Objetivo: h = 0  (ningún número repetido).
    Las filas NO se cuentan porque fill_rows_randomly las garantiza sin conflicto.
    """
    sqrt_n = int(math.sqrt(n))
    conflicts = 0
    for c in range(n):
        col = [state[r][c] for r in range(n)]
        conflicts += n - len(set(col))
    for br in range(sqrt_n):
        for bc in range(sqrt_n):
            block = [
                state[br * sqrt_n + i][bc * sqrt_n + j]
                for i in range(sqrt_n)
                for j in range(sqrt_n)
            ]
            conflicts += n - len(set(block))
    return conflicts


def random_swap(state, fixed, n):
    """Genera un vecino intercambiando dos celdas no-fijas en una fila aleatoria."""
    attempts = 0
    while attempts < 100:
        r = random.randint(0, n - 1)
        free = [c for c in range(n) if not fixed[r][c]]
        if len(free) >= 2:
            c1, c2 = random.sample(free, 2)
            nb = [row[:] for row in state]
            nb[r][c1], nb[r][c2] = nb[r][c2], nb[r][c1]
            return nb
        attempts += 1
    return state


def best_neighbor(state, fixed, n):
    """Retorna el mejor vecino (menor h) explorando todos los swaps posibles."""
    best = None
    best_h = count_conflicts(state, n)
    for r in range(n):
        free = [c for c in range(n) if not fixed[r][c]]
        for i in range(len(free)):
            for j in range(i + 1, len(free)):
                nb = [row[:] for row in state]
                nb[r][free[i]], nb[r][free[j]] = nb[r][free[j]], nb[r][free[i]]
                h = count_conflicts(nb, n)
                if h < best_h:
                    best_h = h
                    best = nb
    return best, best_h


def hill_climbing(grid, fixed, n, max_restarts=100):
    """Hill Climbing con reinicios aleatorios."""
    overall_best_state = None
    overall_best_h = n * n * 2
    total_steps = 0
    reached_restarts = 0

    for restart in range(max_restarts):
        state = fill_rows_randomly(grid, fixed, n)
        h = count_conflicts(state, n)
        steps = 0

        while True:
            if h == 0:
                return state, 0, total_steps + steps, restart + 1
            nb, nb_h = best_neighbor(state, fixed, n)
            if nb is None or nb_h >= h:
                break  # mínimo local
            state = nb
            h = nb_h
            steps += 1

        total_steps += steps
        reached_restarts += 1
        if h < overall_best_h:
            overall_best_h = h
            overall_best_state = [row[:] for row in state]

    return overall_best_state, overall_best_h, total_steps, reached_restarts


def simulated_annealing(grid, fixed, n,
                        T_init=2.0, cooling=0.9995, max_iter=100_000):
    """Simulated Annealing - acepta soluciones peores con probabilidad e^(-Δh/T)."""
    state = fill_rows_randomly(grid, fixed, n)
    h = count_conflicts(state, n)
    best_state = [row[:] for row in state]
    best_h = h
    T = T_init
    accepted = 0

    for it in range(max_iter):
        if h == 0:
            break
        T *= cooling
        if T < 1e-8:
            break

        nb = random_swap(state, fixed, n)
        nb_h = count_conflicts(nb, n)
        delta = nb_h - h

        if delta < 0 or random.random() < math.exp(-delta / T):
            state = nb
            h = nb_h
            accepted += 1

        if h < best_h:
            best_h = h
            best_state = [row[:] for row in state]

    return best_state, best_h, accepted


def print_sudoku(grid, n, title=""):
    sqrt_n = int(math.sqrt(n))
    sep = "  +" + ("-" * (sqrt_n * 2 + 1) + "+") * sqrt_n
    print(f"\n  {title}")
    for r in range(n):
        if r % sqrt_n == 0:
            print(sep)
        row_str = "  |"
        for c in range(n):
            val = grid[r][c]
            row_str += f" {'.' if val == 0 else val}"
            if (c + 1) % sqrt_n == 0:
                row_str += " |"
        print(row_str)
    print(sep)


def run_sudoku(grid, n, label="4x4"):
    fixed = make_fixed(grid)
    print(f"\n{'='*55}")
    print(f"  PARTE 3 - BÚSQUEDA LOCAL  |  Sudoku {label}")
    print(f"{'='*55}")
    print_sudoku(grid, n, "Estado inicial")

    print(f"""
  MODELADO COMO OPTIMIZACIÓN:
  * Espacio de estados  : todas las formas de completar las celdas vacías
                         manteniendo 1..{n} exactamente una vez por fila.
  * Función objetivo    : h = conflictos en columnas + conflictos en bloques
  * Operadores          : intercambiar dos celdas no-fijas en la misma fila
  * Objetivo            : h = 0
""")

    # -- Hill Climbing --
    print("-" * 45)
    print("  Hill Climbing (max 100 reinicios):")
    t0 = time.time()
    hc_state, hc_h, hc_steps, hc_restarts = hill_climbing(grid, fixed, n)
    hc_time = time.time() - t0
    print(f"  h final = {hc_h}  |  Pasos totales = {hc_steps}"
          f"  |  Reinicios = {hc_restarts}  |  {hc_time:.3f} s")
    print_sudoku(hc_state, n, f"HC - h={hc_h}")

    if hc_h > 0:
        print(f"  [!] HC quedó atrapado en mínimo local (h={hc_h} > 0).")

    # -- Simulated Annealing -- (3 corridas para comparar variabilidad)
    print("\n-" * 23)
    print("  Simulated Annealing (3 corridas):")
    sa_results = []
    for run in range(3):
        t0 = time.time()
        sa_state, sa_h, sa_steps = simulated_annealing(grid, fixed, n)
        sa_time = time.time() - t0
        sa_results.append((sa_h, sa_steps, sa_time))
        print(f"  Corrida {run+1}: h={sa_h}  |  Pasos={sa_steps}  |  {sa_time:.3f} s")
    print_sudoku(sa_state, n, f"SA (última corrida) - h={sa_h}")

    # -- Comparación --
    best_sa_h = min(r[0] for r in sa_results)
    avg_sa_steps = sum(r[1] for r in sa_results) // 3
    print(f"\n  COMPARACIÓN:")
    print(f"  {'Algoritmo':<24} {'h final':<10} {'Pasos (aprox)'}")
    print(f"  {'-'*45}")
    print(f"  {'Hill Climbing':<24} {hc_h:<10} {hc_steps}")
    print(f"  {'Simulated Annealing':<24} {best_sa_h:<10} {avg_sa_steps}")
    print(f"""
  ANÁLISIS:
  * Hill Climbing puede quedarse en mínimos locales sin escapar.
    Con reinicios aumenta la probabilidad de encontrar el óptimo global.
  * SA acepta movimientos empeorativos con probabilidad e^(-Δh/T):
    - Alta temperatura inicial -> exploración amplia.
    - Enfriamiento gradual -> explotación del mejor vecindario.
  * SA generalmente encuentra h=0 con mayor frecuencia en Sudoku
    porque puede saltar barreras de mínimos locales.
  * Parámetros críticos de SA: T_init, cooling_rate, max_iter.
    Un cooling muy rápido -> SA ≈ HC. Muy lento -> convergencia lenta.
""")


# -------------------------------------------------------------
#  MAIN
# -------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 55)
    print("  LAB 2 - INTELIGENCIA ARTIFICIAL 2026")
    print("  Búsqueda No Informada | Informada | Local")
    print("=" * 55)

    run_uninformed(MAZE1, "Laberinto 1")
    run_informed(MAZE2, "Laberinto 2")
    run_sudoku(SUDOKU_4x4, 4, "4x4")
    run_sudoku(SUDOKU_9x9, 9, "9x9")

    print("\n" + "=" * 55)
    print("  FIN DEL LABORATORIO")
    print("=" * 55)
