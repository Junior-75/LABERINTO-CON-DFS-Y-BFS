FROM python:3.10

WORKDIR /app

# copiamos los archivos de nuestra app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
WORKDIR /app/app
# Corremos la aplicacion
CMD ["python3", "menu.py"]