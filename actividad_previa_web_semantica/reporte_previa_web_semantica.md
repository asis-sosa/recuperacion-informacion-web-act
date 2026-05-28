# Reporte — Actividad previa Web Semántica
**Estudiante:** Sebastian Asis Sosa Santiago / 22120720

## Misión 0 — Investigación
 - ¿Qué diferencia hay entre una página web que describe a un museo y un dataset que lista museos con coordenadas y horarios? La diferencia mas clara seria el objetivo, mientras que la pagina que describe al museo, solo se enfoca en uno solo, sus horarios, interacciones, promociones, eventos y demas elementos que intervengan con ese mismo museo y no con otro que no este afiliado a este. El dataset, se podria tomar como una enorme tabla que contiene diferentes museos, sus horarios y las ubicaciones en coordenadas de donde encontrarlos, no se esta abarcando otro punto mas que esto y se expande a diferentes museos, no solo a uno.

- Busca «*Tim Berners-Lee four rules of linked data*» o «*cinco estrellas datos abiertos*». Resume con tus palabras qué significa que un dato esté «enlazado». Puede significar que ese dato, cuenta con una URL que lo adjunta a mas datos que estan relacionados, del mismo modo, en ese dato o datos se pueden incluir mas URL para enlazar aun mas datos que tengan relacion, estructurando el dato en un contexto mas amplio.

- Abre en el navegador la consulta de ejemplo de Wikidata Query Service (https://query.wikidata.org/) y ejecuta una consulta de demostración. ¿El resultado parece una tabla SQL o algo distinto? Anota una observación. Al utilizar el ejemplo de "Número de personas en WikiData" el resultado entrego una siple tabla de una sola columna con dos filas, titulo y valor, bastante sencillo y que se podria decir muy parecido a una tabla SQL, sin embargo al consultar un segundo ejemplo: "Colores de ojos más comunes entre los seres humanos" el resultado fue muy distinto y que sin duda no parece una tabla, mas bien luce mas como un diagrama conceptual o mental, donde las figuras o imagenes resaltan mas que el texto, su diseño sin duda no se podria considerar como una tabla, pero podria llegar a dar a entender lo que se espera.

## Misión 1 — Triples desde HTML/JSON

### Tiples

```python
triples_html = [
    ("ex:alicia", "tieneNombre", "Alicia García"),
    ("ex:alicia", "tieneRol", "Profesora de Matemáticas"),
    ("ex:alicia", "trabajaEn", "UNAM"),
    ("ex:bob", "tieneNombre", "Bob Martínez"),
    ("ex:alicia", "coautorDe", "ex:redes_grafos"),
    ("ex:bob", "coautorDe", "ex:redes_grafos"),
]

triples_json = [
    ("ex:libro_L42", "titulo", "Introducción a la Web Semántica"),
    ("ex:libro_L42", "tieneAutor", "ex:alicia_json"),
    ("ex:libro_L42", "tieneAutor", "ex:bob_json"),
    ("ex:alicia_json", "tieneNombre", "Alicia García"),
]
```

### Tiples Casi Iguales

```python
("ex:alicia", "tieneNombre", "Alicia García")
("ex:alicia_json", "tieneNombre", "Alicia García")
```

### Pregunta de Cierre
- Si mañana el HTML cambia la etiqueta "h1" a mayúsculas o mueve el nombre a una etiqueta "span", ¿tu extracción manual sigue siendo válida? Relaciona la respuesta con la idea de separar datos y presentación. Es probale que no sea completamente robusta, ya que la extraccion manual depende bastante de las etiquetas, para este caso, por lo que cambiarlas, la logica podria dejar de funcionar. La idea de separar datos y presentacion esta basada en el hecho de que justamente HTML esta pensado principalmente para presentar informacion, de forma atractiva y visual, mientras que los RDF (triples) estan pensados para representar significados, lo que son y como se relacionan.

## Misión 2 — URIs y París

### Tabla

| Nombre_en_Texto | URI | Tipo_Entidad |
|-----------------|-----|--------------|
| Paris | ex:ciudad/paris | Ciudad |
| Paris Hilton | ex:persona/paris_hilton | Persona |
| FR | ex:pais/francia | Pais |
| Francia | ex:pais/francia | Pais |

### sameAs

```python
same_as = {
    "FR": "http://geo.example/country/fr",
    "París Hilton": "http://people.example/paris_hilton",
}
```

### Riesgos Pregunta de Cierre
- ¿Qué riesgo hay si enlazas owl:sameAs de más (falsos positivos)? Menciona un ejemplo concreto con nombres de la misión. El mayo riesgo que hay al utilizar "owl:sameAs" de mas, como falsos positivos radica en el hecho de que podria unir entidades que en realidad son muy diferentes entre si. Un ejemplo seria si se llegase a enlazar lo siguiente "("ex:ciudad/paris", "owl:sameAs", "ex:persona/paris_hilton")", esto podria terminar por confundir a la maquina y terminaria por concluir que que Paris, la ciudad es una persona llamada Paris Hilton, lo cual claramente es erroneo.

## Misión 3 — Mini-grafo

### Codigo patron_b

```python
# TAREA B: patrón para obtener personas
patron_b = {"s": None, "p": "tipo", "o": "ex:Persona"}
print("Personas:", consulta_simple(G, patron_b))
```

### Salidas

- Autores: [{'o': 'ex:alicia'}, {'o': 'ex:bob'}]
- Personas: [{'s': 'ex:alicia'}, {'s': 'ex:bob'}]
- Grafo:
- {'s': 'ex:alicia', 'p': 'tipo', 'o': 'ex:Persona'}
- {'s': 'ex:alicia', 'p': 'nombre', 'o': 'Alicia García'}
- {'s': 'ex:alicia', 'p': 'conoce', 'o': 'ex:bob'}
- {'s': 'ex:bob', 'p': 'nombre', 'o': 'Bob Martínez'}
- {'s': 'ex:bob', 'p': 'tipo', 'o': 'ex:Persona'}
- {'s': 'ex:libro42', 'p': 'titulo', 'o': 'Introducción a la Web Semántica'}
- {'s': 'ex:libro42', 'p': 'autor', 'o': 'ex:alicia'}
- {'s': 'ex:libro42', 'p': 'autor', 'o': 'ex:bob'}
- {'s': 'ex:libro42', 'p': 'anio', 'o': '2019'}
- {'s': 'ex:alicia', 'p': 'tieneConocidoPersona', 'o': 'ex:bob'}

### Pseudocódigo SPARQL
- ¿En qué se parece consulta_simple a la cláusula WHERE de SPARQL? ¿en qué se queda corta? La consulta_simple tiene un parecido a la clausula "WHERE" en el sentido de que ambos buscan triples que coincidan con un patron. Es en los casos donde los campos son variables que aceptan cualquier valor y lo devuelven como resultado y, donde mas se queda corta es precisamente en su similitud y es que consulta_simple solo buscan por un patron, no puede involucrarsele mas un patron, ademas de que no maneja nombres de variables reales, filtros y demas elementos que si cuenta la clasula "WHERE".

```sql
PREFIX ex: <http://ejemplo.org/>

SELECT ?persona
WHERE {
  ex:libro42 ex:autor ?persona .
}
```

## Puente al tema 5
- Responde en 5–8 líneas: «¿Qué problema de esta actividad resuelve RDF que no resuelve solo JSON?» Como tal, JSON trabaja con ua estructura donde relaciona cadenas de texto con etiquetas, por decirlo relaciona la etiqueta titulo con una cadena que representa el titulo de algun dato o pagina, del mismo modo se puede decir con la etiqueta autores con los nombres de autores, pero nada mas, aqui no podemos relacionar que alguno de los autores de cierto JSON son los mismos que en otro JSON y hacerlo sin duda seria una tarea un complicada que muy probablemente involucraria el uso de logica adicional, RDF en cambio trabaja con tres cosas claves, identificadores globales, modelos de grafo e integracion entre fuentes, esto permite contar con entidades unicas que permiten decir, por decir un ejemplo, un nombre de persona es exactamente esta entidad, guardar relaciones navegables que permiten consultas que son muy parecidoas a las del tipo "SPARQL" y conectar datos de diferentes origenes. Si lo tuvieramos que sintetizar, podriamos decir que JSON organiza los datos en etiquetas, mientras que RDF organiza significados y relaciones entre datos.