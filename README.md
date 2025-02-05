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
     DB_PORT=5432 //Cambiar puerto si es necesario para evitar conflictos con la instalacion de postgresql en la maquina local.

     # Clave secreta JWT
     JWT_SECRET_KEY=supersecretkey
 ```     
     
## Puesta en marcha

- Construir la imagen del docker.
```aiignore
docker build
```
- Iniciar los contenedores.
```aiignore
docker compose up -d
```
- Verificar que los servicios están corriendo.
```
docker ps
```
- Aparecera por consola algo similar a esto:
```aiignore
CONTAINER ID   IMAGE           COMMAND                  CREATED        STATUS       PORTS                    NAMES
cbaaf6849f4d   kata-auth-app   "python src/app.py"      3 hours ago    Up 3 hours   0.0.0.0:5000->5000/tcp   kata_auth_app
9b9cf2026ef3   postgres        "docker-entrypoint.s…"   14 hours ago   Up 3 hours   0.0.0.0:6001->5432/tcp   kata_auth_service

```
- Introducir la siguiente direccion en el navegador o en Postman.
```aiignore
hhttp://localhost:5000/ping
```
- Respuesta endpoint /ping.     
```aiignore
{
  "message": "Servidor conectado correctamente"
}
```

## Documentacion Endpoitns

### 1. `/register`
- **Descripción**:Endpoint para el registro de usuarios nuevos en el sistema.
- **Metodo HTTP**: `POST`
- **URL**:`/register`
- **Headers**: `Content-Type: aplication/json`
- **Cuerpo de la solicitud**: Debe incluir los siguientes datos en formato json:
```json
{   
    "username":"user",
    "mail":"user@mail.com",
    "password":"password"
}   
  ```           
- Respuesta en caso de registro satisfactorio:
```json 
{
  "message": "Usuario javier registrado correctamente."
}
```
- Respuesta en el caso de usuario ya registrado:
```json
{
  "error": "El usuario ya está registrado."
}
```
### 2. ```/login```
- **Descripción**:Endpoint para el acceso del usuario registrado al sistema. 
- **Metodo HTTP**: `POST`
- **URL**:`/login`
- **Headers**: `Content-Type: aplication/json`
- **Cuerpo de la solicitud**: Debe incluir los siguientes datos en formato json:
```json
  {
    "mail": "javier@mail.com",
    "password": "1234",
    "sign": "firma_valida_generada"
  }
```
- Respuesta valida: 
```json
{
  "user": {
    "username": "javier",
    "person_id": "2048eeaf-ca64-4cf4-8ffc-77d7a8454726",
    "activated": true
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpX...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpX..."
}
```
- Codigos de estado:
  - `200`: Inicio de sesion correcto.
  - `400`: Faltan credenciales o firma invalida.
  - `401`: Usuario o contraseña incorrectos.


- Solicitud con credenciales correctas:
```json
{
  "mail": "javier@mail.com",
  "password": "1234",
  "sign": "firma_valida_generada"
}

```
- Respuesta:
```json
{
  "user": {
    "username": "javier",
    "person_id": "2048eeaf-ca64-4cf4-8ffc-77d7a8454726",
    "activated": true
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpX...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpX..."
}

```
- Firma invalida:
```json
{
  "mail": "javier@mail.com",
  "password": "1234",
  "sign": "firma_incorrecta"
}

```
- Respuesta: 
```json
{
  "error": "Firma inválida"
}

```
- Usuario o contraseña incorrectos:
```json
{
  "mail": "usuario_inexistente@mail.com",
  "password": "1234",
  "sign": "firma_valida_generada"
}

```
- Respuesta: 
```json
{
  "error": "Usuario o contraseña incorrectos"
}

```

### 3. `/auth`
- **Descripción**: Endpoint de autenticacion de usuario a traves de un JWT.
- **Metodo HTTP**: `POST`
- **URL**:`/auth`
- **Headers**: `Content-Type: aplication/json`
- **Cuerpo de la solicitud**: Debe incluir los siguientes datos en formato json:

# Microservicio de Autenticación Katalyst Control Suit

Este microservicio, desarrollado en Python, implementa un sistema de autenticación basado en **Flask** y **PostgreSQL**, diseñado para gestionar:
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

## Configuración del archivo .env
Crear un archivo .env en la raiz del proyecto con la siguiente configuración:
```env
# Configuración de la base de datos
DB_NAME=auth_db
DB_USER=postgres
DB_PASSWORD=postgres_password
DB_HOST=db # Para lanzar con Docker. Cambiar a "localhost" para pruebas en local.
DB_PORT=5432 # Cambiar puerto si es necesario para evitar conflictos con la instalación de PostgreSQL en la máquina local.

# Clave secreta JWT
JWT_SECRET_KEY=supersecretkey
```

## Puesta en marcha

- Construir la imagen del Docker.
```sh
docker build
```
- Iniciar los contenedores.
```sh
docker compose up -d
```
- Verificar que los servicios están corriendo.
```sh
docker ps
```
- Aparecerá por consola algo similar a esto:
```sh
CONTAINER ID   IMAGE           COMMAND                  CREATED        STATUS       PORTS                    NAMES
cbaaf6849f4d   kata-auth-app   "python src/app.py"      3 hours ago    Up 3 hours   0.0.0.0:5000->5000/tcp   kata_auth_app
9b9cf2026ef3   postgres        "docker-entrypoint.s…"   14 hours ago   Up 3 hours   0.0.0.0:6001->5432/tcp   kata_auth_service
```
- Introducir la siguiente dirección en el navegador o en Postman.
```sh
http://localhost:5000/ping
```
- Respuesta endpoint /ping.     
```json
{
  "message": "Servidor conectado correctamente"
}
```

### 3. `/auth`
- **Descripción**: Valida si un token JWT es válido.
- **Método HTTP**: `POST`
- **URL**: `/auth`
- **Headers**:
  - `Content-Type: application/json`
  - `Authorization: Bearer <access_token>`
- **Cuerpo de la solicitud**:
```json
{
  "token": "access_token_generado",
  "tokenType": "auth"
}
```
- **Respuesta esperada**:
```json
{
  "message": "Token válido, user_id = <user_id>"
}
```
- **Códigos de estado**:
  - `200`: Token válido.
  - `401`: Token inválido o expirado.
  - `400`: Falta el token en la solicitud.

#### **Casos de Uso**
1. **Solicitud con token válido**
   - **Request**:
   ```plaintext
   POST http://localhost:5000/auth
   Authorization: Bearer <access_token>
   ```
   - **Respuesta**:
   ```json
   {
     "message": "Token válido, user_id = 2048eeaf-ca64-4cf4-8ffc-77d7a8454726"
   }
   ```

2. **Solicitud con token inválido**
   - **Request**:
   ```json
   {
     "token": "token_incorrecto",
     "tokenType": "auth"
   }
   ```
   - **Respuesta**:
   ```json
   {
     "error": "Token inválido"
   }
   ```
   - **Código de estado**: `401`

### 4. `/refresh`
- **Descripción**: Genera un nuevo `access_token` y `refresh_token` utilizando un token de refresco válido.
- **Método HTTP**: `POST`
- **URL**: `/refresh`
- **Headers**:
  - `Content-Type: application/json`
  - `Authorization: Bearer <refresh_token>`
- **Cuerpo de la solicitud**:
```json
{
  "refreshToken": "refresh_token_valido"
}
```
- **Respuesta esperada**:
```json
{
  "access_token": "nuevo_access_token",
  "refresh_token": "nuevo_refresh_token"
}
```
- **Códigos de estado**:
  - `200`: Nuevo token generado correctamente.
  - `401`: Token inválido o caducado.
  - `400`: No se envió el `refresh_token`.

#### **Casos de Uso**
1. **Solicitud con `refresh_token` válido**
   - **Request**:
   ```plaintext
   POST http://localhost:5000/refresh
   Authorization: Bearer <refresh_token>
   ```
   - **Respuesta**:
   ```json
   {
     "access_token": "nuevo_access_token",
     "refresh_token": "nuevo_refresh_token"
   }
   ```
   - **Código de estado**: `200`

2. **Solicitud con `refresh_token` caducado**
   - **Request**:
   ```json
   {
     "refreshToken": "refresh_token_expirado"
   }
   ```
   - **Respuesta**:
   ```json
   {
     "error": "El token ha caducado."
   }
   ```
   - **Código de estado**: `401`

3. **Solicitud sin `refresh_token`**
   - **Request**:
   ```json
   {}
   ```
   - **Respuesta**:
   ```json
   {
     "error": "Falta el token de refresco"
   }
   ```
   - **Código de estado**: `400`
## Pruebas del Microservicio

Para probar los endpoints, puedes utilizar **Postman** o ejecutar comandos en la terminal con `cURL`.
### **Prueba con Postman**
1. Abre **Postman** y crea una nueva solicitud `POST`.
2. Ingresa la URL del endpoint que deseas probar.
3. En la pestaña **Headers**, agrega:
   - `Content-Type: application/json`
   - `Authorization: Bearer <token>` _(Sustituir `<token>` por el `access_token` o `refresh_token` según corresponda)_.
4. En la pestaña **Body**, selecciona `raw` y agrega el JSON de la solicitud.
5. Envía la solicitud y verifica la respuesta.

---

### **Probar `/auth` (Validar token de acceso)**
- **Método HTTP**: `POST`
- **URL**: `http://localhost:5000/auth`
- **Headers**:
  - `Content-Type: application/json`
  - `Authorization: Bearer <access_token>`
- **Body (JSON)**:
  ```json
  {
    "token": "<access_token>",
    "tokenType": "auth"
  }


### **Pruebas con `cURL`**
Ejecuta los siguientes comandos desde la terminal para probar los endpoints:

#### **1. Registro de usuario**
```sh
curl -X POST http://localhost:5000/register -H "Content-Type: application/json" -d '{
    "username": "javier",
    "mail": "javier@mail.com",
    "password": "1234"
}'
```

#### **2. Inicio de sesión**
```sh
curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d '{
    "mail": "javier@mail.com",
    "password": "1234",
    "sign": "firma_valida_generada"
}'
```

#### **3. Validación de token**
```sh
curl -X POST http://localhost:5000/auth -H "Content-Type: application/json" -H "Authorization: Bearer <access_token>" -d '{
    "token": "<access_token>",
    "tokenType": "auth"
}'
```

#### **4. Renovación de token**
```sh
curl -X POST http://localhost:5000/refresh -H "Content-Type: application/json" -H "Authorization: Bearer <refresh_token>" -d '{
    "refreshToken": "<refresh_token>"
}'
```


