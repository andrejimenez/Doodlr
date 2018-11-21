import ply.lex as lex
import ply.yacc as yacc
import sys

import turtle

from lexer import *
from cuadruplos import *
from Cubo import *
from directorioFunciones import *
from maquinavirtual import *


aprobado = True

#Pilas
pilaOpp = []
pilaVar  = []
pilacuadruplos =[]
pilaSaltos = []
funciones =[]
cuadruplos =[]

#VariabLe
temporalContador = 1
tipoDeVar = 0
scope = 1

#globales
gInt = 0
gFloat = 0
gBool = 0
parametrosNum = 0

#locales
lInt = 0
lFloat = 0
lBool = 0

#constantes
cInt = 0
cFloat = 0
cBool = 0

#temporales
tmpInt = 0
tmpFloat = 0
tmpBool = 0
tmpIntArr = 0
tmpFloatArr = 0
tmpBoolArr = 0

funciones.append(EstrucFunc("CONST","VOID",1))
#funciones[0].varTable.append(Var("-1","INT",17500,None))
#cInt += 1
funciones.append(EstrucFunc("GLOBAL","VOID",1))


# Definicion de inicio de programa
def p_prog(p):
	'prog : startQuad globFunc changeScope DecFun PR_main fillMainQuad TO_BRACKOP setMainFuncionValores mainBlock TO_BRACKCLO end' 

#Crea el cuadruplo que dirige al MAIN
def p_startQuad(p):
    'startQuad :'
    pilaSaltos.append(len(cuadruplos))
    cuadruplos.append(cuadruplo(len(cuadruplos), 'Goto', None, None, None))

#Llena el valor de la redireccion del Goto main
def p_fillMainQuad(p):
    'fillMainQuad :'
    salto = pilaSaltos.pop()
    cuadruplos[salto].var3 = len(cuadruplos)


#Crea el cuadrupLo de cierre del programa
def p_end(p):
	'end : '
	cuadruplos.append(cuadruplo(len(cuadruplos), "END", None, None, None))

#El scope cambia, para así saber si trabajamos con variables globales o locales
def p_changeScope(p):
	'changeScope : '
	global scope
	scope = 0


#Definicion de bloque de declaracion de variables globales
def p_globFunc(p):
	'''globFunc : PR_global decVar globFunc
			| empty'''

#Definicion de bloque de declaracion de variables Funciones
def p_DecFun(p):
	'''DecFun : PR_function fun DecFun
			| empty'''

def p_fun(p):
	'fun : tipo ID agregaFuncion TO_PAROP param2 TO_PARCLO TO_BRACKOP mainBlock return TO_BRACKCLO endProcCuad'

def p_agregaFuncion(p):
	'''agregaFuncion : '''
	global scope
	funciones.append(EstrucFunc(p[-1], p[-2], len(cuadruplos)))
	#Obtiene Direccion para el tipo de func
	global gInt , gFloat , gBool , lInt , lFloat , lBool
	gInt = 0
	gFloat = 0
	gBool = 0
	lInt = 0
	lFloat = 0
	lBool = 0
	dire = setDireccionMem(p[-2],0,0,0,0,0,0)
	funciones[1].varTable.append(Var(p[-1], p[-2], dire, None))
	lenFunc = len(funciones)-1
	funciones[lenFunc].globDir = dire
	scope = lenFunc

def p_endProcCuad(p):
	'''endProcCuad : '''
	cuadruplos.append(cuadruplo(len(cuadruplos), 'EndProc', None, None , None))


def p_param2(p):
	'''param2 : tipo ID meteVariable
	         | tipo ID meteVariable TO_COMA param2'''

#Definicion de un bloque de codigo basico
def p_mainBlock(p):
	'''mainBlock : changeScope ciclos mainBlock
	 		| condicionales mainBlock
	 		| decVar mainBlock
	 		| llamadaDeFunciones mainBlock
	 		| igual mainBlock
	 		| write mainBlock
	 		| read mainBlock
			| empty'''


def p_setMainFuncionValores(p):
	'''setMainFuncionValores : '''
	global gInt , gFloat , gBool , lInt , lFloat , lBool
	gInt = 0
	gFloat = 0
	gBool = 0
	lInt = 0
	lFloat = 0
	lBool = 0

#Define Write
def p_write(p):
	'write : PR_write TO_PAROP  ID AgregaCuadWrite TO_PARCLO TO_PuntoComa'

#Define Read
def p_read(p):
	'read : PR_read TO_PAROP ID AgregaCuadRead TO_PARCLO TO_PuntoComa'

#Define Return
def p_return(p):
	'return : PR_return TO_PAROP ID AgregaCuadRet TO_PARCLO TO_PuntoComa'

# Definicion de asignacion
def p_igual(p):
	''' igual : ID AgregaVar OP_EQUALS AgregaOpp superExp TO_PuntoComa AgregaCuadIgual
			  | ID TO_CBRACKOP superExp TO_CBRACKCLO OP_EQUALS superExp cuadruploAsignaArr TO_PuntoComa AgregaCuadIgual'''

# Definicion de ciclos WHILE
def p_ciclo(p):
	' ciclos :  PR_While  TO_PAROP superExp IfQuad1 TO_PARCLO IfQuad1 TO_BRACKOP mainBlock IfQuad3 TO_BRACKCLO '


#Declaracion de Condicionales/ if y else
#Definicion de condicional if
def p_condicionales (p):
	' condicionales : PR_if TO_PAROP superExp TO_PARCLO IfQuad1 TO_BRACKOP mainBlock TO_BRACKCLO else IfQuad3'

#Definicion de condicional else
def p_else (p):
	''' else :  IfQuad2 PR_else TO_BRACKOP  mainBlock TO_BRACKCLO
		| empty'''
def p_WhileQuad1(p):
	'WhileQuad1 : '
	idx = pilaSaltos.pop()
	cuadruplos[idx].var3 = len(cuadruplos)

# guardar indice de cuadruplo del GotoF
def p_WhileQuad2(p):
	'WhileQuad2 : '
	pilaSaltos.append(len(cuadruplos))
	cuadruplos.append(cuadruplo(len(cuadruplos), "GotoF", getDireccionMem(pilaVar.pop()), None, None))


def p_WhileQuad3(p):
	'WhileQuad3 : '
	idx = pilaSaltos.pop()
	pilaSaltos.append(len(cuadruplos))
	cuadruplos.append(cuadruplo(len(cuadruplos), "Goto", None, None, None))
	cuadruplos[idx].var3 = len(cuadruplos)

#Declaracion de Variables , Arreglos

def p_tipo(p):
	''' tipo : PR_int
	         | PR_float
	         | PR_bool
	         | PR_void
	        '''
	p[0] = p[1]

def p_decVar (p):
 	''' decVar : PR_int  tipoVar decVar1 TO_PuntoComa
	         | PR_float  tipoVar decVar1 TO_PuntoComa
	         | PR_bool  tipoVar decVar1 TO_PuntoComa
	         | PR_void  tipoVar decVar1 TO_PuntoComa
	        '''

def p_decVar1 (p):
 	''' decVar1 : var decMasVar
 			 	| arreglo decMasVar '''

def p_decMasVar (p):
 	''' decMasVar :  TO_COMA decVar1
 			 	| empty '''

#Declaracion de variables
def p_var(p):
 	'var : ID meteVariable'

# meter tipo de var
def p_tipoVar(p):
	'tipoVar : empty'
	global tipoDeVar
	tipoDeVar = p[-1]

# Guarda Variable y le asigna direccion
def p_meteVariable(p):
	'meteVariable : empty'
	global scope

	ID = p[-1]

	localVars = list(map(lambda x: x.id, funciones[scope].varTable))
	#localVars = list(funciones[scope].varTable)

	globalVars = list(map(lambda x: x.id ,funciones[1].varTable))
	#globalVars = list(funciones[1].varTable)
	if ID in localVars or ID in globalVars:
		print(str(ID)+' ya fue definida')
	else:
		global tipoDeVar, gInt , gFloat , gBool , lInt , lFloat , lBool

		newDir = setDireccionMem(tipoDeVar, gInt , gFloat , gBool , lInt , lFloat , lBool)

		funciones[scope].varTable.append(Var(ID, tipoDeVar, newDir,None))


#Declaracion de arreglos
def p_arreglo(p):
   ' arreglo : ID TO_CBRACKOP TO_INT TO_CBRACKCLO escribeArr'

def p_escribeArr(p):
   'escribeArr : empty'
   global scope

   ID = p[-4]
   localVars = list(map(lambda x: x.id ,funciones[scope].varTable))
   globalVars = list(map(lambda x: x.id ,funciones[1].varTable))

   if ID in localVars or ID in globalVars:
    print(str(ID)+' ya fue definida')

   else:
    global tipoDeVar
    newDir = setDireccionMem(tipoDeVar, gInt , gFloat , gBool , lInt , lFloat , lBool)
    funciones[scope].varTable.append(Var(ID, tipoDeVar, newDir,p[-2]))

    for i in range(0,int(p[-2])):
        ID = p[-4] + '[' + str(i) + ']'
        newDir = setDireccionMem(tipoDeVar, gInt , gFloat , gBool , lInt , lFloat , lBool)
        funciones[scope].varTable.append(Var(ID, tipoDeVar, newDir,p[-2]))
##################################################


def p_superExp(p):
	'''superExp : Exp
	  			| Exp  PR_and AgregaOpp superExp AgregaCuadAnd
	  			| Exp  PR_or AgregaOpp superExp AgregaCuadAnd'''
	p[0] = p[1]

def p_Exp(p):
	''' Exp : miniExp
	    | miniExp OP_EQUALTO AgregaOpp miniExp AgregaCuadComp
	    | miniExp OP_DIFF AgregaOpp  miniExp AgregaCuadComp
        | miniExp OP_LESST AgregaOpp  miniExp AgregaCuadComp
        | miniExp OP_LESSTEQ AgregaOpp miniExp AgregaCuadComp
        | miniExp OP_GREATT AgregaOpp  miniExp AgregaCuadComp
        | miniExp OP_GREATTEQ AgregaOpp miniExp AgregaCuadComp '''
	p[0] = p[1]

def p_miniExp(p):
	''' miniExp : microExp
	 			| microExp OP_SUBS AgregaOpp miniExp AgregaCuadSR
	 			| microExp OP_ADD AgregaOpp miniExp  AgregaCuadSR'''
	p[0] = p[1]

def p_microExp (p):
	''' microExp : micromicroExp
			     | micromicroExp OP_MULT AgregaOpp microExp AgregaCuadMD
	 		     | micromicroExp OP_DIV AgregaOpp microExp AgregaCuadMD
	 		     | micromicroExp OP_MOD AgregaOpp microExp AgregaCuadMD'''
	p[0] = p[1]

def p_micromicroExp(p):
	''' micromicroExp :  sol
					  | sol OP_POW AgregaOpp micromicroExp AgregaCuadPow'''
	p[0] = p[1]

def p_sol(p):
	''' sol : ID AgregaVar
			| ID TO_CBRACKOP superExp TO_CBRACKCLO cuadArrPush
			| TO_INT CuadInt
			| TO_FLOAT CuadFloat
			| PR_true CuadBool
			| PR_false CuadBool
			| llamadaDeFunciones
			| TO_PAROP AgregaOpp superExp TO_PARCLO AgregaOpp  '''
	p[0] = p[1]


# llamada de fuciones
def p_llamadaDeFunciones(p):
	''' llamadaDeFunciones : ID eraCuadruplo TO_PAROP param TO_PARCLO TO_PuntoComa goSubCuadruplo
							| funcionesDibuja
							| empty'''

def p_funcionesDibuja(p):
    ''' funcionesDibuja : PR_circulo  TO_PAROP ID TO_COMA ID TO_COMA ID TO_PARCLO TO_PuntoComa circuloCuad
                        | PR_rectangulo TO_PAROP ID TO_COMA ID TO_COMA ID TO_PARCLO TO_PuntoComa rectanguloCuad
                        | PR_espiral TO_PAROP ID TO_COMA ID TO_COMA ID TO_PARCLO TO_PuntoComa espiralCuad
                        | PR_estrella TO_PAROP ID TO_COMA ID TO_COMA ID TO_PARCLO TO_PuntoComa estrellaCuad'''


def p_param(p):
	''' param : ID paramCuadruplo
	    	 | ID paramCuadruplo TO_COMA param
	    	 | empty '''

# Agrega operadores a la pila de operadores
def p_AgregaOpp(p):
	'AgregaOpp : empty'
	pilaOpp.append(p[-1]) #p[-1 ] quieredecir que se ira a la instrucion de atras menos 1 es decir se ira al operador


# Agrega Variables a la pila de Variables
def p_AgregaVar(p):
	'AgregaVar : empty'
	pilaVar.append(p[-1])

########################## CUADRUPLOS TIPO VARIABLES ################################

def p_CuadInt(p):
	'CuadInt : empty '
	pilaVar.append(p[-1])
	funciones[0].varTable.append(Var(p[-1], 'INT', getDirecConstantes('INT'),None))

def p_CuadFloat(p):
	'CuadFloat : empty '
	pilaVar.append(p[-1])
	funciones[0].varTable.append(Var(p[-1], 'FLOAT', getDirecConstantes('FLOAT'),None))

def p_CuadBool(p):
	'CuadBool : empty '
	pilaVar.append(p[-1])
	funciones[0].varTable.append(Var(p[-1], 'BOOL', getDirecConstantes('BOOL'),None))

########################## CUADRUPLOS ARREGLOS ################################

def p_CuadruploArrpush(p):
    "cuadArrPush : empty"
    # metemos en la lista de cuadruplos la verificacion de 0 a valor-1 o int(getDimensionVar(p[-4]))-1 y lo guardamos en un espacio de memoria
    cuadruplos.append(cuadruplo(len(cuadruplos), 'Ver' ,0, int(getDimensionVar(p[-4]))-1 , getDireccionMem(p[-2])))
    print("EL DIM " + str(getDimensionVar(p[-4])) )

    global temporalContador
    numTemporal = "t" + str(temporalContador)
    pilaVar.append(numTemporal)
    temporalContador = temporalContador + 1

    #Definimos que la direccion temporal siempre será int, por lo que en la lista de funciones se mete el contador de
    # variable temporal, el tipo INT y la direccion
    dire = getDirecTempArr('INT')
    funciones[scope].varTable.append(Var(numTemporal, 'INT', dire,None))

    #Muestra la fila de cuadruplos, agregando el operador +ARR obteniendo la direccion de memoria del inicio del arreglo,
    # la direccion de la constante/var local/var global y la direccion temporal del arreglo
    cuadruplos.append(cuadruplo(len(cuadruplos), '+ARR' ,getDireccionMem(p[-4]), getDireccionMem(p[-2]) , getDireccionMem(numTemporal)))
    pilaVar.append(numTemporal)
    temporalContador = temporalContador + 1

########################## CUADRUPLOS COMPARACION ################################

def p_AgregaCuadAnd(p):
	'AgregaCuadAnd : '
	if len(pilaOpp)> 0:
		global temporalContador
		if pilaOpp[len(pilaOpp)-1] == 'OR' or pilaOpp[len(pilaOpp)-1] == 'AND':
			op = pilaOpp.pop()
			temporal = pilaVar.pop()
			varT = "t" + str(temporalContador)
			dere = getDireccionMem(temporal)
			tipoDere = getDirecTipoVar(temporal)
			temporal = pilaVar.pop()
			izq = getDireccionMem(temporal)
			tipoizq = getDirecTipoVar(temporal)
			resultado = getCubeType(tipoizq, tipoDere, op)
			if resultado == Type.ERROR:
				print("Error de sintaxis en comparaciones")
				sys.exit()
			dire = getDirecTemporales(resultado)
			funciones[scope].varTable.append(Var(varT, resultado, dire,None))
			cuadruplos.append(cuadruplo(len(cuadruplos), op, izq, dere , dire))
			pilaVar.append(varT)
			temporalContador = temporalContador + 1


def p_AgregaCuadComp(p):
	'AgregaCuadComp : '
	if len(pilaOpp)> 0:
		global temporalContador
		if pilaOpp[len(pilaOpp)-1] == '<' or pilaOpp[len(pilaOpp)-1] == '>'  or pilaOpp[len(pilaOpp)-1] == '<=' or pilaOpp[len(pilaOpp)-1] == '=>' or pilaOpp[len(pilaOpp)-1] == '==' or pilaOpp[len(pilaOpp)-1] == '!=':
			op = pilaOpp.pop()
			temporal = pilaVar.pop()
			varT = "t" + str(temporalContador)
			dere = getDireccionMem(temporal)
			tipoDere = getDirecTipoVar(temporal)
			temporal = pilaVar.pop()
			izq = getDireccionMem(temporal)
			tipoizq = getDirecTipoVar(temporal)
			resultado = getCubeType(tipoizq, tipoDere, op)
			if resultado == Type.ERROR:
				print("Error de sintaxis en comparaciones")
				sys.exit()
			dire = getDirecTemporales(resultado)
			funciones[scope].varTable.append(Var(varT, resultado, dire,None))
			cuadruplos.append(cuadruplo(len(cuadruplos), op, izq, dere , dire))
			pilaVar.append(varT)
			temporalContador = temporalContador + 1


########################## CUADRUPLOS ARITMETICOS ################################

def p_AgregaCuadSR(p):
	'AgregaCuadSR : '
	if len(pilaOpp)> 0:
		global temporalContador
		if pilaOpp[len(pilaOpp)-1] == '+' or pilaOpp[len(pilaOpp)-1] == '-':
			op = pilaOpp.pop()
			temporal = pilaVar.pop()
			varT = "t" + str(temporalContador)
			dere = getDireccionMem(temporal)
			tipoDere = getDirecTipoVar(temporal)
			temporal = pilaVar.pop()
			izq = getDireccionMem(temporal)
			tipoizq = getDirecTipoVar(temporal)
			resultado = getCubeType(tipoizq, tipoDere, op)
			if resultado == Type.ERROR:
				print("Error de sintaxis en comparaciones")
				sys.exit()
			dire = getDirecTemporales(resultado)
			funciones[scope].varTable.append(Var(varT, resultado, dire,None))
			cuadruplos.append(cuadruplo(len(cuadruplos), op, izq, dere , dire))
			pilaVar.append(varT)
			temporalContador = temporalContador + 1

def p_AgregaCuadMD(p):
	'AgregaCuadMD : '
	if len(pilaOpp)> 0:
		global temporalContador
		if pilaOpp[len(pilaOpp)-1] == '*' or pilaOpp[len(pilaOpp)-1] == '/' or pilaOpp[len(pilaOpp)-1] == '%':
			op = pilaOpp.pop()
			temporal = pilaVar.pop()
			varT = "t" + str(temporalContador)
			dere = getDireccionMem(temporal)
			tipoDere = getDirecTipoVar(temporal)
			temporal = pilaVar.pop()
			izq = getDireccionMem(temporal)
			tipoizq = getDirecTipoVar(temporal)
			resultado = getCubeType(tipoizq, tipoDere, op)
			if resultado == Type.ERROR:
				print("Error de sintaxis en comparaciones")
				sys.exit()
			dire = getDirecTemporales(resultado)
			funciones[scope].varTable.append(Var(varT, resultado, dire,None))
			cuadruplos.append(cuadruplo(len(cuadruplos), op, izq, dere , dire))
			pilaVar.append(varT)
			temporalContador = temporalContador + 1

def p_AgregaCuadPow(p):
	'AgregaCuadPow : '
	if len(pilaOpp)> 0:
		global temporalContador
		if pilaOpp[len(pilaOpp)-1] == '^' :
			op = pilaOpp.pop()
			temporal = pilaVar.pop()
			varT = "t" + str(temporalContador)
			dere = getDireccionMem(temporal)
			tipoDere = getDirecTipoVar(temporal)
			temporal = pilaVar.pop()
			izq = getDireccionMem(temporal)
			tipoizq = getDirecTipoVar(temporal)
			resultado = getCubeType(tipoizq, tipoDere, op)
			if resultado == Type.ERROR:
				print("Error de sintaxis en comparaciones")
				sys.exit()
			dire = getDirecTemporales(resultado)
			funciones[scope].varTable.append(Var(varT, resultado, dire,None))
			cuadruplos.append(cuadruplo(len(cuadruplos), op, izq, dere , dire))
			pilaVar.append(varT)
			temporalContador = temporalContador + 1


def p_AgregaCuadIgual(p):
	'AgregaCuadIgual : '
	ID = p[-6]
	if len(pilaOpp)> 0:
		if pilaOpp[len(pilaOpp)-1] == '=' :
			tmp1 = pilaVar.pop()
			variable1 = getDireccionMem(tmp1)
			tipo1 = getDirecTipoVar(tmp1)
			asigna = getDireccionMem(ID)
			tipo2 = getDirecTipoVar(ID)
			Opp = pilaOpp.pop()
			sintaxis = getCubeType(tipo1, tipo2, Opp)
			if sintaxis == Type.ERROR:
				print ("Error de sintaxis")
				sys.exit()
			cuadruplos.append(cuadruplo(len(cuadruplos), Opp,variable1, None , asigna))


# Cuadruplo para asignaciones de arreglos
def p_CuadruploAsignaARR(p):
    'cuadruploAsignaArr : empty'
    ID = p[-6]
    if len(pilaOpp)> 0:
        if pilaOpp[len(pilaOpp)-1] == '=' :
            temporal = pilaVar.pop()
            dirVariable = getDireccionMem(temporal)
            dirTipo1 = getDirecTipoVar(temporal)
            asigna = getDireccionMem(ID)
            dirTipo2 = getDirecTipoVar(ID)
            operador = pilaOpp.pop()
            sintaxis = getCubeType(dirTipo1, dirTipo2, operador)
            if sintaxis == Type.ERROR:
                print ("Error de sintaxis")
                sys.exit()
            cuadruplos.append(cuadruplo(len(cuadruplos), 'Ver', 0, int(getDimensionVar(p[-6]))-1, getDireccionMem(p[-5])))
            global temporalContador
            numTemporal = "t" + str(temporalContador)
            pilaVar.append(numTemporal)
            temporalContador = temporalContador + 1
            dirArr = getDirecTempArr("INT")

            funciones[scope].varTable.append(Var(numTemporal, 'INT', dirArr, None))
            cuadruplos.append(cuadruplo(len(cuadruplos), '+ARR' ,getDireccionMem(p[-7]), getDireccionMem(p[-5]), getDireccionMem(numTemporal)))
            cuadruplos.append(cuadruplo(len(cuadruplos), '=', dirVariable, None,  getDireccionMem(numTemporal)))

def p_AgregaCuadWrite(p):
	'AgregaCuadWrite : '
	ID = p[-1]
	dirID = getDireccionMem(ID)
	cuadruplos.append(cuadruplo(len(cuadruplos), 'Write',dirID, None , None))


def p_AgregaCuadRead(p):
	'AgregaCuadRead : '
	ID = p[-1]
	dirID = getDireccionMem(ID)
	cuadruplos.append(cuadruplo(len(cuadruplos), 'Read',dirID, None , None))

def p_AgregaCuadRet(p):
	'AgregaCuadRet : '
	ID = p[-1]
	dirID = getDireccionMem(ID)
	cuadruplos.append(cuadruplo(len(cuadruplos), 'Return',dirID, None , None))

def p_IfQuad1(p):
	'IfQuad1 : '
	pilaSaltos.append(len(cuadruplos))
	cuadruplos.append(cuadruplo(len(cuadruplos), "GotoF", getDireccionMem(pilaVar.pop()), None, None))

def p_IfQuad2(p):
	'IfQuad2 : '
	idx = pilaSaltos.pop()
	pilaSaltos.append(len(cuadruplos))
	cuadruplos.append(cuadruplo(len(cuadruplos), "Goto", None, None, None))
	cuadruplos[idx].var3 = len(cuadruplos)

def p_IfQuad3(p):
	'IfQuad3 : '
	idx = pilaSaltos.pop()
	cuadruplos[idx].var3 = len(cuadruplos)

# guardar indice de cuadruplo donde se empieza la condicion del while
def p_WhileQuad1(p):
	'WhileQuad1 : '
	idx = pilaSaltos.pop()
	cuadruplos[idx].var3 = len(cuadruplos)

# guardar indice de cuadruplo del GotoF
def p_WhileQuad2(p):
	'WhileQuad2 : '
	pilaSaltos.append(len(cuadruplos))
	cuadruplos.append(cuadruplo(len(cuadruplos), "GotoF", getDireccionMem(pilaVar.pop()), None, None))

def p_WhileQuad3(p):
	'WhileQuad3 : '
	idx = pilaSaltos.pop()
	pilaSaltos.append(len(cuadruplos))
	cuadruplos.append(cuadruplo(len(cuadruplos), "Goto", None, None, None))
	cuadruplos[idx].var3 = len(cuadruplos)

# obtiene parametros
def p_paramCuadruplo(p):
	'''paramCuadruplo : '''
	ID = p[-1]
	global parametrosNum
	parametroVal = getDireccionMem(ID)
	paramActual = "param" + str(parametrosNum)
	parametrosNum += 1
	cuadruplos.append(cuadruplo(len(cuadruplos), 'Param',parametroVal, None , paramActual))

def p_eraCuadruplo(p):
	'''eraCuadruplo : '''
	#ID = p[-1]
	global parametrosNum
	#funcionesAll = list(map(lambda x: x.id,funciones))
	#if ID in funcionesAll:
	cuadruplos.append(cuadruplo(len(cuadruplos), 'Era',getFunctionById(p[-1]).dir, None , None))
	parametrosNum = 1
	#else:
	#	print(str(ID)+' no esta definida')

def p_goSubCuadruplo(p):
	'''goSubCuadruplo : '''
	ID = p[-6]
	global parametrosNum
	cuadruplos.append(cuadruplo(len(cuadruplos), 'Gosub',getFunctionById(p[-6]).dir, None , None))
	parametrosNum = 1


########################## CUADRUPLOS FIGURAS ################################
def p_circuloCuad(p):
    ' circuloCuad : '
    radio = getDireccionMem(p[-7])
    width = getDireccionMem(p[-5])
    color = getDireccionMem(p[-3])
    cuadruplos.append(cuadruplo(len(cuadruplos), 'Circulo', radio, width, color))

def p_rectanguloCuad(p):
    ' rectanguloCuad : '
    largo = getDireccionMem(p[-7])
    alto = getDireccionMem(p[-5])
    color = getDireccionMem(p[-3])
    cuadruplos.append(cuadruplo(len(cuadruplos), 'Rectangulo', largo , alto , color))

def p_espiralCuad(p):
    ' espiralCuad : '
    rango = getDireccionMem(p[-7])
    angulo = getDireccionMem(p[-5])
    color = getDireccionMem(p[-3])
    cuadruplos.append(cuadruplo(len(cuadruplos), 'Espiral', rango , angulo , color))

def p_estrellaCuad(p):
    ' estrellaCuad : '
    vertices = getDireccionMem(p[-7])
    step = getDireccionMem(p[-5])
    largo = getDireccionMem(p[-3])
    #color = getDireccionMem(p[-2])
    cuadruplos.append(cuadruplo(len(cuadruplos), 'Estrella', vertices, step, largo))
    #cuadruplos.append(cuadruplo(len(cuadruplos), 'estrella2', color, None, None, None))



# FUNCIONES BUSQUEDA
def getFuncion(ID):
	funcionesAll = list(map(lambda x: x.id , funciones))
	idFuncion = funcionesAll.index(ID)
	if idFuncion >= 0:
		return funciones[idFuncion]

# FUNCS DIRECCIONES DE MEMORIA
def setDireccionMem(varType, globalI, globalFloat , globalBool , localInt , localFloat , localBool):
	global scope, gInt , gFloat , gBool , lInt , lFloat , lBool
	global scope
	iniDir =  0
	if (scope == 1):
	    if (varType == 'INT'):
	        iniDir = 5500 + globalI
	        gInt = gInt +1
	    elif (varType == 'FLOAT'):
	        iniDir = 6500 + globalFloat
	        gFloat = gFloat +1
	    elif (varType == 'BOOL'):
	        iniDir = 7500 + globalBool
	        gBool= gBool +1
	else:
	    if (varType == 'INT'):
	        iniDir = 8500 + localInt
	        lInt = lInt +1
	    elif (varType == 'FLOAT'):
	        iniDir = 9500+ localFloat
	        localFloat = lFloat +1
	    elif (varType == 'BOOL'):
	        iniDir = 10500 + localBool
	        lBool = lBool +1
	return iniDir


def getDireccionMem(ID):
	varLocales = list(map(lambda x: x.id ,funciones[scope].varTable))
	varGlobales = list(map(lambda x: x.id ,funciones[1].varTable))
	varConstant = list(map(lambda x: x.id ,funciones[0].varTable))
	if ID in varLocales:
		idT = varLocales.index(ID)
		return funciones[scope].varTable[idT].dir
	elif ID in varGlobales:
	    idT  = varGlobales.index(ID)
	    return funciones[1].varTable[idT].dir
	elif ID in varConstant:
		idT = varConstant.index(ID)
		return funciones[0].varTable[idT].dir
	return False

def getDirecTipoVar(ID):
	varLocales = list(map(lambda x: x.id ,funciones[scope].varTable))
	varGlobales = list(map(lambda x: x.id ,funciones[1].varTable))
	varConstant = list(map(lambda x: x.id ,funciones[0].varTable))
	if ID in varLocales:
		idx = varLocales.index(ID)
		return funciones[scope].varTable[idx].type
	elif ID in varGlobales:
		idx = varGlobales.index(ID)
		return funciones[1].varTable[idx].type
	elif ID in varConstant:
		idx = varConstant.index(ID)
		return funciones[0].varTable[idx].type
	return False

def getDirecTemporales(varType):
    DireTemp = 0
    global tmpInt, tmpFloat, tmpBool
    if(varType == 'INT'):
        DireTemp = 11500 + tmpInt
        tmpInt += 1
    elif(varType == 'FLOAT'):
        DireTemp = 12500 + tmpFloat
        tmpFloat += 1
    elif(varType == 'BOOL'):
        DireTemp = 13500 + tmpBool
        tmpBool += 1
    return DireTemp

def getDirecConstantes(varType):
    DireTemp = 0
    global cInt,cFloat,cBool
    if(varType == 'INT'):
        DireTemp = 14500 + cInt
        cInt += 1
    elif(varType == 'FLOAT'):
        DireTemp = 15500 + cFloat
        cFloat += 1
    elif(varType == 'BOOL'):
        DireTemp = 16500 + cBool
        cBool += 1
    return DireTemp

def getDirecTempArr(varType):
    direcTempArr = 0
    global tmpIntArr,tmpFloatArr,tmpBoolArr
    if(varType == 'INT'):
        direcTempArr = 17500 + tmpIntArr
        tmpIntArr += 1
    elif(varType == 'FLOAT'):
        direcTempArr = 18500 + tmpFloatArr
        tmpFloatArr += 1
    elif(varType == 'BOOL'):
        direcTempArr = 19500 + tmpBoolArr
        tmpBoolArr += 1
    return direcTempArr

def getFunctionById(ID):
    fNombres = list(map(lambda x: x.id , funciones))
    idx = fNombres.index(ID)
    if idx >= 0:
        return funciones[idx]

def p_empty(p):
    'empty : '


def p_error(p):
    global aprobado
    aprobado = False
    print("Error de sintaxis en '%s'" % p.value)
    sys.exit()

parser = yacc.yacc()

archivo = sys.argv[1]
f = open(archivo, 'r')
s = f.read()
parser.parse(s)

func = directorioFunciones()
func.funciones = funciones

maquina = maquinavirtual(func, cuadruplos)
maquina.run(0,'END')

if aprobado == True:

	print("Archivo aprobado")
	print ("\nCuadruplos:")
	for i in range(0, len(cuadruplos)):
		print(str(cuadruplos[i]))

	sys.exit()
else:
    print("Archivo no aprobado")
    sys.exit()
