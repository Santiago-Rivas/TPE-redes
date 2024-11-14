# TPE: Grafana

## Composición de los containers

Para poder utilizar el servicio de Grafana y monitorear las métricas de nuestros servidores, tenemos que hacer primero:

```bash
docker-compose down
docker-compose up -d
```

Esto reinicia el ambiente dentro del directorio que contiene nuestra configuración Docker.

## Configuraciones de Grafana

### Monitoreo de distintos niveles de servicio

En estos pasos crearemos las alertas para ver cuándo el servicio en cuestión demora bastante, o mucho en responder.

1. En la máquina local, abrir http://localhost:3000
2. En el menú lateral, poner el mouse sobre el "+", crear un Dashboard y luego, tocar "Add a new panel"
3. En el menú inferior, en "Query", crear la consulta que sea pertinente. En nuestro caso será ```probe_duration_seconds, instance = http://delay-api:80```
4. Luego, ir a "Alert" y tocar "Create alert rule from this panel".
5. Elegir carpeta, poner una condición límite en la expresión B para "IS ABOVE", nosotros pondremos 2 segundos, luego, 6 segundos como mucho.
6. Por último, elegir "None" como Period.
7. Opcionalmente, agregar los Contact Points de los mails de los operadores y administradores, así podremos alertarles a cada punto de contactos según el caso.
