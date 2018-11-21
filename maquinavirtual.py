from cuadruplos import *
from directorioFunciones import *
from memoriavirtual import *
from turtle import  *

class parametro():
    def __init__(self,value,type):
        self.value = value
        self.type = type

class maquinavirtual():
    def __init__(self, funciones, cuadruplos):
        self.cuadruplos = cuadruplos
        self.funciones = funciones
        
        self.cuadruploActual = 0
        self.regresaCuadruplo = []
        self.regresaDireccion = []

        self.memoria = memoriaVirtual()
        
        for i in range(0,len(self.funciones.funciones)):
            self.memoria.colocarValores(self.funciones.funciones[i])

        self.parametros = []

    def goto(self,cuadruplos):
        self.cuadruploActual = cuadruplos.var3-1

    def gotoF(self,cuadruplos,memoria):
        var1 = self.memoria.obtenerValor(cuadruplos.var1)
        if not var1:
            self.cuadruploActual = cuadruplos.var3-1

    def goSub(self,cuadruplos):
        begin = cuadruplos.var1
        self.regresaCuadruplo.append(self.cuadruploActual)
        self.run(begin,'EndProc')
        #print(str(begin = cuadruplos.var1))
        self.cuadActual = self.regresaCuadruplo.pop()

    def param(self,cuadruplos,memoria):
        valor = memoria.obtenerValor(cuadruplos.var1)
        tipo = memoria.sacarType(cuadruplos.var1)
        param = parametro(valor,tipo)
        self.parametros.append(param)
    
    def ret(self,cuadruplos,memoria):
        value = memoria.getValue(var.var1)
        dir = self.regresaDireccion.pop()
        memoria.setValue(value,dir)
    
    def verifica(self,cuadruplos,memoria):
        var1 = cuadruplos.var1
        var2 = cuadruplos.var2
        value = memoria.obtenerValor(cuadruplos.var3)
        value = memoria.fixType(cuadruplos.var3, value)
        if not value<var1 and value>var2:
            print('No cabe')
    
    def era(self, cuadruplos):
        self.regresaDireccion.append(cuadruplos.var1)
    

    def ARRDef(self,cuadruplos,memoria):
        var1 = cuadruplos.var1
        var1 = var1+1
        var2 = memoria.obtenerValor(cuadruplos.var2)
        var2 = memoria.fixType(cuadruplos.var2, var2)
        value = var1+var2
        memoria.meterValor(value,cuadruplos.var3)
        memoria.meterValor(var2,value)

    def opDivision(self,cuadruplos,memoria):
        var2 = memoria.getValue(cuadruplos.var2)
        var2 = memoria.fixType(cuadruplos.var2, var2)
        if(arg2 == 0):
            print('division entre 0')
            quit()
        else:
            var1 = memoria.obtenerValor(cuadruplos.var1)
            var1 = memoria.fixType(cuadruplos.var1,var1)
            var3 = cuadruplos.var3
            valor = var1 / var2
            memoria.meterValor(valor,var3)

    def opDivMod(self,cuadruplos,memoria):
        var2 = memoria.getValue(cuadruplos.var2)
        var2 = memoria.fixType(cuadruplos.var2, var2)
        if(arg2 == 0):
            print('division entre 0')
            quit()
        else:
            var1 = memoria.obtenerValor(cuadruplos.var1)
            var1 = memoria.fixType(cuadruplos.var1,var1)
            var3 = cuadruplos.var3
            valor = var1 % var2
            memoria.meterValor(valor,var3)

    def opMatematica(self,cuadruplos,memoria):
        var1 = memoria.obtenerValor(cuadruplos.var1)
        var2 = memoria.obtenerValor(cuadruplos.var2)
        var3 = cuadruplos.var3
        estatuto = cuadruplos.estatuto
        var1 = memoria.fixType(cuadruplos.var1, var1)
        var2 = memoria.fixType(cuadruplos.var2, var2)

        if estatuto == '+':
            valor = var1 + var2
        
        elif estatuto == '-':
            valor = var1 - var2
        
        elif estatuto == '*':
            valor = var1 * var2
        
        elif estatuto == '/':
            valor = var1 / var2

        elif estatuto == '%':
            valor = var1 / var2
        memoria.meterValor(valor,var3)

    def opComparacion(self,cuadruplos,memoria):
        var1 = memoria.obtenerValor(cuadruplos.var1)
        var2 = memoria.obtenerValor(cuadruplos.var2)
        var3 = cuadruplos.var3
        estatuto = cuadruplos.estatuto
        var1 = memoria.fixType(cuadruplos.var1, var1)
        var2 = memoria.fixType(cuadruplos.var2, var2)

        if estatuto == '>':
            valor = var1 > var2

        elif estatuto == '>=':
            valor = var1 >= var2
        
        elif estatuto == '<':
            valor = var1 < var2
        
        elif estatuto == '<=':
            valor = var1 <= var2

        elif estatuto == '!=':
            valor = var1 != var2
        
        elif estatuto == '==':
            valor = var1 == var2
        
        elif estatuto == '%':
            valor = var1 / var2
        memoria.meterValor(valor,var3)

    def signoIgual(self,cuadruplos,memoria):
        valor = memoria.obtenerValor(cuadruplos.var1)
        #print('valor signo igual ' + str(valor))
        memoria.meterValor(valor, cuadruplos.var3)

    def despliega(self,cuadruplos,memoria):
        valor = memoria.obtenerValor(cuadruplos.var1)
        print(valor)

    def mandarparam(self,cuadruplos,memoria):
        valor = memoria.obtenerValor(cuadrup.var1)
        tipo = memoria.sacarType(cuadrup.var1)
        parametro = param(valor,tipo)
        self.parametros.append(parametro)
 

    def dibujaCirculo(self,cuadruplos,memoria):
        var1 = memoria.obtenerValor(cuadruplos.var1)
        vRadio = memoria.fixType(cuadruplos.var1, var1)
        var2 = memoria.obtenerValor(cuadruplos.var2)
        vWidth = memoria.fixType(cuadruplos.var2, var2)
        var3 = memoria.obtenerValor(cuadruplos.var3)
        vColor = memoria.fixType(cuadruplos.var3, var3)
        #self.c.create_oval(vRadio - vColor, vWidth - vColor, vRadio + vColor, vWidth + vColor, fill='black')

        hideturtle()
        if vColor == 1:
            color("red")
        if vColor == 2:
            color("purple")
        if vColor == 3:
            color("blue")

        width(vWidth)
        penup()
        goto(10,10)
        pendown()
        begin_fill()
        circle(vRadio)
        end_fill()
        done()

    def dibujaRectangulo(self,cuadruplos,memoria):
        var1 = memoria.obtenerValor(cuadruplos.var1)
        vLargo = memoria.fixType(cuadruplos.var1, var1)
        var2 = memoria.obtenerValor(cuadruplos.var2)
        vAlto = memoria.fixType(cuadruplos.var2, var2)
        var3 = memoria.obtenerValor(cuadruplos.var3)
        vColor = memoria.fixType(cuadruplos.var3, var3)

        hideturtle()
        if vColor == 1:
            color("red")
        if vColor == 2:
            color("purple")
        if vColor == 3:
            color("blue")
        
        penup()
        goto(10,10)
        pendown()
        begin_fill()
        forward(vLargo)
        left(90)
        forward(vAlto)
        left(90)
        forward(vLargo)
        left(90)
        forward(vAlto)
        end_fill()
        done()

    def dibujaEspiral(self,cuadruplos,memoria):
        var1 = memoria.obtenerValor(cuadruplos.var1)
        vRango = memoria.fixType(cuadruplos.var1, var1)
        var2 = memoria.obtenerValor(cuadruplos.var2)
        vAngulo = memoria.fixType(cuadruplos.var2, var2)
        var3 = memoria.obtenerValor(cuadruplos.var3)
        vColor = memoria.fixType(cuadruplos.var3, var3)

        hideturtle()
        if vColor == 1:
            color("red")
        if vColor == 2:
            color("purple")
        if vColor == 3:
            color("blue")
        self.penup()
        goto(10,10)
        self.pendown()
        for i in range(vRango): # this "for" loop will repeat these functions n times
            self.forward(i)
            self.left(vAngulo)
        done()

    def dibujaEstrella(self,cuadruplos,memoria):
        var1 = memoria.obtenerValor(cuadruplos.var1)
        vVertices = memoria.fixType(cuadruplos.var1, var1)
        var2 = memoria.obtenerValor(cuadruplos.var2)
        vStep= memoria.fixType(cuadruplos.var2, var2)
        var3 = memoria.obtenerValor(cuadruplos.var3)
        vLargo = memoria.fixType(cuadruplos.var3, var3)
        hideturtle()
        color("blue")
        penup()
        goto(10,10)
        pendown()
        for i in range(vVertices): # this "for" loop will repeat these functions n times
            forward(vLargo)
            right(vStep*360.0/vVertices)
        done()



    def run(self,begin,end):
        memoria = memoriaVirtual()
        memoria.mConstante = self.memoria.mConstante
        memoria.mGlobal = self.memoria.mGlobal

        for i in range(2,len(self.funciones.funciones)):
            memoria.colocarValores(self.funciones.funciones[i])
        self.cuadruploActual = begin    
        
        while self.cuadruplos[self.cuadruploActual].estatuto != end:
            cuadruplo = self.cuadruplos[self.cuadruploActual]
            print(cuadruplo)
            accion = cuadruplo.estatuto
        
            if accion == 'Goto':
                self.goto(cuadruplo)
            
            elif accion == 'GotoF':
                self.gotoF(cuadruplo, memoria)
            
            elif accion == 'Era':
                self.era(cuadruplo)
            
            elif accion == 'Gosub':
                self.goSub(cuadruplo)
            
            elif accion == 'Param':
                self.param(cuadruplo,memoria)

            elif accion == 'Return':
                self.ret(cuadruplo,memoria)
            
            elif accion == 'Ver':
                self.verifica(cuadruplo, memoria)
            
            elif accion == '+ARR':
                self.ARRDef(cuadruplo, memoria)

            elif accion == 'Read':
                self.despliega(cuadruplo, memoria)

            elif accion == 'Write':
                self.despliega(cuadruplo, memoria)
            
            
            elif accion == '+' or accion == '-' or accion == '*':
                self.opMatematica(cuadruplo,memoria)

            elif accion == '/':
                self.opDivision(cuadruplo,memoria)

            elif accion == '%':
                self.opDivMod(cuadruplo,memoria)
            
            elif accion == 'AND' or accion == 'OR' or accion == '<' or accion == '<=' or accion == '>' or accion == '>=' or accion == '!=' or accion == '==':
                self.opComparacion(cuadruplo,memoria)
            
            elif accion == '=':
                self.signoIgual(cuadruplo, memoria)

            elif accion == 'Circulo':
                self.dibujaCirculo(cuadruplo,memoria)

            elif accion == 'Rectangulo':
                self.dibujaRectangulo(cuadruplo,memoria)

            elif accion == 'Espiral':
                self.dibujaEspiral(cuadruplo,memoria)

            elif accion == 'Estrella':
                self.dibujaEstrella(cuadruplo,memoria)

            else:
                print('ERROR, cuadruplo no acceptado: ')
                print(cuadruplo)

            self.cuadruploActual = self.cuadruploActual + 1

        self.memoria.mConst = memoria.mConstante
        self.memoria.mGlobal = memoria.mGlobal