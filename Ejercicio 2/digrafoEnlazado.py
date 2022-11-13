import numpy as np
from celdaTabla import CeldaTabla
from nodo import Nodo
from colaEnlazada import ColaE

class DiGrafoEncadenado:
    __tam = None

    def __init__ (self, tam):
        self.__tam = tam
        self.__matriz = np.zeros(tam, dtype = Nodo)
    
    def Agregar(self, nodo1, nodo2):
        nodo1 -= 1
        nodo2 -= 1
        if (0 <= nodo1 < self.__tam) and (0 <= nodo2 < self.__tam):
            self.InsertarNodo(nodo1, nodo2)
        else:
            print("\nEl nodo ingresado no es correcto")

    def InsertarNodo(self, pos, valor):
        NuevoNodo = Nodo(valor)
        if self.__matriz [pos] == None:
            self.__matriz [pos] = NuevoNodo
        else:
            aux = self.__matriz[pos]
            repetido = False
            while aux.getSiguiente() != None and repetido:
                if aux.getSiguiente().getValor() == valor:
                    repetido = True
                aux = aux.getSiguiente()
            if not repetido:
                aux.setSiguiente(NuevoNodo)
    
    def Adyacente(self,nodo):
        lista = []
        aux = self.__matriz[nodo]
        while aux != None:
            lista.append(aux.getValor())
            aux = aux.getSiguiente()
        return lista
    
    def Mostrar(self):
        for i in range(len(self.__matriz)):
            cadena = str(i) + ": "
            aux = self.__matriz[i]
            while aux != None:
                cadena += str(aux.getValor())
                aux = aux.getSiguiente()
            print(cadena)
    
    def REP_visita(self, nodo_origen, nodo_destino, d):
        d[nodo_origen] = 1
        adys = self.Adyacente(nodo_origen)
        for nodos in adys:
            if nodos == nodo_destino:
                return [nodo_destino]
            if d[nodos] == 0:
                retorno = self.REP_visita(nodos, nodo_destino, d)
                if isinstance(retorno, list):
                    retorno.insert(0,nodos)
                    return retorno
        return 0
    
    def getCamino(self,inicio,fin):
        d= np.zeros(self.__tam,dtype=int)
        resultado = self.REP_visita(inicio, fin, d)
        if isinstance(resultado,list):
            resultado.insert(0,inicio)
        return resultado
    
    def REPvisita(self,arreglo,s,tiempo):
        tiempo +=1
        arreglo[s] = tiempo
        for u in self.Adyacentes(s):
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

    def REA(self,origen):
        arreglo = -1*np.ones(self.__tam,dtype=int)
        cola = ColaE()
        cola.insertar(origen)
        arreglo[origen] = 0
        v = 0
        while not cola.vacia():
            cola.suprimir()
            for i in self.Adyacente(v):
                    if arreglo[i] == -1:
                        arreglo[i] = arreglo[v] + 1
                        cola.insertar(i)
            v+=1
        print(arreglo)
    
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
    
    def WARSHALL (self):
        matrizCamino = np.zeros((self.__tam,self.__tam),dtype=int)
        for i in range(self.__tam):
            for j in self.Adyacente(i):
                matrizCamino[i,j] = 1
        for k in range(self.__tam):
            for i in range(self.__tam):
                for j in range(self.__tam):
                    if matrizCamino[i,j]  == 1 or (matrizCamino[i,k] * matrizCamino[k,j]) == 1:
                        matrizCamino[i,j] = 1
                    else:
                        matrizCamino[i,j] = 0
        return matrizCamino
    
    def Prim(self,origen):
        Tabla = np.empty(self.__tam,dtype=CeldaTabla)
        for i in range(self.__tam):
            Tabla[i] = CeldaTabla()
        Tabla[origen].setDistancia(0)
        v = origen
        for i in range(self.__tam):
            v = self.getV(Tabla)
            Tabla[v].setConocido(True)
            for w in self.Adyacentes(v):
                if self.__matriz[v,w] == 1:
                    if Tabla[w].getConocido() == False:
                        if self.__matriz[v,w] < Tabla[w].getDistancia():
                            Tabla[w].setDistancia(self.__matriz[v,w])
                            Tabla[w].setCamino(v)
        return Tabla
    
    def getV(self,Tabla):
        v = 0
        mindist = 99999999
        for i in range(len(Tabla)):
            if Tabla[i].getConocido() == False and Tabla[i].getDistancia() < mindist:
                v = i
                mindist = Tabla[i].getDistancia()
        return v
    
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