# TPE: Grafana

## Composición de los containers

Para poder utilizar el servicio de Grafana y monitorear las métricas de los hosts correr:

```bash
docker compose up -d
```

Para detener los contenedores utilizar:


```bash
docker compose down
```

Esto reinicia el ambiente dentro del directorio que contiene nuestra configuración Docker.

## Configuraciones de Grafana

### Monitoreo de Metrica

Para el monitoreo de metricas, acceder a la instancia de Grafana en http://localhost:3000.
Alli, luego de generar una nueva clave, se podran generar dashboards.
Cada Dashboard puede tener varios paneles de visualizacion.
Cada serie temporal de datos se puede visualizar de diferente manera.

A continuacion se presentaran los diferentes queries que se pueden realizar en la arquitectura construida con docker compose.

Para poder medir el CPU del node-exporter:

```
100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

Para poder medir el tiempo de un probe (tiempo de respuesta de un servidor):

```
probe_duration_seconds{instance="http://delay-api:80"}
```

Para obtener si la probe fue exitosa se puede utilizar probe_success,
en este caso se ve si fue exitosa la probe al endpoint /health del api service.
Se utiliza un regex para ver que se retorne lo esperado.

```
probe_success{job="blackbox-health"}
```

Para poder medir el cambio de una metrica en el tiempo se utiliza rate,
en este caso se mide la cantidad de comandos "set" realizdos por Redis:

```
rate(redis_commands_total{cmd="set"}[$__rate_interval])
```

### Filtrado

Cuando se edita un Dashboard, se puede entrar a los settings del mismo.
Alli se puede agregar una variable.
Esta funcionalidad tiene diferentes usos.

Se puede utlilizar para agregar un filtrado en la pantalla de paneles de un Dashboard.

### Monitoreo de distintos niveles de servicio

En estos pasos crearemos las alertas para ver cuándo el servicio en cuestión demora bastante, o mucho en responder.

1. En la máquina local, abrir http://localhost:3000
2. En el menú lateral, poner el mouse sobre el "+", crear un Dashboard y luego, tocar "Add a new panel"
3. En el menú inferior, en "Query", crear la consulta que sea pertinente. En nuestro caso será ```probe_duration_seconds, instance = http://delay-api:80```
4. Luego, ir a "Alert" y tocar "Create alert rule from this panel".
5. Elegir carpeta, poner una condición límite en la expresión B para "IS ABOVE", nosotros pondremos 2 segundos, luego, 6 segundos como mucho.
6. Por último, elegir "None" como Period.
7. Opcionalmente, agregar los Contact Points de los mails de los operadores y administradores, así podremos alertarles a cada punto de contactos según el caso.

