def idenElem(l):
    """Consigue las operaciones que estan involucradas en la preposicion compuesta.
    Estas son separadas por los paréntesis

    Args:
        l: lista de los elementos de la operación
    Returns:
        Es una lista que contiene las operaciones las preposiciones atómicas con sus operandos
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
    hasta evalular la compuesta

    Args:
        fp: lista de los elementos de la operación
        dic_elem: valores de las variables de la preposición compuesta
        dic_op: diccionario de operadores que contiene a "and", "or" y "not"
    Returns:
        Resultado de evaluar la preposición
    """
    #Si es un sólo elemnto entonces lo retorna
    if len(fp)==1: return dic_elem[fp[0]]
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

fp='( ( p | q ) <=> ( ! r ) )'
#fp='r'
#dic_elem={'p':False,'q':True, 'r':True}
dic_op={'|':' or ','&':' and ','!':'not '}
lista=fp.split(' ')

for p in [True,False]:
    for q in [True,False]:
        for r in [True,False]:
            lista=fp.split(' ')
            #print(str(p),str(q) ,str(r))
            print(evalua(lista, {'p':p, 'q':q, 'r': r}, dic_op))

#print(evalua(lista,dic_elem,dic_op))
