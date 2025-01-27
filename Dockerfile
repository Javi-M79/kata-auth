
#Imagen de python

#Imagen de python
FROM python:3.12-slim

#Directorio de trabajo
WORKDIR /app

#Copia archivos necesarios al contenedor
COPY requirements.txt requirements.txt


#Instalacion de dependencias
RUN pip install --no-cache-dir -r requirements.txt

#Copia todos los archivos del proyecto al contenedor
COPY . .

#Expone el puerto 5000 para Flask
EXPOSE 5000

#Comando para ejecutar la aplicacion
CMD ["python","app.py"]

#Directorio de trabajo
WORKDIR /app

#Copia archivos necesarios al contenedor
COPY requeriments.txt requeriments.txt
COPY . .

#Instalacion de dependencias
RUN pip install --no-cache-dir -r requirements.txt

#Expone el puerto 5000 para Flask
EXPOSE 5000

#Comando para ejecutar la aplicacion
CMD ["python","app.py"]

