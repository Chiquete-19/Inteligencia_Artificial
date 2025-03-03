class Nodo:
    def __init__(self, datos, nivel,fval, padre):
        self.datos = datos
        self.nivel = nivel
        self.fval = fval
        self.padre = padre
    
    def genera_hijos(self):
        x,y = self.buscar(self.datos,'_')
        
        lista_valores = [[x,y-1],[x,y+1],[x-1,y],[x+1,y]]
        hijos = []
        
        for i in lista_valores:
            hijo = self.mezclar(self.datos,x,y,i[0],i[1])
            if hijo is not None:
                nodo_hijo = Nodo(hijo, self.nivel+1,0, self)
                hijos.append(nodo_hijo)
        return hijos
    
    def mezclar(self,puz,x1,y1,x2,y2):
        if x2>= 0 and x2 < len(self.datos) and y2 >= 0 and y2 < len(self.datos):
            temp_puz = []
            temp_puz = self.copiar(puz)
            temp = temp_puz[x2][y2]
            temp_puz[x2][y2] = temp_puz[x1][y1]
            temp_puz[x1][y1]=temp
            return temp_puz
        else:
            return None
    
    def copiar(self, root):
        temp = []
        for i in root:
            t = []
            for j in i:
                t.append(j)
            temp.append(t)
        return temp
    
    def buscar(self, puz, x):
        for i in range(0,len(self.datos)):
            for j in range(0,len(self.datos)):
                if puz[i][j] == x:
                    return i,j
                
    def imprimir_ruta(self,raiz):
        if raiz == None:
            return
        raiz.imprimir_ruta(raiz.padre)
        print("-------")
        
        raiz.imprimirse()
        
        
    def imprimirse(self):
        for i in self.datos:
            for j in i:
                print(j, end=" ")
            print("")
        
class Puzzle:
    def __init__(self, tam):
        self.n =tam
        self.abierto = []
        self.cerrado = []
    
    def aceptar(self):
        puz = []
        for i in range(0,self.n):
            temp = input().split(" ")
            puz.append(temp)
        return puz
    
    def f(self, inicio,final):
        return self.h(inicio.datos,final)+inicio.nivel

    def h(self,inicio,final):
        temp = 0
        for i in range(0, self.n):
            for j in range(0, self.n):
                if inicio[i][j] != final[i][j] and inicio[i][j] != '_':
                    temp +=1
        return temp
    
    def proceso(self):
        print("Ingresa el estado inicial del puzzle \n")
        inicio = [['1','2','3'],['4','5','6'],['7','_','8']] #self.aceptar()
        print("Ingresa el estado final del puzzle")
        final = [['1','2','3'],['4', '5','6'],['7','8','_']] #self.aceptar()
        
        inicio = Nodo(inicio,0,0, None)
        inicio.fval = self.f(inicio,final)
        
        self.abierto.append(inicio)
        
        print("\n\n")
        print("Procesando...\n")
        while True:
            print("...")
            act = self.abierto[0]
            
            if(self.h(act.datos,final) ==0):
                act.imprimir_ruta(act)
                break
            for i in act.genera_hijos():
                i.fval = self.f(i,final)
                self.abierto.append(i)
            self.cerrado.append(act)
            del self.abierto[0]
            
            self.abierto.sort(key = lambda x:x.fval,reverse =False)

if __name__ == '__main__':
    puz = Puzzle(3)
    puz.proceso()
   