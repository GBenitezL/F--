# *F--*
## *Compilador para el Lenguaje F--*
## Manual de Usuario

El lenguaje F-- es un lenguaje de programación enfocado en el paradigma imperativo procedural. Cuenta con funciones básicas de muchos lenguajes modernos, y además permite hacer análisis estadísticos muy fácilmente.

### Inicialización del Programa
Para iniciar un programa, se require usar la palabra reservada 'program' seguida de un identificador
```
program  nombre_programa;
```
### Variables soportadas
- int
- char
- float
- bool

### Declaración de variables
Se pueden definir múltiples variables a la vez utilizando comas, pero estas deben de ser del mismo tipo. Para declarar un arreglo de cualquier tipo, se debe especificar su tamaño.
```
var variable1: bool;
var variable2, variable3: int;
var a, b, c: float[10];
```

#### Operaciones Aritméticas
- +: suma
- -: resta
- *: multiplicación
- /: división

#### Operaciones de Comparación
- <: menor
- \>: mayor
- <=: menor o igual
- \>=: mayor o igual
- ==: igual
- !=: diferente

#### Operaciones Booleanas
- &&: and
- ||: or

### Funciones Estadísticas 
Estas funciones están diseñadas para ser utilzizadas en arreglos

- mean()
- median()
- variance()
- std()

#### Otras funciones
- print: imprime en consola
- read: lee una entrada
- rand: genera un número aleatorio entre el parámetro 1 y el 2
- plot: grafica 2 arreglos en pantalla.

### Ciclos

#### While
```
while (i < 10) {
    print(i);
    i = i + 1;
}
```

#### For
```
for (i = 0; i < 10; 1) {
    print(i);
}
```

### Funciones
#### Declaracion
```
function func1: void(number: int){
    print("Number: ", number);
}
```
#### Llamado
```
func1(5);
```
