from directorioFunciones import *
from cuadruplos import *

class memoriaVirtual():
    def __init__(self):
        self.mGlobal = valoresmemoria(5500, 6500, 7500)
        self.mLocales = valoresmemoria(8500, 9500, 10500)
        self.mTemporales = valoresmemoria(11500, 12500, 13500)
        self.mConstante = valoresmemoria(14500, 15500, 16500)
        self.mTempArr = valoresmemoria(17500, 18500, 19500)


    def fixType(self,dir,value):
        if dir < 8500:
            return self.mGlobal.fixType(dir,value)
        elif dir < 11500:
            return self.mLocales.fixType(dir,value)
        elif dir < 14500:
            return self.mTemporales.fixType(dir,value)
        elif dir < 17500:
            return self.mConstante.fixType(dir,value)
        elif dir < 19500:
            return self.mTempArr.fixType(dir,value)

    def sacarType(self,dir):
        if dir < 8500:
            return self.mGlobal.sacarType(dir)
        elif dir < 11500:
            return self.mLocales.sacarType(dir)
        elif dir < 14500:
            return self.mTemporales.sacarType(dir)
        elif dir < 17500:
            return self.mConstante.sacarType(dir)
        elif dir < 19500:
            return self.mTempArr.sacarType(dir)

    def obtenerValor(self,dir):
        if dir < 8500:
            return self.mGlobal.obtenerValor(dir)
        elif dir < 11500:
            return self.mLocales.obtenerValor(dir)
        elif dir < 14500:
            return self.mTemporales.obtenerValor(dir)
        elif dir < 17500:
            return self.mConstante.obtenerValor(dir)
            print("PRUEBA ASIGNACION " +  str(self.mConstante.obtenerValor(dir)))
        elif dir < 19500:
            return self.mTempArr.obtenerValor(dir)

    def meterValor(self,value,dir):
        if dir < 8500:
            self.mGlobal.meterValor(value,dir)
        elif dir < 11500:
            self.mLocales.meterValor(value,dir)
        elif dir < 14500:
            self.mTemporales.meterValor(value,dir)
        elif dir < 17500:
            self.mConstante.meterValor(value,dir)
           # self.mConstante.obtenerValor(dir)
          #  print("PRUEBA ASIGNACION " +  str(self.mConstante.obtenerValor(dir)))
        elif dir < 19500:
            self.mTempArr.meterValor(value,dir)

    def colocarValores(self,funcion):
        if funcion.id != 'CONST':
            for i in range(0, len(funcion.varTable)):
                self.meterValor(0, funcion.varTable[i].dir)
               # print("aaaaaah " + str(funcion.varTable[i].dir))
        else:
            for i in range(0, len(funcion.varTable)):
                print(str(funcion.varTable[i].id) + " " + str(funcion.varTable[i].dir))
                self.meterValor(funcion.varTable[i].id, funcion.varTable[i].dir)

class valoresmemoria():
    def __init__(self,tmpInt,tmpFloat,tmpBool):
        self.tmpInt = tmpInt
        self.tmpFloat = tmpFloat
        self.tmpBool = tmpBool
        self.vInt = []
        self.vFloat = []
        self.vBool = []


    def fixType(self,dir,value):
        if dir < self.tmpFloat:
            return int(value)
        elif dir < self.tmpBool:
            return float(value)
        else:
            return value

    def sacarType(self,dir):
        if dir < self.tmpFloat:
            return 'INT'
        elif dir < self.tmpBool:
            return 'FLOAT'
        else:
            return 'BOOL'

    def obtenerValor(self,dir):
        if dir < self.tmpFloat:
            return self.vInt[dir-self.tmpInt]
            #print("+++++++++++++++++++++++++ " + str(self.vInt[dir-self.tmpInt]))
        elif dir < self.tmpBool:
            return self.vFloat[dir-self.tmpFloat]
           # print("################################ " + str(self.vFloat[dir-self.tmpFloat]))
        else:
            return self.vBool[dir-self.tmpBool]
           # print("//////////////////////// " + str(self.vBool[dir-self.tmpBool]))

    def meterValor(self,value,dir):
        #print("----------- " + str(len(self.vInt)) + " " + str(dir-self.tmpInt))
        if dir < self.tmpFloat:
           # print("******************* " + str(len(self.vInt)) + " " + str(dir-self.tmpInt))
            if len(self.vInt) > abs(dir-self.tmpInt):
                self.vInt[dir-self.tmpInt] = value
            else:
                self.vInt.append(value)
        elif dir < self.tmpBool:
            if len(self.vFloat) > abs(dir-self.tmpFloat):
                self.vFloat[dir-self.tmpFloat] = value
            else:
                self.vFloat.append(value)
        else:
            if len(self.vBool) > abs(dir-self.tmpBool):
                self.vBool[dir-self.tmpBool] = value
            else:
                self.vBool.append(value)