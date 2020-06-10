## Proxy para Nautapy:
Proxy que establece sesión nauta de manera transparente, cada vez que recibe una nueva petición de conexión. Se debe iniciar la sesión al recibir una petición en el proxy, siempre y cuando no haya ya una sesión activa. Se debe cerrar la sesión cuando no queden conexiones activas. El proxy solo debe cerrar una sesión nauta si esta fue abierta por él mismo.


### Features:
- Conexiones recurrentes, usar `asyncio`.
- Debe ser posible especificar la unidad mínima de división de tiempo, según tarificación de ETECSA, por ejemplo para Nauta Hogar sería 120s.
- Filtrado por `domain_name` (_whitelist_ o _blacklist_).


### Linea de comandos

```bash
nauta proxy [OPTIONS]

OPTIONS puede ser:
-p, --port          Puerto especificado del servicio, default: 3128
-t, --time-unit     Unidad de division de tiempo. Este parametro es obligatorio.
-u, --user          Usuario que se usara para conectarse, default: default_nautapy_user
-m, --max-conn      Maximo número de conexiones simultaneas
-l, --log           Logs file, use "-" for stdout, defautl: "-"
```
