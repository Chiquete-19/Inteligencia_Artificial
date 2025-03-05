import heapq
import copy
import time

class Nodo:
    def __init__(self, datos, nivel, fval, padre=None):
        self.datos = datos
        self.nivel = nivel
        self.fval = fval
        self.padre = padre

    def __lt__(self, otro):
        return self.fval < otro.fval

    def generar_hijos(self):
        x, y = self.buscar(0)  # 0 representa el espacio vacío
        movimientos = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]
        hijos = []
        
        for nx, ny in movimientos:
            if 0 <= nx < 3 and 0 <= ny < 3:
                nuevo_estado = copy.deepcopy(self.datos)
                nuevo_estado[x][y], nuevo_estado[nx][ny] = nuevo_estado[nx][ny], nuevo_estado[x][y]
                hijos.append(Nodo(nuevo_estado, self.nivel + 1, 0, self))
        
        return hijos

    def buscar(self, valor):
        for i in range(3):
            for j in range(3):
                if self.datos[i][j] == valor:
                    return i, j
        return None

    def imprimir_ruta(self):
        if self.padre:
            self.padre.imprimir_ruta()
        print("-------")
        for fila in self.datos:
            print(" ".join(map(str, fila)))

class Puzzle:
    def __init__(self):
        self.abierto = []
        self.cerrado = set()

    def heuristica(self, actual, objetivo):
        """Heurística de Manhattan"""
        distancia = 0
        for i in range(3):
            for j in range(3):
                if actual[i][j] != 0:
                    x, y = self.buscar_posicion(objetivo, actual[i][j])
                    distancia += abs(i - x) + abs(j - y)
        return distancia

    def buscar_posicion(self, estado, valor):
        for i in range(3):
            for j in range(3):
                if estado[i][j] == valor:
                    return i, j
        return None

    def resolver(self, inicio, objetivo):
        inicio_tiempo = time.time()
        nodo_inicial = Nodo(inicio, 0, 0)
        nodo_inicial.fval = self.heuristica(inicio, objetivo)
        heapq.heappush(self.abierto, nodo_inicial)
        movimientos = 0
        
        while self.abierto:
            actual = heapq.heappop(self.abierto)
            movimientos += 1
            if actual.datos == objetivo:
                fin_tiempo = time.time()
                actual.imprimir_ruta()
                print("Solución encontrada en {} movimientos".format(actual.nivel))
                print("Tiempo de ejecución: {:.4f} segundos".format(fin_tiempo - inicio_tiempo))
                return
            
            self.cerrado.add(tuple(map(tuple, actual.datos)))
            for hijo in actual.generar_hijos():
                if tuple(map(tuple, hijo.datos)) not in self.cerrado:
                    hijo.fval = hijo.nivel + self.heuristica(hijo.datos, objetivo)
                    heapq.heappush(self.abierto, hijo)
        
        print("No se encontró solución")

if __name__ == '__main__':
    estado_inicial = [[1, 0, 3], [4, 6, 7], [2, 5, 8]]
    estado_objetivo = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    puzzle = Puzzle()
    puzzle.resolver(estado_inicial, estado_objetivo)
