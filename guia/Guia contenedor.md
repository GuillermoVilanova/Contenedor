## **Guía para Crear y Desplegar una App en un Contenedor Docker**

### **1. Requisitos Previos**
- Tener instalado:
  - [Docker](https://www.docker.com/get-started) (sigue las instrucciones de la página).
  - Un editor de código como [VS Code](https://code.visualstudio.com/) o Sublime Text.
- Cuentas gratuitas en:
  - [GitHub](https://github.com/)
  - [Docker Hub](https://hub.docker.com/)
  - [Railway](https://railway.app)

---

### **2. Crear la Aplicación**
#### a) **Archivo `app.py`** (la app web)
1. Abre tu editor de código y crea un archivo llamado `app.py`.
2. Copia este código:
   ```python
   from flask import Flask
   app = Flask(__name__)

   @app.route('/')
   def hello():
       return "¡Hola desde Docker! 🐳"

   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=5000)
   ```

#### b) **Archivo `requirements.txt`** (dependencias)
1. Crea otro archivo llamado `requirements.txt`.
2. Copia esto:
   ```
   Flask==3.0.2
   gunicorn==21.2.0
   ```

---

### **3. Crear el Dockerfile** (receta para el contenedor)
1. Crea un archivo llamado `Dockerfile` (sin extensión).
2. Copia esto:
   ```Dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY app.py .
   EXPOSE 5000
   CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
   ```

---

### **4. Probar Localmente**
#### a) **Construir el Contenedor**
1. Abre una terminal en la carpeta de tu proyecto.
2. Ejecuta:
   ```bash
   docker build -t my-flask-app .
   ```

![alt text](image.png)

#### b) **Ejecutar el Contenedor**
```bash
docker run -p 5000:5000 my-flask-app
```
![alt text](image-1.png)

3. Abre tu navegador en: http://localhost:5000  
   ¡Deberías ver el mensaje de bienvenida!

![alt text](image-2.png)

#### c) **Detener el Contenedor**
Presiona `Ctrl + C` en la terminal o usa:
```bash
docker stop [ID_del_contenedor]
```
![alt text](image-3.png)
---

### **5. Subir a Docker Hub (con GitHub Actions)**
#### a) **Preparar GitHub**
1. Crea un repositorio nuevo en GitHub.
![alt text](image-4.png)
2. Sube tus archivos (`app.py`, `requirements.txt`, `Dockerfile`).

#### b) **Crear el Workflow de GitHub**
1. Crea una carpeta `.github/workflows` en tu proyecto.
2. Dentro, crea un archivo `docker-publish.yml` con este contenido:
   ```yaml
   name: Docker Build and Push

on:
  push:
    branches: ["main"]

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and Push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ secrets.DOCKER_USERNAME }}/my-flask-app:latest

      - name: List files for debugging
        run: ls -R

   ```

#### c) **Configurar Secrets en GitHub**
1. En tu repositorio de GitHub, ve a **Settings > Secrets > Actions**.
2. Crea dos secrets:
   - `DOCKER_USERNAME`: Tu usuario de Docker Hub.
   - `DOCKER_PASSWORD`: [Crea un token aquí](https://hub.docker.com/settings/security). si no funciona pon tu contraseña de dockrhub!

#### d) **Subir los Archivos a GitHub**
1. Asegúrate de que tu proyecto tenga esta estructura:
   ```
   tu-proyecto/
   ├── app.py
   ├── requirements.txt
   ├── Dockerfile
   └── .github/
       └── workflows/
           └── docker-publish.yml
   ```
2. Sube los archivos a GitHub:
   - Si usas GitHub Desktop, arrastra la carpeta del proyecto.
   - Si usas la terminal, ejecuta:
     ```bash
     git add .
     git commit -m "Primera subida"
     git push origin main
     ```

---

### **6. Verificar el Workflow**
1. Ve a tu repositorio en GitHub.
2. Haz clic en la pestaña **Actions**.
3. Deberías ver un workflow llamado "Docker Build and Push" en ejecución.
4. Si todo está bien, verás una marca verde (✅) cuando termine.

![alt text](image-5.png)
---

### **7. Desplegar en Railway**
1. Ingresa a [Railway](https://railway.app) y crea una cuenta.
2. Haz clic en **New Project > Deploy from Docker Hub**.
3. Escribe el nombre de tu imagen: `tudockerhubusuario/my-flask-app:latest`.
4. Railway desplegará automáticamente tu app.
5. ¡Listo! En la pestaña "Settings" de Railway encontrarás el enlace para acceder a tu app.

---

### **Estructura Final de tu Proyecto**
```
tu-proyecto/
├── app.py
├── requirements.txt
├── Dockerfile
└── .github/
    └── workflows/
        └── docker-publish.yml
```

---

### **Notas Importantes**
- Si tienes errores:
  - **Puerto 5000 en uso**: Cambia el puerto en `docker run -p 8080:5000 ...`.
  - **Problemas con Docker Hub**: Verifica que el token tenga permisos de escritura.
- Railway te da un dominio gratis tipo `https://tu-app.up.railway.app`.

---

### **Resumen de Pasos**
1. Crear la app (`app.py`, `requirements.txt`, `Dockerfile`).
2. Probar localmente con Docker.
3. Crear el archivo `.yml` para GitHub Actions.
4. Configurar Secrets en GitHub.
5. Subir los archivos a GitHub.
6. Verificar que el workflow funciona.
7. Desplegar en Railway.
