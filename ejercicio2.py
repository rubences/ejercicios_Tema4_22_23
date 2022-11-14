#arbol rojo y negro
# -*- coding: utf-8 -*-
import sys
import os
import time
import random
import math
import pygame

from pygame.locals import *

# Constantes
WIDTH = 640
HEIGHT = 480
FPS = 30

# Colores


# Clases y funciones
class Nodo:
    def __init__(self, valor, color):
        self.valor = valor
        self.color = color
        self.izq = None
        self.der = None
        self.padre = None

    def __str__(self):

        return str(self.valor)

class Arbol:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        nuevo = Nodo(valor, ROJO)

        if self.raiz == None:
            self.raiz = nuevo
            self.raiz.color = NEG
        else:
            actual = self.raiz
            while True:
                if valor < actual.valor:
                    if actual.izq == None:
                        actual.izq = nuevo
                        nuevo.padre = actual
                        break
                    else:
                        actual = actual.izq
                else:
                    if actual.der == None:
                        actual.der = nuevo
                        nuevo.padre = actual
                        break
                    else:
                        actual = actual.der

        self.balancear(nuevo)

    def balancear(self, nodo):
        while nodo != self.raiz and nodo.padre.color == ROJO:
            if nodo.padre == nodo.padre.padre.izq:
                tio = nodo.padre.padre.der
                if tio != None and tio.color == ROJO:
                    nodo.padre.color = NEG
                    tio.color = NEG
                    nodo.padre.padre.color = ROJO
                    nodo = nodo.padre.padre
                else:
                    if nodo == nodo.padre.der:
                        nodo = nodo.padre
                        self.rotar_izq(nodo)
                    nodo.padre.color = NEG
                    nodo.padre.padre.color = ROJO
                    self.rotar_der(nodo.padre.padre)
            else:
                tio = nodo.padre.padre.izq
                if tio != None and tio.color == ROJO:
                    nodo.padre.color = NEG
                    tio.color = NEG
                    nodo.padre.padre.color = ROJO
                    nodo = nodo.padre.padre
                else:
                    if nodo == nodo.padre.izq:
                        nodo = nodo.padre
                        self.rotar_der(nodo)
                    nodo.padre.color = NEG
                    nodo.padre.padre.color = ROJO
                    self.rotar_izq(nodo.padre.padre)

        self.raiz.color = NEG

    def rotar_der(self, nodo):
        temp = nodo.izq
        nodo.izq = temp.der

        if temp.der != None:
            temp.der.padre = nodo

        temp.padre = nodo.padre

        if nodo.padre == None:
            self.raiz = temp
        else:
            if nodo == nodo.padre.der:
                nodo.padre.der = temp
            else:
                nodo.padre.izq = temp

        temp.der = nodo
        nodo.padre = temp

    def rotar_izq(self, nodo):
        

        temp = nodo.der
        nodo.der = temp.izq

        if temp.izq != None:
            temp.izq.padre = nodo

        temp.padre = nodo.padre

        if nodo.padre == None:
            self.raiz = temp
        else:
            if nodo == nodo.padre.izq:
                nodo.padre.izq = temp
            else:
                nodo.padre.der = temp

        temp.izq = nodo
        nodo.padre = temp

    def imprimir(self):
        self.imprimir_aux(self.raiz)

    def imprimir_aux(self, nodo):
        if nodo != None:
            self.imprimir_aux(nodo.izq)
            print nodo.valor, nodo.color
            self.imprimir_aux(nodo.der)

    def buscar(self, valor):
        return self.buscar_aux(self.raiz, valor)

    def buscar_aux(self, nodo, valor):
        if nodo == None:
            return None
        elif nodo.valor == valor:
            return nodo
        elif valor < nodo.valor:
            return self.buscar_aux(nodo.izq, valor)
        else:
            return self.buscar_aux(nodo.der, valor)

    def eliminar(self, valor):
        nodo = self.buscar(valor)
        if nodo != None:
            self.eliminar_aux(nodo)

    def eliminar_aux(self, nodo):

        if nodo.izq == None or nodo.der == None:
            hijo = nodo
        else:
            hijo = self.sucesor(nodo)

        if hijo.izq != None:
            nieto = hijo.izq
        else:
            nieto = hijo.der

        if nieto != None:
            nieto.padre = hijo.padre

        if hijo.padre == None:
            self.raiz = nieto
        else:
            if hijo == hijo.padre.izq:
                hijo.padre.izq = nieto
            else:
                hijo.padre.der = nieto

        if hijo != nodo:
            nodo.valor = hijo.valor

        if hijo.color == NEG:
            self.eliminar_balancear(nieto)

    def eliminar_balancear(self, nodo):

        while nodo != self.raiz and nodo.color == NEG:
            if nodo == nodo.padre.izq:
                hermano = nodo.padre.der
                if hermano.color == ROJO:
                    hermano.color = NEG
                    nodo.padre.color = ROJO
                    self.rotar_izq(nodo.padre)
                    hermano = nodo.padre.der

                if hermano.izq.color == NEG and hermano.der.color == NEG:
                    hermano.color = ROJO
                    nodo = nodo.padre
                else:
                    if hermano.der.color == NEG:
                        hermano.izq.color = NEG
                        hermano.color = ROJO
                        self.rotar_der(hermano)
                        hermano = nodo.padre.der

                    hermano.color = nodo.padre.color
                    nodo.padre.color = NEG
                    hermano.der.color = NEG
                    self.rotar_izq(nodo.padre)
                    nodo = self.raiz
            else:
                hermano = nodo.padre.izq
                if hermano.color == ROJO:
                    hermano.color = NEG
                    nodo.padre.color = ROJO
                    self.rotar_der(nodo.padre)
                    hermano = nodo.padre.izq

                if hermano.der.color == NEG and hermano.izq.color == NEG:
                    hermano.color = ROJO
                    nodo = nodo.padre
                else:
                    if hermano.izq.color == NEG:
                        hermano.der.color = NEG
                        hermano.color = ROJO
                        self.rotar_izq(hermano)
                        hermano = nodo.padre.izq

                    hermano.color = nodo.padre.color
                    nodo.padre.color = NEG
                    hermano.izq.color = NEG
                    self.rotar_der(nodo.padre)
                    nodo = self.raiz

        nodo.color = NEG

    def sucesor(self, nodo):
        if nodo.der != None:
            return self.minimo(nodo.der)
        else:
            temp = nodo.padre
            while temp != None and nodo == temp.der:
                nodo = temp
                temp = temp.padre
            return temp

    def minimo(self, nodo):
        while nodo.izq != None:
            nodo = nodo.izq
        return nodo

    def maximo(self, nodo):
        while nodo.der != None:
            nodo = nodo.der
        return nodo

    def imprimir_inorden(self):
        self.imprimir_inorden_aux(self.raiz)

    def imprimir_inorden_aux(self, nodo):
        if nodo != None:
            self.imprimir_inorden_aux(nodo.izq)
            print nodo.valor
            self.imprimir_inorden_aux(nodo.der)

    def imprimir_preorden(self):
        self.imprimir_preorden_aux(self.raiz)

    def imprimir_preorden_aux(self, nodo):
        if nodo != None:
            print nodo.valor
            self.imprimir_preorden_aux(nodo.izq)
            self.imprimir_preorden_aux(nodo.der)

    def imprimir_postorden(self):
        self.imprimir_postorden_aux(self.raiz)

    def imprimir_postorden_aux(self, nodo):
        if nodo != None:
            self.imprimir_postorden_aux(nodo.izq)
            self.imprimir_postorden_aux(nodo.der)
            print nodo.valor

    def imprimir_nivel(self, nivel):
        self.imprimir_nivel_aux(self.raiz, nivel)

    def imprimir_nivel_aux(self, nodo, nivel):
        if nodo != None:
            if nivel == 0:
                print nodo.valor
            else:
                self.imprimir_nivel_aux(nodo.izq, nivel - 1)
                self.imprimir_nivel_aux(nodo.der, nivel - 1)

    def imprimir_por_niveles(self):
        altura = self.altura()
        for i in range(altura):
            self.imprimir_nivel(i)

    def altura(self):
        return self.altura_aux(self.raiz)
    
    def altura_aux(self, nodo):
        if nodo == None:
            return 0
        else:
            return 1 + max(self.altura_aux(nodo.izq), self.altura_aux(nodo.der))

    def imprimir_por_niveles2(self):

        cola = Cola()
        cola.encolar(self.raiz)

        while not cola.es_vacia():
            nodo = cola.desencolar()
            print nodo.valor
            if nodo.izq != None:
                cola.encolar(nodo.izq)
            if nodo.der != None:
                cola.encolar(nodo.der)

    def imprimir_por_niveles3(self):
            
            cola = Cola()
            cola.encolar(self.raiz)
    
            while not cola.es_vacia():
                nodo = cola.desencolar()
                print nodo.valor
                if nodo.izq != None:
                    cola.encolar(nodo.izq)
                if nodo.der != None:
                    cola.encolar(nodo.der)

    def imprimir_por_niveles4(self):
                
                cola = Cola()
                cola.encolar(self.raiz)
        
                while not cola.es_vacia():
                    nodo = cola.desencolar()
                    print nodo.valor
                    if nodo.izq != None:
                        cola.encolar(nodo.izq)
                    if nodo.der != None:
                        cola.encolar(nodo.der)
                    
    def imprimir_por_niveles5(self):
                        
                        cola = Cola()
                        cola.encolar(self.raiz)
                
                        while not cola.es_vacia():
                            nodo = cola.desencolar()
                            print nodo.valor
                            if nodo.izq != None:
                                cola.encolar(nodo.izq)
                            if nodo.der != None:
                                cola.encolar(nodo.der)

    def imprimir_por_niveles6(self):
                                    
                                    cola = Cola()
                                    cola.encolar(self.raiz)
                            
                                    while not cola.es_vacia():
                                        nodo = cola.desencolar()
                                        print nodo.valor
                                        if nodo.izq != None:
                                            cola.encolar(nodo.izq)
                                        if nodo.der != None:
                                            cola.encolar(nodo.der)
                                            





