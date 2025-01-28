# Microservicio de Autenticación Katalyst Control Suit

Este microservicio, desarrollado en python, implementa un sistema de autenticación basado en **Flask** y **PostgreSQL**, diseñado para gestionar:
- Registro de usuarios.
- Inicio de sesión seguro.
- Generación y validación de tokens JWT (access y refresh).


El proyecto está diseñado para ser fácilmente desplegado en un entorno **Docker**, garantizando portabilidad y consistencia.

## Repositorio
El código fuente está disponible en el siguiente enlace:
[https://github.com/Javi-M79/kata-auth](https://github.com/Javi-M79/kata-auth)


## Herramientas
Herramientas necesarias para su puesta en marcha y pruebas.
- Docker (https://www.docker.com/).
- Docker compose.
- Postman.(https://www.postman.com/)

## Configuracion del archivo .env
Crear un archivo.env en la raiz del proyecto con la siguiente configuracion:
   ```env
     # Configuración de la base de datos
     DB_NAME=auth_db
     DB_USER=postgres
     DB_PASSWORD=postgres_password
     DB_HOST=db //Para lanzar con Docker. Cambiar a "localhost" para pruebas en local.
     DB_PORT=5432 //Cambiar puerto para evitar confilctos con la instalacion de postgresql en la maquina

     # Clave secreta JWT
     JWT_SECRET_KEY=supersecretkey
     ```