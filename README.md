# NautaPy

__NautaPy__ Python API para el portal cautivo [Nauta](https://secure.etecsa.net:8443/) de Cuba + CLI.

![Screenshot](../screenshots/screenshots/console-screenshot.png?raw=true)

## Requisitos

1. Instale la última versión estable de [Python3](https://www.python.org/downloads/)

## Instalación

Instalación:

```bash
pip3 install --upgrade https://github.com/abrahamtoledo/nautapy.git#v0.2.0
```

## Modo de uso

#### Agrega un usuario

```bash
nauta users add periquito@nauta.com.cu
```

Introducir la contraseña cuando se pida. Cambie `periquito@nauta.com.cu` por 
su usuario Nauta.

#### Iniciar sesion:

__Especificando el usuario__

```bash
nauta up periquito
```

Se muestra el tiempo en el terminal, para cerrar la sesión se debe pulsar `Ctrl+C`.

* Opcionalmente puede especificar la duración máxima para la sesión, luego de la cual se desconecta automáticamente:
    
    ```bash
    nauta up --time 60 periquito
    ```
    
    El ejemplo anterior mantiene abierta la sesión durante un minuto.

__Sin especificar el usuario__

```bash
nauta up
```
Se utiza el usuario predeterminado o el primero que se encuentre en la base de datos.


#### Ejecutar un comando con conexion

```bash
run-connected <cmd>
```
Ejecuta la tarea especificada con conexion, la conexion se cierra al finalizar la tarea.


#### Consultar informacion del usuario

```bash
nauta info periquito
```

__Salida__:

```text
Usuario Nauta: periquito@nauta.com.cu
Tiempo restante: 02:14:24
Credito: 1.12 CUC
```

#### Determinar si hay conexion a internet

```text
nauta is-online
```

__Salida__:
```text
Online: No
```

#### Determinar si hay una sesion abierta

```text
nauta is-logged-in
```

__Salida__:
```text
Sesion activa: No
```
    
# Mas Información

Lee la ayuda del modulo una vez instalado:

```bash
nauta --help
```

## Contribuir
Todas las contribuciones son bienvenidas. Puedes ayudar trabajando en uno de los issues existentes. 
Clona el repo, crea una rama para el issue que estes trabajando y cuando estes listo crea un Pull Request.

Tambien puedes contribuir difundiendo esta herramienta entre tus amigos y en tus redes. Mientras
mas grande sea la comunidad mas solido sera el proyecto. 

Si te gusta el proyecto dale una estrella para que otros lo encuentren mas facilmente.

### Contacto del autor 

- Twitter: [@atscub](https://twitter.com/atscub)
- Telegram: [@atscub](https://t.me/atscub)


### Compartir
- [Twitter](https://twitter.com/intent/tweet?url=https%3A%2F%2Fgithub.com%2Fabrahamtoledo%2Fnautapy%2F&text=Python%20API%20para%20el%20portal%20cautivo%20Nauta%20de%20Cuba%20%2B%20CLI)
