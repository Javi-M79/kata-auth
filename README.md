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
     DB_PORT=5432 //Cambiar puerto si es necesario para evitar confilctos con la instalacion de postgresql en la maquina local.

     # Clave secreta JWT
     JWT_SECRET_KEY=supersecretkey
 ```     
     
## Puesta en marcha

- Construir la image del docker
```aiignore
docker build
```
- Iniciar los contenedores
```aiignore
docker compose up -d
```
- Verificar que los servicios están corriendo
```
docker ps
```
- Aparecera por consola algo similar a esto:
```aiignore
CONTAINER ID   IMAGE           COMMAND                  CREATED        STATUS       PORTS                    NAMES
cbaaf6849f4d   kata-auth-app   "python src/app.py"      3 hours ago    Up 3 hours   0.0.0.0:5000->5000/tcp   kata_auth_app
9b9cf2026ef3   postgres        "docker-entrypoint.s…"   14 hours ago   Up 3 hours   0.0.0.0:6001->5432/tcp   kata_auth_service

```
- Probar endopints
```aiignore
hhttp://localhost:5000/ping
```
- Respuesta endpoint /ping
```aiignore
{
  "message": "Servidor conectado correctamente"
}
```




