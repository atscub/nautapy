# nauta-cli

Original [ateijelo/nauta-cli](https://github.com/ateijelo/nauta-cli)

## Descripción

**nauta-cli** es una utilidad en línea de comandos (CLI) para la gestión del portal cautivo [Nauta](https://secure.etecsa.net:8443/) de Cuba.

## Estadisticas
![Downloads](https://pepy.tech/badge/nauta-cli)

## Requisitos

1. Instale la última versión estable de [Python](https://www.python.org/downloads/)

## Instalación

Instalación fácil con PIP:

`> python -m pip install --upgrade nauta-cli`

## Modo de uso

1. Crear una entrada de usuario (card). En el terminal introducir:


    `> nauta card add periquito@nauta.com.cu`
    
    Introducir la contraseña cuando se pida. Debe cambiar `periquito@nauta.com.cu` por su usuario Nauta.

1. Iniciar sesion:

    `> nauta up periquito`
    
    Se muestra el tiempo en el terminal, para cerrar la sesión se debe pulsar `Ctrl+C`.

    * Opcionalmente puede especificar la duración máxima para la sesión, luego de la cual se desconecta automáticamente:
    
        `> nauta up --time 60 periquito`
        
        El ejemplo anterior mantiene abierta la sesión durante un minuto.
    
# Mas Información

Lee la ayuda del modulo una vez instalado:

`> nautacli --help`
