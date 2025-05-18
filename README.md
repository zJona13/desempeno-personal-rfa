# Desempeño Personal - RFA

Este proyecto es una aplicación web desarrollada con Python y herramientas modernas de frontend, diseñada para gestionar el desempeño personal. Incluye autenticación JWT, rutas protegidas, y estilos con Tailwind CSS.

## 🛠️ Tecnologías Utilizadas

- **Python 3.10+**
- **FastAPI** (o Flask si es el caso)
- **Tailwind CSS**
- **HTML (Jinja2 o render básico)**
- **JWT para autenticación**
- **Node.js** (para compilar Tailwind)
- **SQLite o similar (puede variar)**

## 📁 Estructura del Proyecto

DESARROLLO-PERSONAL-RFA/
├── models/ # Modelos de datos
├── routes/ # Rutas del API
├── static/ # Archivos estáticos (CSS)
│ ├── dist/ # Archivos compilados
│ └── src/ # Archivos fuente de Tailwind
├── templates/ # HTML templates
├── tools/ # Utilidades (JWT, seguridad)
├── app.py # Archivo principal de la app
├── conexionBD.py # Conexión a la base de datos
├── config.py # Configuraciones generales
├── .gitignore # Ignorar archivos innecesarios en Git
├── requirements.txt # Dependencias de Python
├── package.json # Configuración de Node.js
├── tailwind.config.js # Configuración de Tailwind


## ⚙️ Instalación y Ejecución

### Backend

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tuusuario/desempeno-personal-rfa.git
   cd desempeno-personal-rfa

2. **Si gustas puedes crear un entorno virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate   # En Linux/Mac
    venv\Scripts\activate      # En Windows

3. **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt

### Frontend

1. **Instalar dependencias de Node.js:**
   ```bash
   npm install

2. **Compilar CSS con Tailwind:**
    ```bash
    npx tailwindcss -i ./static/src/input.css -o ./static/dist/output.css --watch