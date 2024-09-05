#3 de septiembre 2024
https://mcd-unison.github.io/ing-caract/eda2/ 


*Nota:Hay que buscar, incluso en los casos de uso de fechas, que los indices de un dataframe sean unicos. Por eso hay que tener cuidado al utilizar fechas o timestamps como indices.*

pandas_datareader: biblioteca

Existe el método de "rolling.()" para calcular curvas de la media y promedio de una serie de datos

##Expresiones regulares

*Nota:Siempre es bueno asegurarse que una columna que viene guardada cómo tipo "Object" se le asigne el tipo adecuado, ya que luego se pueden prestar errores de conversión prevenibles.*

Se discute a fondo cómo funcionan los métodos de pandas actuando sobre una columna de un dataframe y algunas restricciones. Se aclaran algunos detalles acerca de cómo interpretar las columnas dentro de un dataframe de pandas(cómo series). También se aclaran dudas acerca de los formatos de datos que se pueden guardar/encontrar dentro de un dataframe. Siempre es buena práctica establecer/forzar el programa que aserte un formato esperado/deseado desde la incepción del dataframe para evitar arrastrar problemas.

*Nota:Es buena práctica en el diseño de bases de datos incluir el tipo de dato que debe tener el formato de la variable.Ejemplo <cuentaClabe_int64>*

Algunas expresiones regulares para tener en cuenta:

^:Inicio del string

.:Cualquier cosa

|:Or

[a-zA-Z0-9_]=\w:Cualquier caractér alfanúmerico y guión bajo
\W:Lo contrario a \w

Entonces, la siguiente expresión regular "^.p|roto" lee cómo "Cualquier string que inicie con 'p' o con 'roto'".Continuamos con otras expresiones.

[^<expresión>]:Cualquier cosa que no sea <expresión>

<expresión>?:Puede encontrarse <expresión> o no.(Es opcional encontrarlo o no)Ejemplo "colou?r" encuentra "color" y "colour"
<expresión>+:Puede encontrarse <expresión> de 1 a n veces.(Al menos uno o mas)
<expresión>*:Puede encontrarse <expresión> de 0 a n veces.(Puede estar, o puede estar muchas veces)

{<int>}: Se utilizan para decir cuántas veces se puede encontrar 
Ejemplo: La expresión regular de un correo eléctronico simple pudiese ser "[a-zA-Z0-9_]+@([a-zA-Z0-9_]+\.)+[A-Za-z]{2-4}"

\s:Cualquier caracter que represente un espacio
\S:Lo contrario a \s

*Nota:Por lo general, la biblioteca de re por default busca el patrón más grande.Por esto, es recomendado utilizar el método de .compile() del módulo de re para grandes consultas*

spaCy es una biblioteca de python bastante util para el procesamiento de lenguaje natural

Se ejecutó una libreta de jupyter con un ejemplo del uso de wordcloud:https://colab.research.google.com/github/mcd-unison/ing-caract/blob/main/ejemplos/tipos/python/nube_informe.ipynb 

stopwords:Palabras (en spaCy) que no contienen valor o significado. Ejemplo "que" "o" "el" etc.


