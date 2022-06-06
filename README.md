# Asignación de teoría de autómatas 
## Conversiones cubiertas:

1. Regex a AFN
2. Convertir AFN a AFD
3. Minimizar AFD 

## Compilacion
`python3 q<no>.py arg1 arg2`  done arg1 es el path del input y arg2 es el output

## Simbolos
- '+' : union 
- '*' : Kleene
- '$' : epsilon 
- '()' : Agrupacion

## I/O 
Archivo Json

## Problema 1: Convertir Regex a AFN

### Pasos

1. Agregamos el simbolo de concatenacion "." en add_concat()
2. Pasamos la Expresion Regular es su forma postfija de acuerdo a su precedencia dada en compute_regex()
3. Creamos el arbol de expresiones en la funcion exp_tree() a partir de la expresion obtenida en el paso 2 
4. Ahora compute_regex() usando el arbol de expresion que se obtubo anteriormente, Pasamos la raiz del arbol de expreiones a esta funcion
5. De acuerdo con la operación encontrada, vamos a la función respectiva para evaluarla.
6. Cada estado consta de pares que contienen diccionarios
7. Cada cálculo devuelve su estado inicial y final.
8. En do_concat() concatenamos el lado izquierdo y derecho de "." despues de calcularlos. Luego el final de la izquierda se une al inicio de la derecha usando èpsilon "$"
9. En do_union(), calculamos el lado izquierdo y derecho de "+" y luego unimos el estado de inicio creando al inicio de estos dos por "$". Del mismo modo, unimos el final de estos al estado final creado por "$". Luego devolvemos el nodo inicial y final.
10. En do_kleene_star(), calculamos la expresión a destacar. Luego unimos su estado inicial y final creado con el estado inicial creado por "$" y también los unimos al final del nfa calculado para completar el bucle.
11. Encontrar un simbolo genera dos estados, inicio y fin, unidos por el simbolo y devuelve los estados
12. Luego hacemos el objeto NFA según sea necesario. Tenemos los estados junto con sus transiciones ahora. Sumamos todos los estados y la función de transición.
13. Obtenemos los estados de inicio agregando el inicio y los estados conectados a él por "$" y, de manera similar, obtenemos los estados finales.
14. Mostramos el AFN como un objeto json.

## Problema 2: Convertir AFN a AFD

### Pasos
1. Después de cargar el AFN, primero obtenemos el conjunto de potencia de los estados AFN para obtener los estados AFD.
2. Luego, para cada estado en el AFD, agregamos los estados donde los estados nfa en él hacen la transición y tomamos su unión.
3. Los estados de inicio del AFD son los estados de inicio del AFN.
4. Los estados finales de AFD consisten en todos los estados que tienen al menos un estado AFN final. Los incluimos en los estados finales de AFD.
5. Mostramos el AFD como un objeto json.

## Problem 3: Minimizar AFD

### Pasos
1. Después de cargar el DFA, primero eliminamos los estados inalcanzables del estado inicial. Para eso, obtenemos los estados alcanzables desde el estado inicial y luego actualizamos los estados y la función de transición considerando solo los estados alcanzables.
2. Para minimizar AFD, calculamos las clases de equivalencia 0, las clases de equivalencia 1... hasta que no necesitemos más divisiones.
3. Primero dividimos los estados final y no final. Luego, en cada iteración verificamos si los estados en el mismo grupo pasan a estados en el mismo grupo. Si no lo son, dividimos los estados considerados.
4. Hacemos la agrupación usando group que contiene bool para si los estados están en el mismo grupo o no.
5. Finalmente, para obtener los grupos, usamos la unión de conjuntos disjuntos. Luego obtenemos los nuevos estados y calculamos la función de transición usando estos nuevos estados tomando todas las transiciones de un conjunto de estados a otro.
6. Calculamos los estados inicial y final tomando los estados que contienen al menos un estado inicial y final respectivamente.
