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
    cnt=0
    aux,sal=[],[]
    #Elimina primero y último paréntesis
    l.pop(len(l)-1)
    l.pop(0)
    #Separa los elementos en la lista basándose en el numero de paréntesis
    for i in l:
        if i == '(': cnt+=1
        elif i== ')': cnt-=1
        aux.append(i)
        if cnt==0:
            sal.append(aux)
            aux=[]
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
    if len(fp)==1:
        if fp[0].lower()=='true': return True
        if fp[0].lower()=='false': return False
        return dic_elem[fp[0]]
    elem=idenElem(fp)
    #Si es operador binario
    if(len(elem)==3):
        if elem[1][0]=='=>':
            val= not evalua(elem[0],dic_elem,dic_op) or evalua(elem[2],dic_elem,dic_op)
        elif elem[1][0]=='<=>':
            val1= evalua(elem[0],dic_elem,dic_op)
            val2= evalua(elem[2],dic_elem,dic_op)
            val= (not val1 or val2) and (not val2 or val1)
        else:
            val = eval(str(evalua(elem[0],dic_elem,dic_op))+dic_op[elem[1][0]]+str(evalua(elem[2],dic_elem,dic_op)))
    #Si es unario
    elif(len(elem)==2):
        val = eval(dic_op[elem[0][0]]+str(evalua(elem[1],dic_elem,dic_op)))
    return val

def create_dic_elem(n_elem, variable_names, dic_elem):
    """
    Funcion que nos regresa un diccionario con una combinación de valores
    de las variables de la preposición compuesta dada por la cadena n_elem

    Por ejemplo si n_elem = "1000" para las variables [p,q,r,b]
    entonces la combinación para 4 variables sería:
    {'p': True, 'q': False, 'r': True, 'b': False}
    Args:
        dic_elem: pasamos la referencia de un diccionario para agregarle valores
        n_elem: cadena que nos dice una combinación que se quiere de las variables
        variable_names: lista que contiene los nombres de las variables
        de la preposicón compuesta
    Returns:
        diccionario con una combinación de valores que fue dada
    """
    count = 0
    for i in list(n_elem):
        if i != "0" :
            dic_elem[variable_names[count]] = True
        else:
            dic_elem[variable_names[count]] = False
        count+=1
    print("para " + str(dic_elem) + "\n")
    return dic_elem

def main():
    """
        Funcion que pide las entradas del programa y nos arroja los resultados
    """
    dic_op={'|':' or ','&':' and ','!':'not '}

    print("dime la preposición compuesta")
    fp = input()
    print("dime el número de variables")
    n_variables = int(input())

    n_variables_1 = 0
    n_variable_true = False
    n_variable_false = False
    variable_names = []
    for i in range(n_variables):
        print("dime el nombre de la variable " + str(i+1))
        variable_names.append(input())
        #checar si true y false son variables
        if variable_names[i].lower() == 'true':
            n_variable_true = True
            variable_names[i] = variable_names[i].lower()
        elif variable_names[i].lower() == 'false':
            n_variable_false = True
            variable_names[i] = variable_names[i].lower()
        else:
            #contar el numero de variables que no son TRUE o FALSE
            n_variables_1 += 1

    dic_elementos = {}
    #si ambas son variables, agregarlas al diccionario
    #si no agregarlas individualmente
    if n_variable_false == True and n_variable_true == True:
        dic_elementos['true'] = True
        dic_elementos['false'] = False
    elif n_variable_false == True:
        dic_elementos['false'] = False
    elif n_variable_true == True:
        dic_elementos['true'] = True

    print("resultado")

    #si n_variables_1 es igual a cero, significa que la preposición tiene solo variables TRUE y FALSE
    if (n_variables_1 == 0):
        print("para " + str(dic_elementos) + "\n")
        print(evalua(fp.split(' '),dic_elementos, dic_op))
        return

    for i in range(2**n_variables_1):
        n_elem = bin(i)[2:].zfill(n_variables_1)
        lista=fp.split(' ')
        print(evalua(lista, create_dic_elem(n_elem, variable_names, dic_elementos), dic_op))

main()
