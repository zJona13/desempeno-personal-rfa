# Desempeño Personal - RFA

Este proyecto es una aplicación web desarrollada con Python y herramientas modernas de frontend, diseñada para gestionar el desempeño personal. Incluye autenticación JWT, rutas protegidas, y estilos con Tailwind CSS.

## 🛠️ Tecnologías Utilizadas

- **Python 3.10+**
- **Tailwind CSS**
- **HTML (Jinja2 o render básico)**
- **JWT para autenticación**
- **Node.js** (para compilar Tailwind)
- **MySQL**

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