# Cómo se configura la API

Tenemos el URL del host de la API:
```
API_HOST="https://versionpublicarnpdno.segob.gob.mx/"
``` 
Y algunas raíces y endpoints utíles:

```
API_SOCIODEMOGRAFICOS_ROOT = "Sociodemografico/"
API_CATALAGO_ROOT = "Catalogo/"

ENDPOINT_CATALOGO_EDO = "Estados/"
ENDPOINT_CATALOGO_MUN = "Municipios/"
ENDPOINT_CATALOGO_COL = "Colonias/"
``` 

Luego, tenemos que hacer los siguientes requests para obtener las cookies apropiadas:
```
main_session = requests.Session()
main_session.get("https://versionpublicarnpdno.segob.gob.mx/Dashboard/Index")
main_session.get("https://versionpublicarnpdno.segob.gob.mx/Dashboard/ContextoGeneral")
```
Ahora sí podemos utilizar la API:

```
TARGET_URL=API_HOST+<raíz de api de interes>+< endpoint de informacion de interes >
```
Para ver que informacion se puede extraer, probemos con el siguiente endpoint:

```
TARGET_URL=API_HOST

r=main.session.get(TARGET_URL)
content=r.json()
```

Construiremos una función que permita hacer requests y que regrese una tabla del request:

```
def API_GET(endpoint,DATA=None):
    #Modulos importantes
    import os
    import sys
    import requests
    import datetime

    import pandas as pd
    import json

    API_HOST = "https://versionpublicarnpdno.segob.gob.mx/"
    

# Before doing anything, we must make a dummy request to the index in order to get the propper cookies
    main_session = requests.Session()
    main_session.get(f"{API_HOST}Dashboard/Index")
    main_session.get(f"{API_HOST}Dashboard/ContextoGeneral")

    r=main_session.post(API_HOST+endpoint,data=DATA)

    return pd.json_normalize(r.json(),)
```

Parece ser que es necesario insertar un endpoint, la pura raíz no nos deja hacer el request. 
# Ejercicios
## Ejercicio 1

Ahora sí, veamos como poder responder la pregunta: "¿Como podríamos consultar las estadísticas sobre mujeres desaparecidas en el municipio de Cajeme?"

Para poder obtener las estas estadísticas, primero configuramos los datos:
```
DATA = {
  "titulo":"",
  "subtitulo": "",
  "idEstatusVictima":"0",
  "idHipotesisNoLocalizacion":"0",
  "idEstado":"26", 
  "idMunicipio":"18",# Se cambia al id de Cajeme
  "idColonia":"0",
  "fechaInicio":"",
  "fechaFin":"",
  "mostrarFechaNula":"0",
  "edadInicio":"",
  "edadFin":"",
  "mostrarEdadNula":"0",
  "idNacionalidad":"0",
  "idHipotesis":"",
  "idMedioConocimiento":"",
  "idCircunstancia":"",
  "tieneDisc`pacidad":"",
  "idTipoDiscapacidad":"0",
  "idEtnia":"0",
  "idLengua":"0",
  "idReligion":"",
  "esMigrante":"",
  "idEstatusMigratorio":"0",
  "esLgbttti":"",
  "esServidorPublico":"",
  "esDefensorDH":"",
  "esPeriodista":"",
  "esSindicalista":"",
  "esONG":"",
  "idDelito":"0"
}
```

Y ahora, intentamos con el endpoint API_SOCIODEOGRAFICOS_ROOT+"Mujeres" a ver si funciona. No funciona, intentaremos con "Mujer". Parece que no existen estos endpoints. Estoy revisando el manual de uso "https://comisionacionaldebusqueda.gob.mx/wp-content/uploads/2022/12/Instructivo-Version-Publica-RNPDNO-V1.pdf" y parece ser que la unica manera de consultar información de sexo es a traves de los endpoints asociados a las gráficas: "BarChartSexoColonia" y "AreaChartSexoAnio".

Para ello, intentaremos con la siguiente forma de datos pero con el endpoint BarChartSexoColonia:

```
import pandas as pd
import json
import sys
import requests
import datetime

import pandas as pd
import json


API_HOST = "https://versionpublicarnpdno.segob.gob.mx/"
    

# Before doing anything, we must make a dummy request to the index in order to get the propper cookies
main_session = requests.Session()
main_session.get(f"{API_HOST}Dashboard/Index")
main_session.get(f"{API_HOST}Dashboard/ContextoGeneral")
TARGET_URL = API_HOST + API_SOCIODEOGRAFICOS_ROOT + "BarChartSexoColonia"

DATA = {
  "titulo":"PERSONAS DESAPARECIDAS, NO LOCALIZADAS Y LOCALIZADAS",
  "subtitulo":"POR COLONIAS - CAJEME",
  "idEstado":"26",
  "idMunicipio":"18",## Id de cajeme
  "idColonia":"0",
  "idEstatusVictima":"0",
  "idHipotesisNoLocalizacion":"0",
  "idDelito":"0",
  "fechaInicio":"",
  "fechaFin":"",
  "mostrarFechaNula":"0",
  "idNacionalidad":"0",
  "edadInicio":"",
  "edadFin":"",
  "mostrarEdadNula":"0",
  "idHipotesis":"",
  "idMedioConocimiento":"",
  "idCircunstancia":"",
  "tieneDiscapacidad":"",
  "idTipoDiscapacidad":"0",
  "idEtnia":"0",
  "idLengua":"0",
  "idReligion":"",
  "esMigrante":"",
  "idEstatusMigratorio":"0",
  "esLgbttti":"",
  "esServidorPublico":"",
  "esDefensorDH":"",
  "esPeriodista":"",
  "esSindicalista":"",
  "esONG":"",
}

r = main_session.post(TARGET_URL, json = DATA)

res = r.json()
datos = {serie['name']: serie['data'] for serie in res['Series']}
datos['Colonia'] = res['XAxisCategories']
por_colonia = pd.DataFrame(datos)
por_colonia.index = por_colonia.Colonia

por_colonia
```

Funcionó, seguimos con la siguiente pregunta.

## Ejercicio 2:¿Como podemos sacar lo que pasa en todo el estado, por municipios y por colonias?

Tengo la idea de que se puede analizar tablas por sexo y se escoge un estado en particular, donde las columnas pueden ser las colonias y las filas los municipios. 

La estrategia va ser la siguiente:
    Por cada municipio, extraer una tabla con las colonias como fila y las columnas "Hombre,Mujer,Indeterminado,Municipio"
    Concatenar tablas

La funcion final quedó de la forma:

```
def por_estado(estado="SONORA"):

    import pandas as pd
    import json
    import sys
    import requests
    import datetime

    import pandas as pd
    import json



## Aquí se obtiene el id del estado de interes
    estados_id=API_GET(API_CATALAGO_ROOT + ENDPOINT_CATALOGO_EDO)
    estados_id.columns = ['Valor', 'Estado']
    id_estado=estados_id[estados_id['Estado']==estado]

## Aquí se obtiene el id del municipio de interes
    municipios=API_GET(API_CATALAGO_ROOT+ENDPOINT_CATALOGO_MUN,{"idEstado":id_estado['Valor'].iloc[0]})
    municipios.columns = ['Valor', 'Municipio']
    
    resultado=pd.DataFrame()
    for municipio in municipios['Municipio'].unique()[1:]:
        print(municipio)
        df=por_municipio(estado,municipio)
        resultado=pd.concat([resultado, df], axis=0)
   

    return resultado

```

## Ejercicio 3:¿Se puede hacer por municipio? ¿En forma programática? ¿Para algun caso especial?

Al parecer, al hacer esta modificación a la configuración del API nos arroja estadísticas de gente desaparecida por año por municipio sin problema:

```
def por_municipio_anio(estado="SONORA",municipio="HERMOSILLO"):

    import pandas as pd
    import json
    import sys
    import requests
    import datetime

    import pandas as pd
    import json



## Aquí se obtiene el id del estado de interes
    estados_id=API_GET(API_CATALAGO_ROOT + ENDPOINT_CATALOGO_EDO)
    estados_id.columns = ['Valor', 'Estado']
    id_estado=estados_id[estados_id['Estado']==estado]

## Aquí se obtiene el id del municipio de interes
    municipios=API_GET(API_CATALAGO_ROOT+ENDPOINT_CATALOGO_MUN,{"idEstado": "26"})
    municipios.columns = ['Valor', 'Municipio']
    id_municipio=municipios[municipios['Municipio']==municipio]


    API_HOST = "https://versionpublicarnpdno.segob.gob.mx/"
    

# Before doing anything, we must make a dummy request to the index in order to get the propper cookies
    main_session = requests.Session()
    main_session.get(f"{API_HOST}Dashboard/Index")
    main_session.get(f"{API_HOST}Dashboard/ContextoGeneral")
    TARGET_URL = API_HOST + API_SOCIODEOGRAFICOS_ROOT + "AreaChartSexoAnio"


    DATA = {
    "titulo":"PERSONAS DESAPARECIDAS, NO LOCALIZADAS Y LOCALIZADAS",
    "subtitulo":f"POR AÑO EN EL ESTADO DE {estado}",
    "idEstado":f"{id_estado['Valor'].iloc[0]}",
    "idMunicipio":f"{id_municipio['Valor'].iloc[0]}",## Municipio de interes
    "idColonia":"0",# Todas las colonias
    "idEstatusVictima":"0",
    "idHipotesisNoLocalizacion":"0",
    "idDelito":"0",
    "fechaInicio":"",
    "fechaFin":"",
    "mostrarFechaNula":"0",
    "idNacionalidad":"0",
    "edadInicio":"",
    "edadFin":"",
    "mostrarEdadNula":"0",
    "idHipotesis":"",
    "idMedioConocimiento":"",
    "idCircunstancia":"",
    "tieneDiscapacidad":"",
    "idTipoDiscapacidad":"0",
    "idEtnia":"0",
    "idLengua":"0",
    "idReligion":"",
    "esMigrante":"",
    "idEstatusMigratorio":"0",
    "esLgbttti":"",
    "esServidorPublico":"",
    "esDefensorDH":"",
    "esPeriodista":"",
    "esSindicalista":"",
    "esONG":"",
    }

    r = main_session.post(TARGET_URL, json = DATA)

    res = r.json()
    datos = {serie['name']: serie['data'] for serie in res['Series']}
    datos['Fecha'] = res['XAxisCategories']
    por_fecha = pd.DataFrame(datos)

    por_fecha['Fecha'] = pd.to_numeric(por_fecha.Fecha, errors='coerce')
    por_fecha.index = por_fecha.Fecha
    por_fecha=por_fecha.drop('Fecha',axis=1)
    por_fecha['Municipio']=municipio
    return por_fecha

```

## Ejercicio 4:Extrae alguna información del conjunto de datos que pienses que es relevante, y explica porqué.

A mi me llaman la atencion los campos "esPeriodista","esDefensorDH","esServidorPublico" . Tal vez sea interesante consultar información de los desaparecidos local,(Hermosillo,Sonora), y ver las desapariciones por año. También sería bueno identificar los valores de "idDelito"

## Investigación de APIs

Primero,voy a explorar el código fuente de la página:https://versionpublicarnpdno.segob.gob.mx/Dashboard/ContextoGeneral

Al ver el código fuente de la página :
https://versionpublicarnpdno.segob.gob.mx/Dashboard/Sociodemografico

Logré encontrar lo siguiente:
```
<div class="col-md-4">
                    <div class="form-group">
                        <label class="control-label" for="cboEstatus">Estatus de la persona</label>
                        <select id="cboEstatus" name="cboEstatus" class="form-control black-options" required>
                            <option value="0" selected>PERSONAS DESAPARECIDAS, NO LOCALIZADAS Y LOCALIZADAS</option>
                            <option value="7">PERSONAS DESAPARECIDAS Y NO LOCALIZADAS</option>
                            <option value="4">PERSONAS DESAPARECIDAS</option>
                            <option value="5">PERSONAS NO LOCALIZADAS</option>
                            <option value="6">PERSONAS LOCALIZADAS</option>
                            <option value="2">PERSONAS LOCALIZADAS CON VIDA</option>
                            <option value="3">PERSONAS LOCALIZADAS SIN VIDA</option>
                        </select>
                    </div>
                </div>



