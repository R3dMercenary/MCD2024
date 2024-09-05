## Problema 1

def prob_1(cadena):
    if type(cadena)==type(2):
        if (cadena<10)and(cadena>=0) :
            print(f"La cadena se conforma de un solo digito")
        else:
            print(f"La cadena no se conforma de un solo digito")
    elif type(cadena)==type("str"):
        if len(cadena)==1:
            if int(cadena[0]):
                print(f"La cadena se conforma de un solo digito")
        else:
            print(f"La cadena no se conforma de un solo digito")
    else:
        print(f"La cadena no se conforma de un solo digito")
    

## Problema 2

def prob_2(cadena,memoria=[],caracter=0):
    
    try:
        if int(cadena):
            print("La cadena se constituye de solo digitos")               
    except Exception as e:
        print("La cadena no se constituye de solo digitos") 
           
    
## Problema 3

def prob_3():
    import random
    resultado=random.randint(0,9)
    return resultado

## Problema 4

def prob_4(numero_digitos,resultado=""):
    print(len(resultado),resultado)
    import random
    if len(resultado)<numero_digitos:
        digito_al=random.randint(0,9)
        resultado_alterado=resultado+str(digito_al)
        prob_4(numero_digitos,resultado_alterado)
    
    return resultado

## Problema 5
def prob_5(cadena_1,cadena_2,distancia={'distancia':0},indice=0):
    if (len(cadena_1)==len(cadena_2)) and (indice<=len(cadena_1)):
        if indice!=len(cadena_1):
          
            if cadena_1[indice]==cadena_2[indice]:
                distancia['distancia']+=1
                
        elif indice==len(cadena_1):
            if cadena_1[indice-1]==cadena_2[indice-1]:
                distancia['distancia']+=1
                

        indice+=1
        prob_5(cadena_1,cadena_2,distancia,indice)
    return distancia['distancia']

## Problema 6
def prob_6(cadena):
    import random
    pos=random.randint(0,len(cadena))
    if pos==len(cadena):
        resultado=cadena[:pos]+str(random.randint(0,9))
    else:
        resultado=cadena[:pos]+str(random.randint(0,9))+cadena[pos+1:]
    
    return resultado

## Problema 7
def prob_7(cadena,usadas=[],resultado="",memoria=[]):
    import random
    memoria.append(cadena)
    if len(usadas)<2:
        digito=str(random.randint(0,9))
        pos=random.randint(0,len(cadena))
        if pos in usadas:
            prob_7(cadena,usadas)
        elif pos==len(cadena):
            
            if (digito==cadena[pos-1])or (digito==memoria[0][pos-1]):
                prob_7(cadena,usadas)
            else:
                resultado=cadena[:pos]+digito
                usadas.append(pos)
                prob_7(resultado,usadas,memoria=memoria)
        else:

            if (digito==cadena[pos])or(digito==memoria[0][pos]):
                prob_7(cadena,usadas)
            else:
                resultado=cadena[:pos]+digito+cadena[pos+1:]
                usadas.append(pos)
                prob_7(resultado,usadas,memoria=memoria)
        
        print("ok",resultado,usadas,memoria)    
    return memoria[-1]

    ## Problema 8
def prob_8(cadena,usadas=[],resultado="",memoria=[]):
    import random
    memoria.append(cadena)
    if len(usadas)<3:
        digito=str(random.randint(0,9))
        pos=random.randint(0,len(cadena))
        if pos in usadas:
            prob_8(cadena,usadas)
        elif pos==len(cadena):
            
            if (digito==cadena[pos-1])or (digito==memoria[0][pos-1]):
                prob_8(cadena,usadas)
            else:
                resultado=cadena[:pos]+digito
                usadas.append(pos)
                prob_8(resultado,usadas,memoria=memoria)
        else:

            if (digito==cadena[pos])or(digito==memoria[0][pos]):
                prob_8(cadena,usadas)
            else:
                resultado=cadena[:pos]+digito+cadena[pos+1:]
                usadas.append(pos)
                prob_8(resultado,usadas,memoria=memoria)
        
        print("ok",resultado,usadas,memoria)    
    return memoria[-1]

## Problema 9
    
def prob_9(cadena,n,usadas=[],resultado="",memoria=[]):
    import random
    memoria.append(cadena)
    if len(usadas)<n:
        digito=str(random.randint(0,9))
        pos=random.randint(0,len(cadena))
        if pos in usadas:
            prob_9(cadena,n,usadas)
        elif pos==len(cadena):
            if (digito==cadena[pos-1])or(digito==memoria[0][pos-1]):
                prob_9(cadena,n,usadas)
            else:
                resultado=cadena[:pos]+digito
                usadas.append(pos)
                prob_9(resultado,n,usadas,memoria=memoria)
        else:

            if (digito==cadena[pos])or(digito==memoria[0][pos]):
                prob_9(cadena,n,usadas)
            else:

                resultado=cadena[:pos]+digito+cadena[pos+1:]
                if resultado not in memoria:
                    usadas.append(pos)
                    prob_9(resultado,n,usadas,memoria=memoria)
        
        print("ok",resultado,usadas,memoria)    
    return memoria[-1]