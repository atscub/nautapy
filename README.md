# NautaPy

__NautaPy__ Python API para el portal cautivo [Nauta](https://secure.etecsa.net:8443/) de Cuba + CLI.

![Screenshot](../screenshots/screenshots/console-screenshot.png?raw=true)

## Requisitos

1. Instale la última versión estable de [Python3](https://www.python.org/downloads/)

## Instalación

Instalación:

```bash
pip3 install --upgrade git+https://github.com/plinkr/nautapy.git
```

## Modo de uso

#### Agrega un usuario

```bash
nauta users add periquito@nauta.com.cu
```

Introducir la contraseña cuando se pida. Cambie `periquito@nauta.com.cu` por 
su usuario Nauta.

#### Iniciar sesión:

__Especificando el usuario__

```bash
nauta up periquito
```

Se muestra el tiempo en el terminal, para cerrar la sesión se debe pulsar `Ctrl+C`.

* Opcionalmente puede especificar la duración máxima para la sesión, luego de la cual se desconecta automáticamente:
    
    ```bash
    nauta up --session-time 60 periquito
    ```
    
    El ejemplo anterior mantiene abierta la sesión durante un minuto.

__Sin especificar el usuario__

```bash
nauta up
```
Se utiza el usuario predeterminado o el primero que se encuentre en la base de datos.


#### Ejecutar un comando con conexión

```bash
run-connected <cmd>
```
Ejecuta la tarea especificada con conexión, la conexión se cierra al finalizar la tarea.


#### Consultar información del usuario

```bash
nauta info periquito
```

__Salida__:

```text
Usuario Nauta: periquito@nauta.com.cu
Tiempo restante: 02:14:24
Crédito: 1.12 CUC
```

#### Determinar si hay conexión a internet

```text
nauta is-online
```

__Salida__:
```text
Online: No
```

#### Determinar si hay una sesión abierta

```text
nauta is-logged-in
```

__Salida__:
```text
Sesión activa: No
```
    
# Más Información

Lee la ayuda del módulo una vez instalado:

```bash
nauta --help
```

## Contribuir
__IMPORTANTE__: Notifícame por Twitter (enviar DM) sobre cualquier actividad en el proyecto (Issue o PR).

Todas las contribuciones son bienvenidas. Puedes ayudar trabajando en uno de los issues existentes. 
Clona el repo, crea una rama para el issue que estés trabajando y cuando estés listo crea un Pull Request.

También puedes contribuir difundiendo esta herramienta entre tus amigos y en tus redes. Mientras
más grande sea la comunidad más sólido será el proyecto. 

Si te gusta el proyecto dale una estrella para que otros lo encuentren más fácilmente.

### Contacto del autor 

- Twitter: [@atscub](https://twitter.com/atscub)


### Compartir
- [Twitter](https://twitter.com/intent/tweet?url=https%3A%2F%2Fgithub.com%2Fatscub%2Fnautapy%2F&text=Python%20API%20para%20el%20portal%20cautivo%20Nauta%20de%20Cuba%20%2B%20CLI)
