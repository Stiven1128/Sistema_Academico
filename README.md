# Sistema Academico
## Descripció del Problema:
Una escuela tiene problemas  para  sistematizar  y calcular los promedios de  notas en linea  para sus  estudiantes, y que estos las puedan  visualizar las notas  sacadas periodo  a periodo  ya  que   no se tiene a tiempo  la informacion.

## Solución:
 Crear un sistema  para  calcular promedios en línea  de notas   de estudiantes periodo a periodo , es  decir   aprueba o reprueba. y que cada estudiante  las  pueda ver  para  ver en linea. Con el fin de ordenar  , registrar y recopilar  periodo  a periodo  las  notas apilando la información  en una estructura de  datos.  
-(cada estudiante  tendría su árbol o  estructura de  datos) 
-Utilizando  colas  de  prioridad , árboles de decisión o heap, según lo   visto en clase.


## Funcionalidades Clave del Sistema Académico

1. Gestión Académica Centralizada
Registro de actores:

- Estudiantes (nombre, ID, cursos matriculados).

- Profesores (asignaturas impartidas, grupos asignados).

- Asignaturas (código, créditos, prerrequisitos).

Relaciones dinámicas:

- Asignación de estudiantes a cursos y profesores mediante arrastrar/soltar o selección en QComboBox.

2. Cálculo Inteligente de Promedios
Algoritmos basados en estructuras de datos:

- Uso de heaps (colas de prioridad) para calcular promedios en tiempo real con complejidad O(log n).

- Árboles binarios para almacenar notas históricas por período (búsqueda eficiente en O(log n)).

Actualización automática:

- Al ingresar una nueva nota (nota.py), el sistema recalcula:

- Promedio del período actual.

- Promedio acumulado.

- Estado Aprobado/Reprobado (umbral configurable).

3. Visualización Interactiva
Dashboard unificado (views/dashboard.py):

- Gráficos de matplotlib integrados con FigureCanvas:

-- Evolución de notas por período (líneas temporales).

-- Comparativa de rendimiento vs. promedio del grupo.

Widgets de PyQt5:

- QProgressBar para mostrar avance en créditos académicos.

- QTableWidget con filtros por período/asignatura.

4. Registro de Notas en Tiempo Real
Interfaz para profesores (views/tabs/notas.py):

- Ingreso masivo de notas usando QDoubleSpinBox (validación: rango 0.0-5.0).

- Asignación automática a la estructura de datos del estudiante (árbol o heap).


5. Acceso Estudiantil Autogestionado
Panel personalizado (views/tabs/estudiantes.py):

- Visualización de todas las notas históricas apiladas en su estructura asignada.

- Filtrado por período con QComboBox.

- Exportación de reportes (PDF o CSV).



## Requesitos:
Python 3.13.3
### Librerias:
- PyQt5
- matplotlib


## Autores:
- Jose Stiven Rodas
- Elizabeth Salazar
