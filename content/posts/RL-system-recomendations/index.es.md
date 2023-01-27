---
weight: 1
title: "RL y sistemas de recomendación"
date: 2023-01-14T21:29:01+08:00
lastmod: 2020-03-06T21:29:01+08:00
draft: false
author: "Kenny Flores"
authorLink: "https://www.mrkenny.me/"
description: "Discover what the Hugo - LoveIt theme is all about and the core-concepts behind it."
images: []
resources:
- name: "featured-image"
  src: "featured-image.jpg"

tags: ["Markov", "reinforce-learning","system-recomendation"]
categories: ["documentation"]

lightgallery: true

toc:
  auto: false

math:
  enable: true  
---

<!--
Que es un sistema de recomendación
Sistemas de recomendación tradicionales:
    - CF
    - based in content

Sistemas de recomendación con RL:
    - Que es el reinforce learning
    - Aplicaciones de sistemas con RL
    
Caso práctico: RL para sistemas de recomendación de
vídeos de youtube

Conclusiones

Referencias
NO SE DONDE INCLUIR MOVIELENS
-->

El aprendizaje por refuerzo ha tenido grandes avances en la robótica y en los videojuegos, pero con la creciente importancia de generar contenido personalizado al usuario en las plataformas en línea como Netflix o Spotify, el generar sistemas de recomendación basados en aprendizaje por refuerzo puede ofrecernos una serie de mejoras positivas a diferencia de los sistemas tradicionales basados en aprendizaje supervisado.

En este estudio se discutirá los diferentes tipos de sistemas de recomendación, los desafíos a los que tendremos que enfrentarnos del pasar de los sistemas tradicionales al uso de aprendizaje reforzado, un caso práctico donde se está usando en el mundo real, y una visión general de las tendencias y desarrollos actuales en el campo.

## 1. Sistemas de recomendación

Los sistemas de recomendación (o llamados en inglés "recommender systems") son algoritmos que buscan sugerir contenido o productos relevantes al usuario, en base a sus preferencias y otras informaciones relevantes.

Estos sistemas son fundamentales en diferentes industrias (como el comercio electrónico o aplicaciones de entrenimiento multimedia) para descubrir el contenido que les interesaría al usuario, haciendo que aumente la probabilidad de que se retengan en la plataforma y generen ingresos para la empresa.


### Sistemas de recomendación tradicionales

<!--
TODO: si añadimos los de segunda generación, deberemos
cambiar algunas cosas de aquí

si no, no pasa nada

-->

Existen dos paradigmas importantes dentro de los sistemas de recomendación antiguos: el filtro colaborativo y los sistemas basados en contenido. 


#### Sistemas de recomendación basados en filtro colaborativo

Este método construye una matriz de interacción usuario-elemento, que recoge las interacciones previas de los usuarios con los elementos.

Los elementos o items son los productos que se quieren recomendar al usuario (canciones, películas, libros, entre otros).

Se hace uso de esta matriz para idenfiticar los perfiles similares en función de su proximidad y aprender de sus intereses para recomendar a los usuarios. 

Ejemplo de matriz de interacción usuario-elemento:

<!--

TODO: INSERTAR IMAGEN DE MATRIZ DE INTERACCIÓN USUARIO-ELEMENTO

-->

En la figura anterior, se puede observar que tenemos una matriz donde las columnas son los productos que queremos valorar, y las filas son los usuarios que le dan una valoración a esos productos.

Las casillas que no están con ninguna valoración significan que el usuario aún no ha probado ese producto. Por lo cual nuestro objetivo es encontrar un modelo que prediga las interacciones que faltan en la matriz.

Dentro de este paradigma existen dos tipos de filro colaborativo:

<!--
(https://impulsatek.com/11-sistemas-de-recomendacion-y-modelos-de-aprendizaje-basados-en-grafos/#Sistemas_basados_en_filtrado_colaborativo)
-->

##### Basados en memoria

Aquí cuando tengamos un nuevo usuario calculamos la valoración de un producto por similitud entre usuarios o por parecido entre los productos.

<!--
La similitud o distancia entre usuarios o contanidos se puede calcular usando distancia euclidea, manhattan, jaccard, correlaciones, etc.
-->

##### Basados en modelos

Mientras tanto, en estos métodos se desarrollan modelos haciendo uso de algoritmos de aprendizaje automático sobre la matriz usuario-elemento para predecir las valoraciones de los usuarios de los elementos no valorados.


#### Sistemas de recomendación basados en contenido

En lugar de basarse en el historial de acciones de los usuarios, estos métodos usan la información sobre el contenido de los productos para enconrar similitudes y recomendar productos similares a los que el usuario ha mostrado interés.

Estos métodos también usan técnicas de aprendizaje automático para generar estas recomendaciones.


### Limitaciones del aprendizaje supervisado

Estos métodos tradicionales de recomendación están muy influenciados por técnicas de aprendizaje automático, y estos presentan algunas limitaciones que discutiremos a continuación:

#### Recomendación miope


Los sistemas de recomendación tradicionales tienen el problema de dar recomendaciones que probablemente te lleven a una respuesta inmediata, además de llevarte a resultados que tienden a recomendar un contenido que un usuario ha consumido previamente (recomendación miope). 

El que ocurra esto puede llevar a que un usuario acabe encerrado en una "burbuja de recomendación", en la cual un usuario se ve expuesto a un conjunto cada vez más estrecho de contenido.Y  en el peor de los casos, podría dañar la confianza de los usuarios a largo plazo.

#### Sesgo del sistema
<!-- System bias -->

Otro problema que nos podemos encontrar en estos sistemas es que no tienen en cuenta factores adicionales como las preferencias del usuario o el sesgo del sistema, lo que puede resultar en recomendaciones poco precisas o irrelevantes.

## Sistemas de recomendación con RL

<!-- Sistemas de recomendación con RL:
    - Que es el reinforce learning
    - Aplicaciones de sistemas con RL -->

Viendo las limitaciones que tiene el usar los sistemas de recomendación tradicionales, podemos hacer uso de aprendizaje por refuerzo para darle un nuevo enfoque al recomendar contenido a los usuarios.

<!-- Podríamos decir  "dinámicas del usuario para opimizarsu utilidad a largo plazo -->
El objetivo sería asegurar y descubrir las preferencias dinámicas del usuario para maximizar su satisfacción dentro de la plataforma, esto es posible con el paradigma del aprendizaje por refuerzo, debido a que es capaz de aprender contínuamente y equilibrar el mostrarle tanto contenido relevante para el usuario como presentarle contenido novedoso que le genere nuevos intereses.

Aunque obviamente aplicar este paradigma no es tan sencillo, ya que nos encontraremos una serie de desafíos que vamos a tener que resolver.

### ¿Qué es el aprendizaje por refuerzo?

El aprendizaje por refuerzo (Reinforce Learning en inglés) es la técnica más cercana al aprendizaje humano que se pueden conseguir en los sistemas actuales. Este paradigma consiste en que un agente (como podría ser un robot o una máquina) aprende a tomar acciones en un entorno mediante la retroalimentación en forma de recompensas o castigos. 

Al agente se le coloca en un entorno desconocido, donde debe tomar decisiones para alcanzar un objetivo específico, que mediante prueba y error, el agente aprende cuales acciones llevan a un resultado positivo, por lo cual las irá repitiendo, mientras que las acciones que lo lleven por un resultado negativo las va a ir evitando. 

Como hemos hablado, este paradigma tiene una gran variedad de aplicaciones como en el procesamiento del lenguaje natural, marketing o robots automatizados. Pero veremos que puede tener un uso muy interesante en los sistemas de recomendaciones.

### Retos al aplicar aprendizaje por refuerzo en sistemas de recomendación

Hemos visto que con este paradigma se pueden resolver los problemas que tenían los sistemas tradicionales, pero, ahora vamos a hablar de los diferentes retos que nos podríamos encontrar a la hora de poner en práctica este método.

1. **Gran espacio de acción:** se refiere a la cantidad de posibles acciones que un sistema de recomendación basado por refuerzo debe tomar en momento determinado.

    Por ejemplo, si quisieramos desarrollar un sistema de recomendación que recomiende vídeos de Youtube a un usuario, el espacio de estados serían la gigantesca cantidad de vídeos disponibles en el sitio.

    El gran espacio de estados representa un enorme desafío para el desarrollo del sistema, debido a que cuanto mayor sea el espacio de estados, más compleja será la tarea de aprender las preferencias del problema y seleccionar los productos (por ejemplo, los vídeos de Youtube) más adecuados para recomendar.

2. **Exploración costosa:** la exploración puede ser costosa en estos sistemas debido a la necesidad de probar diferentes acciones y adaptarse a los cambios en los gustos y preferencias del usuario.

    Aún así es importante hacer una buena exploración, debido a que si el recomendador solo te muestra contenido aleatorio, podría generar una mala experiencia al usuario.


<!-- 3. **Aprendizaje fuera de la política:** el aprendizaje fuera de la política o también conocido como off-policy es una técnica usada en aprendizaje por refuerzo que permite al sistema aprender de experiencias pasadas diferentes a la política actual, mejorando así su habilidad para poder adaptarse a situaciones no previstas anteriormente.

      El detalle es que implementar esta técnica puede ser muy desafiante debido a la complejidad en la selección y procesamiento de los datos de entrenamiento, como complicado de ajstar  -->


3. **Observabilidad parcial:** cuando estamos construyendo el sistema de recomendación, el usuario no nos informa explícitamente lo que le interesa y debemos inferir ese interés del usuario a partir de las actividades que realiza en la plataforma.


4. **Recompensa ruidosa:** esto se refiere a que tenemos señales de recompensa muy ruidosas y dispersas prodecentes de los usuarios. Esto puede ocurrir por una gran variedad de motivos, como podría ser la falta de información del contexto, que el usuario se sienta incómodo proporcionando recomendación o simplemente el usuario no sepa lo que quiere. <!-- TODO: BUSCAR MEJOR FRASE Debido a esto, habrá que buscar alguna forma de minimizar ese ruido. -->

<!-- ## Aplicaciones -->

## Caso práctico: RL para sistemas de recomendación de vídeos de youtube

En esta sección vamos a realizar un análisis de un caso real de implementación de un sistema de recomendación basado en aprendizaje por refuerzo. En este caso será el de recomendación de videos de youtube, desarrollado por la empresa Google.


### Introducción

El acceso a contenido en línea se ha convertido en una necesidad entre las plataformas más populares se encuentra Youtube, donde millones de personas consumen vídeos cada día. No obstante, el hacer uso de los sistemas tradicionales nos podía producir que los usuarios acaben encerrados en una "burbuja"  o dar recomendaciones irrelevantes que hagan que se pierda la confianza en el usuario, por lo cual el objetivo es adaptar y descubrir las preferencias dinámicas del usuario para poder optimizar su utilidad a largo plazo, y esto podremos conseguirlo haciendo uso del aprendizaje por refuerzo.

### Generación de candidatos

El sistema que produce las recomendaciones de los vídeos de Youtube es un recomendador de varias etapas, que selecciona docenas de videos para los usuarios a partir de un corpus formado por miles de millones de vídeos.

<!--
TODO: AÑADIR IMAGEN DE CANDIDATE GENERATOR DEL MINUTO
11:55 SIN LA PARTE DE LA DERECHA 

-->

En este estudio solamente se han centrado en la etapa de **generación de candidatos**, donde entra el corpus de los vídeos y  se reduce a unos cientos de vídeos más relevantes para pasar a la siguiente etapa.

Habrá algunos desafíos que se han encontrado para construir esta estructura, ya que el sistema de recomendación debe enfrentarse a los miles de millones de usuarios con preferencias que van cambiando a lo largo del tiempo, a miles de millones de vídeos que no tienen una gran cantidad de visitas, pero son relevantes para un pequeño grupo de usuarios (distribución de lanzamiento), o también comentarios de usuario ruidosos y dispersos. 

### Aprendizaje por refuerzo en sistemas de recomendación

Una vez hayamos entendido el significado de la generación de candidatos, vamos a basarlo en aprendizaje por refuerzo.

El objetivo es construir agentes que realicen acciones en un entorno para maximizar una noción de recompensa acumulativa, por lo que vamos a considerar nuestro **agente** al candidato generador, los **estados** serán el interés de los usuarios, así como los contactos de recomendación, la **recompensa** será la satisfacción del usuario y finalmente las **acciones** que pueden tomar el agente es elegir y proponer videos para ser incluidos en un catálogo con millones de videos.

### Construcción del modelo

En esta sección vamos a ver como los trabajadores de Youtube han ido construyendo el agente de recomendación de vídeos hacienddo uso de aprendizaje por refuerzo.

#### Agente y Recompensa

La fuente de datos que se ha utilizado para construir el agente es la trayectoria del usuario, es decir, una secuencia de actividades que el usuario ha realizado en la plataforma ( como los videos que ha visto, las búsquedas realizadad, etc.).


<!-- INSERTAR IMAGEN DE USER EVENTS DONDE SE VE EL USER STATE Y RECOMPENSA -->

Esta información se divide en la **trayectoria secuencial del pasado**,compuesta por las actividades anteriores a las recomendaciones del agente, y la **trayectoria secuencial del futuro**, con la información sobre las actividades que el usuario ha realizado después de recibir las recomendaciones del agente.

La autora de la presentación menciona que hacen uso de la trayectoria secuencial del pasado para llegar a la "creencia del estado del usuario" y hacen uso de la **trayectoria futura** para llegar a la recompensa.

#### Estados

<!-- Poner img User state representation through RNNs -->

Uno de los grandes desafíos a la hora de construir la representación del estado es la observabilidad parcial debido a que los usuarios no nos proporcionan información sobre sus intereses o como están satisfechos con las recomendaciones que les damos. Por lo que, para abordar este desafío se usan redes neuronales recurrentes (RNN) para analizar la actividad previa del usuario y obtener una representación del estado.

#### Acciones

En este caso haremos uso de un enfoque basado en políticas debido a que queremos maximizar directamente la recompensa a largo plazo y es más estable que un enfoque basado en valores.

Estamos tratando de aprender una política estocástica (Pi theta) que va a emitir una distribución sobre el espacio de estado de acciones, con el objetivo de maximizar la recompensa acumulada a largo plazo.

<!-- Añadir imagen de Policy-based RL

 -->

La trayectoria $\tau$ es generada siguiendo esta política y la recompensa acumulada es la suma total de recompensas para toda la trayectoria. Además, se pueden optimizar los parámetros de la política mediante el ascenso del gradiente. 

A causa de esto, se podría decir que el aprnedizaje por refuerzo está muy conectado al aprendizaje  supervisado, debido a que se optimiza para la verosimilitud logarítmica de observar la próxima acción, pero el paradigma del aprendizaje reforzado ofrece una manera de pensar en la exploración, planificación y cambio en el estado del usuario subyacente.

Usa una técnica de muestreo para abordar el espacio de acciones muy grande y ejecuta una búsqueda rápida en vecindarios para reducir el tiempo de procesamiento.

### Resolución de las limitaciones del aprendizaje automático

En esta parte vamos a ver como han podido solucionar las dos limitaciones que tienen los sistemas de recomendación tradicionales

#### Recomendación miope

Para abordar el problema que teníamos con la recomendación miope es incorporar recompensas futuras en lugar de solo considerar recompensas inmediatas. 

Cuando se hicieron experimentos, la incorporación de estas recompensas futuras hicieron que haya un aumento del 0.3% de ganancia en la matriz en línea.


#### Sesgo del sistema 

Este sistema solo tiene acceso a los datos de registro que son generados por un agente que se va actualizando cada 5 horas, lo que significa que la política de los agentes podría ser muy diferente de la política objetivo que se está tratando de aprender, por lo tanto, el equipo sigue estudiando como hacer frente al sesgo del sistema causado por solo tener acceso a estos datos de registro.

## Conclusiones

## Referencias