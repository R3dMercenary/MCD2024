# Modelado y evaluación
## 3 de septiembre 2024

Primero, descargaremos los datos del url "https://files.conagua.gob.mx/aguasnacionales/TODOS%20LOS%20MONITOREOS.xlsb" que se encuentra en la fuente de información "https://www.gob.mx/conagua/articulos/calidad-del-agua":

```
import pandas as pd
import urllib
import re
import copy

url="https://files.conagua.gob.mx/aguasnacionales/TODOS%20LOS%20MONITOREOS.xlsb"
temp_file=urllib.request.urlretrieve(url)

sitios=pd.read_excel(temp_file[0],sheet=0)
resultados=pd.read_excel(temp_file[0],sheet=1)
simbologia=pd.read_excel(temp_file[0],sheet=2)

backup_sitios=copy.deepcopy(sitios)
backup_resultados=copy.deepcopy(resultados)
backup_simbologia=copy.deepcopy(simbologia)

```

Se tardó 1 minuto con 41.4 segundos con mi conexión de internet de (64bytes)*139/138189 ms en ejecutarse la extracción del archivo. En total, la celda tardó 14 minutos con 12.6 segundos en ejecutarse.


La estrategia sera la siguiente:

    Identificar las columnas de las mediciones

    Identificar las columnas relacionadas con el tiempo

    Hacer el tratado y limpieza a las columnas de mediciones apoyandonos del notebook "contaminacion_superficial.ipynb"

    Buscar por otras inconsistencias en los datos:formato, valores extraños.

Luego, debemos identificar las columnas que solo tienen que ver con el estado de Sonora

Esto lo podemos lograr al descargar el archivo de los resultados en Sonora: "https://files.conagua.gob.mx/aguasnacionales/RESULTADOS-SONORA.xlsb"


En cuanto la identificación de columnas, nos apoyaremos del dataframe de "simbologia" Hay que identificar las columnas de los indicadores de agua superficial.

Estas vienen siendo(basandonos en la fuente de información):

 Demanda Bioquímica de Oxígeno a cinco días()
 Demanda Química de Oxígeno 
 Sólidos Suspendidos Totales  
 Coliformes fecales  
 Escherichia coli
 Enterococos fecales 
 porcentaje de saturación de Oxígeno Disuelto 
 Toxicidad aguda (TOX)

Claves relevantes apoyandonos del archivo "TODOS LOS MONITOREOS.xlsb"

```
superficial=resultados[
"TIPO CUERPO DE AGUA",
"Año",
"DBO_SOL",
"DBO_TOT",
"DQO_SOL",
"DQO_TOT",
"SST",
"COLI_FEC",
"E_COLI",
"ENTEROC_FEC",
"OD_%_SUP"
"TOX_D_48_SUP_UT",
"TOX_FIS_SUP_15_UT",
"TOX_FIS_SUP_30_UT",
"TOX_FIS_SUP_5_UT",
]

```

Ahora hay que filtrar por cuerpos que no son subterraneos: Lótico,léntico,costero.

## 4 de septiembre 2024

Aún no tenemos limpios nuestros datos, entonces me apoyaré de la libreta "contaminacion.ipynb". Encontré este snippet de código que puede ser útil:

```
columnas_mediciones=[
    'DBO_mg/L', 
    'DQO_mg/L',
    'SST_mg/L',
    'COLI_FEC_NMP_100mL',
    'E_COLI_NMP_100mL',
    'ENTEROC_NMP_100mL',
    'OD_PORC', 
    'OD_PORC_SUP', 
    'OD_PORC_MED', 
    'OD_PORC_FON',  
    'TOX_D_48_UT', 
    'TOX_V_15_UT',
    'TOX_D_48_SUP_UT',
    'TOX_D_48_FON_UT',
    'TOX_FIS_SUP_15_UT', 
    'TOX_FIS_FON_15_UT',]

concentraciones={}

for cuerpo in contaminada_B['CUERPO DE AGUA']:
    indeces=contaminada_B[contaminada_B['CUERPO DE AGUA']==cuerpo].index.tolist()
    agente={}
    for columna in columnas_mediciones:
        
        concentracion_acum=0
        for index in indeces:
            cantidad=contaminada_B[columna][index]
            if (type(cantidad)==type("hola")):
                expresion=re.search(r"<\d{1,2}",cantidad).group()
                numero_reemplazo=float(re.search(r"\d{1,2}",expresion).group())-0.1
                concentracion_acum+=numero_reemplazo
            elif pd.isnull(cantidad)==False:
                concentracion_acum+=cantidad
            else:
                continue

        agente[columna]=round(concentracion_acum/len(indeces),4)
    concentraciones[cuerpo]=agente

final_B=pd.DataFrame(concentraciones)
final_B

```

La parte que me interesa en partícular es:

```
for index in indeces:
            cantidad=contaminada_B[columna][index]
            if (type(cantidad)==type("hola")):
                expresion=re.search(r"<\d{1,2}",cantidad).group()
                numero_reemplazo=float(re.search(r"\d{1,2}",expresion).group())-0.1
                concentracion_acum+=numero_reemplazo
            elif pd.isnull(cantidad)==False:
                concentracion_acum+=cantidad
            else:
                continue

```

Esta parte del código es la responsable de limpiar las columnas, sólo tendría que verificar todos los tipos de valores que vienen guardados en cada columna.

```
for valor in superficial[columna]:
    if type(valor)==type("hola"):
        print(valor,type(valor))


```