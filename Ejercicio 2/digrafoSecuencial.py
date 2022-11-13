import numpy as np
from colaEnlazada import ColaE
from CeldaTabla import CeldaTabla

class DiGradoSecuencial:
    __tam = None

    def __init__ (self, tam):
        self.__tam = tam
        self.__matriz = np.zeros((tam,tam), dtype = int)
    
    def Agregar(self, nodo1, nodo2, peso = 1):
        nodo1 -= 1
        nodo2 -= 1
        if (0 <= nodo1 < self.__tam) and (0 <= nodo2 < self.__tam):
            self.__matriz [nodo1][nodo2] = peso
        else:
            print("\nEl nodo ingresado no es correcto")
    
    def Adyacente (self,vertice):
        adyacente = []
        for i in range(self.__tam):
            if self.__matriz[vertice,i]:
                adyacente.append(i)
        return adyacente

    def REPvisita(self,arreglo,s,tiempo):
        tiempo +=1
        arreglo[s] = tiempo
        for u in self.Adyacente(s):
            if arreglo[u] == 0:
                return self.REPvisita(arreglo,u,tiempo)
        tiempo +=1
        return arreglo
    
    def REP(self):
        arreglo = np.zeros(self.__tam, dtype=int)
        tiempo = 0
        for s in range(self.__tam):
            if arreglo[s] == 0:
                arreglo = self.REPvisita(arreglo,s,tiempo)
        print(arreglo)

    def REA (self,origen):
        arreglo = -1*np.ones(self.__tam,dtype=int)
        cola = ColaE()
        cola.insertar(origen)
        arreglo[origen] = 0
        v = 0
        while not cola.vacia():
            cola.suprimir()
            for i in self.Adyacentes(v):
                    if arreglo[i] == -1:
                        arreglo[i] = arreglo[v] + 1
                        cola.insertar(i)
            v+=1
        print(arreglo)

    def WARSHALL (self):
        matrizCamino = self.__matriz
        for k in range(self.__tam):
            for i in range(self.__tam):
                for j in range(self.__tam):
                    if matrizCamino[i,j]  == 1 or (matrizCamino[i,k] * matrizCamino[k,j]) == 1:
                        matrizCamino[i,j] = 1
                    else:
                        matrizCamino[i,j] = 0
        return matrizCamino
    
    def Conexo(self):
        matriz = self.WARSHALL()
        resultado = True
        i = 0
        while i < self.__tam and resultado:
            j=0
            while j < self.__tam and resultado:
                
                if i != j and matriz[i,j] == 0:
                    resultado = False
                j+=1
            i+=1
        print(resultado)

    def Dijkstra(self,origen,destino):
        Tabla = np.empty(self.__tam,dtype=CeldaTabla)
        for i in range(self.__tam):
            Tabla[i] = CeldaTabla()
        Tabla[origen].setDistancia(0)
        v = origen
        for i in range(self.__tam):
            v = self.getV(Tabla)
            Tabla[v].setConocido(True)
            for w in self.Adyacentes(v):
                    if Tabla[w].getConocido() == False:
                        if (Tabla[v].getDistancia() + self.__matriz[v,w]) < Tabla[w].getDistancia():
                            Tabla[w].setDistancia(Tabla[v].getDistancia() + self.__matriz[v,w])
                            Tabla[w].setCamino(v)
        v = destino
        camino = [v]
        while Tabla[v].getCamino() != None:
            v = Tabla[v].getCamino()
            camino.insert(0,v)
        print(camino)
    
    def Prim(self,origen):
        Tabla = np.empty(self.__tam,dtype=CeldaTabla)
        for i in range(self.__tam):
            Tabla[i] = CeldaTabla()
        Tabla[origen].setDistancia(0)
        v = origen
        for i in range(self.__tam):
            v = self.getV(Tabla)
            Tabla[v].setConocido(True)
            for w in self.Adyacente(v):
                if self.__matriz[v,w] == 1:
                    if Tabla[w].getConocido() == False:
                        if self.__matriz[v,w] < Tabla[w].getDistancia():
                            Tabla[w].setDistancia(self.__matriz[v,w])
                            Tabla[w].setCamino(v)
        for i in range(len(Tabla)):
            print(str(i) + ": " + str(Tabla[i]))
        
    def getV(self,Tabla):
        v = 0
        mindist = 99999999
        for i in range(len(Tabla)):
            if Tabla[i].getConocido() == False and Tabla[i].getDistancia() < mindist:
                v = i
                mindist = Tabla[i].getDistancia()
        return v