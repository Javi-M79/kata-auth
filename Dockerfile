# Imagen base de Python
FROM python:3.9-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar solo las dependencias primero para optimizar el uso de caché de Docker
COPY requirements.txt requirements.txt

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todos los archivos del proyecto al contenedor
COPY . .

# Exponer el puerto 5000 para la aplicación Flask
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "src/app.py"]
