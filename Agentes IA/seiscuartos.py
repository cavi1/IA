#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
seiscuartos.py.py
------------

"""

import entornos_o
from random import choice

__author__ = 'CAVI'


class Cuarto():
    def __init__(self, cuarto_inicial):
        self.cuarto_actual=cuarto_inicial
        self.disposicion={"A":"EII","B":"MI","C":"EID","D":"ESI","E":"MSPB","F":"ESD"}##aca se podría cambiar la disposición de los cuartos
        self.cuarto_izquierdo=""
        self.cuarto_derecho=""
        self.cuarto_superior=""
        self.cuarto_inferior=""
        self.get_cuartos()
    
    def get_cuartos(self):
        # Diccionario de adyacencias basado en las reglas
        adyacencias = {
            "EII": {"derecho": "MI", "superior": "ESI"},
            "MI": {"izquierdo": "EII", "derecho": "EID"},
            "EID": {"izquierdo": "MI", "superior": "ESD"},
            "ESI": {"derecho": "MSPB"},
            "MSPB": {"izquierdo": "ESI", "inferior": "MI", "derecho": "ESD"},
            "ESD": {"izquierdo": "MSPB"}
        }
        
        # Crear diccionario inverso para mapear códigos a nombres de cuartos
        inv_disposicion = {v: k for k, v in self.disposicion.items()}
        
        # Obtener el código del cuarto actual
        codigo_actual = self.disposicion[self.cuarto_actual]
        
        # Obtener las direcciones adyacentes
        direcciones = adyacencias.get(codigo_actual, {})
        
        # Asignar los cuartos adyacentes usando el diccionario inverso
        self.cuarto_izquierdo = inv_disposicion.get(direcciones.get("izquierdo", ""), "")
        self.cuarto_derecho = inv_disposicion.get(direcciones.get("derecho", ""), "")
        self.cuarto_superior = inv_disposicion.get(direcciones.get("superior", ""), "")
        self.cuarto_inferior = inv_disposicion.get(direcciones.get("inferior", ""), "")
        
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
    
    def __init__(self, x0=["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"], disposicion={"A":"EII","B":"MI","C":"EID","D":"ESI","E":"MSPB","F":"ESD"}):
        """
        Por default inicialmente el robot está en A y los seis cuartos
        están sucios

        """
        self.x = x0[:]
        self.desempeño = 0
        self.disposicion = disposicion
        
    
    
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
        
    def definir_destino(self, accion):
        if accion == "ir_derecha"

    def transición(self, accion):
        if not self.acción_legal(accion) or not self.puede_hacer(self.x[0], accion):##añadida la funcion puede_hacer que determina la accion segun la posicion
            raise ValueError("La acción no es legal para este estado")
        robot, a, b, c, d, e, f = self.x ## asigna a los valores robot, a, b ,c, d, e, f el estado actual
        if accion is not "nada" or a is "sucio" or b is "sucio" or c is "sucio" or d is "sucio" or e is "sucio" or f is "sucio":
            self.desempeño -= 1 ##si la accion es no hacer nada o el cuarto en el que me encuentro esta sucio penaliza
        if accion is "limpiar":
            self.x["ABCDEF".find(self.x[0])] = "limpio" ##lo que hago aca es buscar si, en el cuarto en el que me encuentro, el estado es limpio
            self.desempeño -= 0
        elif self.definir_destino(accion): ##define el paradero según la accion y la posicion
            
            
    def percepcion(self):
        return self.x[0], self.x["ABCDEF".find(self.x[0])] ##Donde me encuentro y cual es mi estado
    
class AgenteAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        return choice(self.acciones)
    
        
def test():
    """
    Prueba del entorno y los agentes

    """
    print("Prueba del entorno con un agente aleatorio")
    acciones=['ir_A', 'ir_B', 'limpiar', 'nada']
    entornos_o.simulador(SeisCuartos(),AgenteAleatorio(acciones),10)



if __name__ == "__main__":
    test()