"""
	Programa que evalua preposiciones compuestas mediante el algoritmo de Dijkstra Recursivo

	Input:
		La preposición dada por consola, por ejemplo:
			( ( p | q ) <=> ( ! r ) )

		número de variables: para el ejemplo anterior son 3

		nombres de las variables: para el ejemplo anterior son "p", "q" y "r"
"""

def idenElem(l):
	"""
	Consigue las preposiciones atómicas que estan involucradas en la preposicion compuesta.
	Estas son separadas por los paréntesis

	Args:
		l: lista de los elementos de la preposición
	Returns:
		Es una lista que contiene las preposiciones atómicas
	"""
	cnt = 0
	aux,sal = [],[]
	#Elimina primero y último paréntesis
	l.pop(len(l) - 1)
	l.pop(0)
	#Separa los elementos en la lista basándose en el numero de paréntesis
	for i in l:
		if i == '(': cnt += 1
		elif i == ')': cnt -= 1
		aux.append(i)
		if cnt == 0:
			sal.append(aux)
			aux = []
	return sal

def evalua(fp, dic_elem, dic_op):
	"""
	Esta función obtiene el resultado de la preposición compuesta

	Va evaluando las preposiciones atómicas recursivamente y regresa su valor
	hasta evalular la preposición compuesta completamente

	Args:
		fp: lista de los elementos de la operación
		dic_elem: valores de las variables de la preposición compuesta
		dic_op: diccionario de operadores que contiene a "and", "or" y "not"
	Returns:
		Resultado de evaluar la preposición
	"""
	#Si es un sólo elemnto entonces lo retorna
	if len(fp) == 1:
		if fp[0].lower() == 'true': return True
		if fp[0].lower() == 'false': return False
		return dic_elem[fp[0]]
	elem = idenElem(fp)
	#Si es operador binario
	if(len(elem) == 3):
		if elem[1][0] == '=>':
			val = not evalua(elem[0], dic_elem, dic_op) or evalua(elem[2], dic_elem, dic_op)
		elif elem[1][0] == '<=>':
			val1 = evalua(elem[0], dic_elem, dic_op)
			val2 = evalua(elem[2], dic_elem, dic_op)
			val = (not val1 or val2) and (not val2 or val1)
		else:
			val = eval(str(evalua(elem[0], dic_elem, dic_op)) + dic_op[elem[1][0]] + str(evalua(elem[2], dic_elem, dic_op)))
	#Si es unario
	elif(len(elem) == 2):
		val = eval(dic_op[elem[0][0]] + str(evalua(elem[1], dic_elem, dic_op)))
	return val

def create_dic_elem(variable_names):
	"""
	Funcion que nos regresa un diccionario con una combinación de valores
	de las variables de la preposición compuesta dada por la cadena n_elem

	Por ejemplo si n_elem = "1000" para las variables [p,q,r,b]
	entonces la combinación para 4 variables sería:
	{'p': True, 'q': False, 'r': True, 'b': False}
	Args:
		n_elem: cadena que nos dice una combinación que se quiere de las variables
		variable_names: lista que contiene los nombres de las variables
		de la preposicón compuesta
	Returns:
		diccionario con una combinación de valores que fue dada
	"""
	dic_elem = {}
	for i in range(len(variable_names)):
		l = variable_names[i].split(' ')
		if l[1].lower() == 'true':
			dic_elem[l[0]] = bool(l[1])
		elif l[1].lower() == 'false':
			dic_elem[l[0]] = bool('')
		else:
			return dic_elem
	return dic_elem

def main():
	"""
		Funcion que pide las entradas del programa y nos arroja los resultados
	"""
	dic_op={'|':' or ','&':' and ','!':'not '}

	print("Dime la preposición compuesta separada por espacios y encerrada en paréntesis")
	fp = input()
	n_variables = int(input("\nDime el número de variables (las entradas True o False no cuentan como variables): "))

	variable_names = []
	for i in range(n_variables):
		print("\nDime el nombre de la variable " + str(i+1) + " y su valor (true o false) separados por un espacio: ")
		variable_names.append(input())

	print("\nResultado:")

	lista = fp.split(' ')
	try:
		print(evalua(lista, create_dic_elem(variable_names), dic_op))
	except:
		print("\nError inesperado: Revise la entrada de los datos.")
main()
