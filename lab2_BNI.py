class Entorno:
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
    
    def get_estado_inicial(self):
        for i in range(len(self.mapa)):
            for j in range(len(self.mapa[i])):
                if self.mapa[i][j] == 'S':
                    return (i, j)

    def get_estado_final(self):
        for i in range(len(self.mapa)):
            for j in range(len(self.mapa[i])):
                if self.mapa[i][j] == 'G':
                    return (i, j)

    def es_posicion_valida(self, posicion):
        fila, col = posicion
        if fila < 0 or fila >= len(self.mapa):
            return False
        if col < 0 or col >= len(self.mapa[fila]):
            return False
        return self.mapa[fila][col] != '#'

class Agente:
    pass
