#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
seiscuartos.py.py
------------

"""

import entornos_o
from random import choice

__author__ = 'CAVI'

        
class SeisCuartos(entornos_o.Entorno):
    """
    Clase para un entorno de seis cuartos.
    
    Disposición de los cuartos: 
                                        |D| |E| |F| --cuartos de arriba--
                                        -----------    
                                        |A| |B| |C| --cuartos de abajo-- 
                                        
    Estan identificados por las siglas 
    EII=extremo inferior izquierdo
    MI=medio inferior
    EID=extremo inferior derecho
    ESI=extemo superior izquierdo
    MSPB=medio superior puede bajar
    ESD=extremo  superior derecho
    

    El estado se define como (robot, A, B, C, D, E, F)
    donde robot puede tener los valores "A", "B", "C", "D", "E", "F"
    A, B, C, D, E, F pueden tener los valores "limpio", "sucio"

    La acción de `"subir"` solo es legal en el piso de abajo, en los cuartos de los extremos,
    mientras que la acción de `"bajar"` solo es legal en el piso de arriba y en el cuarto del
    centro (dos escaleras para subir, una escalera para bajar).

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza
    """
    
    def __init__(self, x0=["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]):
        """
        Por default inicialmente el robot está en A y los seis cuartos
        están sucios

        """
        self.x = x0[:]
        self.desempeño = 0
        self.disposicion = {"A":"EII","B":"MI","C":"EID","D":"ESI","E":"MSPB","F":"ESD"}
        
    
    
    def acción_legal(self, acción):
        return acción in ("ir_derecha", "ir_izquierda", "subir", "bajar", "limpiar", "nada")
    
    def puede_hacer(self,cuarto_actual,accion):
        if self.disposicion[cuarto_actual]=="EII":
            return accion in ("ir_derecha", "subir", "limpiar", "nada")
        elif self.disposicion[cuarto_actual]=="MI":
            return accion in ("ir_derecha","ir_izquierda", "limpiar", "nada")
        elif self.disposicion[cuarto_actual]=="EID":
            return accion in ("ir_izquierda","subir", "limpiar", "nada")
        elif self.disposicion[cuarto_actual]=="ESI":
            return accion in ("ir_derecha","limpiar", "nada")
        elif self.disposicion[cuarto_actual]=="MSPB":
            return accion in ("ir_derecha","ir_izquierda","bajar","limpiar","nada")
        elif self.disposicion[cuarto_actual]=="ESD":
            return accion in ("ir_izquierda","limpiar","nada")
        
    def definir_destino(self, cuarto_actual, accion):
        """
        Dada una acción y el cuarto actual, devuelve el cuarto destino.
        """
        match accion:
            case "ir_derecha":
                match cuarto_actual:
                    case "A": return "B"
                    case "B": return "C"
                    case "D": return "E"
                    case "E": return "F"
                    case _: return cuarto_actual
                    
            case "ir_izquierda":
                match cuarto_actual:
                    case "B": return "A"
                    case "C": return "B"
                    case "E": return "D"
                    case "F": return "E"
                    case _: return cuarto_actual
                    
            case "subir":
                match cuarto_actual:
                    case "A": return "D"
                    case "C": return "F"
                    case _: return cuarto_actual
                    
            case "bajar":
                match cuarto_actual:
                    case "E": return "B"
                    case _: return cuarto_actual
            
            case _:
                # Si la acción es limpiar o nada, el robot se queda en el mismo cuarto
                return cuarto_actual
            

    def transición(self, accion):
        if not self.acción_legal(accion) or not self.puede_hacer(self.x[0], accion):##añadida la funcion puede_hacer que determina la accion segun la posicion
            raise ValueError("La acción no es legal para este estado")
        robot, a, b, c, d, e, f = self.x 
        if accion == "nada" or a == "sucio" or b == "sucio" or c == "sucio" or d == "sucio" or e == "sucio" or f == "sucio":
            self.desempeño -= 1 ##si la accion es no hacer nada o hay cuartos sucios penalizo
        if accion == "limpiar":
            idx = 1 + "ABCDEF".find(self.x[0])
            self.x[idx] = "limpio" ##lo que hago aca es buscar si, en el cuarto en el que me encuentro, el estado es limpio
            self.desempeño -= 0.5
        else:
            if accion in ("ir_izquierda","ir_derecha"):
                self.desempeño -= 1
            elif accion in ("subir","bajar"):
                self.desempeño -= 2
            self.x[0] = self.definir_destino(self.x[0],accion) ##define el paradero según la accion y la posicion
            
            
    def percepción(self):
        idx = 1 + "ABCDEF".find(self.x[0])
        return self.x[0], self.x[idx] ##Donde me encuentro y cual es mi estado
    
class AgenteAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones, entorno):
        self.acciones = acciones
        self.entorno = entorno

    def programa(self, percepcion):
        robot, _ = percepcion
        while True:
            eleccion_aleatoria = choice(self.acciones)
            if self.entorno.puede_hacer(robot, eleccion_aleatoria):
                return eleccion_aleatoria
    
        
def test():
    """
    Prueba del entorno y los agentes

    """
    print("Prueba del entorno con un agente aleatorio")
    acciones=["ir_derecha", "ir_izquierda", "subir", "bajar", "limpiar", "nada"]
    entorno = SeisCuartos()
    entornos_o.simulador(entorno, AgenteAleatorio(acciones, entorno), 10)



if __name__ == "__main__":
    test()