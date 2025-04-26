# Issues Manager

**Issues Manager** es una herramienta web para la gestión de incidencias, tareas y bugs, diseñada con un enfoque tipo tablero Kanban. Está pensada para facilitar la organización y seguimiento de proyectos en equipos de desarrollo.

## 🚀 Características

- Creación y gestión de issues (incidencias, tareas, bugs).
- Asignación de responsables por cada issue.
- Cambio de estados para el seguimiento visual al estilo Kanban.
- Interfaz sencilla y funcional para equipos de trabajo.

## 🛠️ Tecnologías

- **Backend:** Django
- **Base de Datos:** SQLite
- **Python:** 3.11.9
- Dependencias adicionales especificadas en `requirements.txt`

## 📦 Instalación

Sigue estos pasos para ejecutar el proyecto en tu entorno local:

1. **Clona el repositorio**
```bash
   git clone https://github.com/ChrisUBS/FSDI-113-issues-manager
   cd FSDI-113-issues-manager
```

2. **Crea un entorno virtual**
```bash
python -m venv venv
source venv/bin/activate   # En Windows usa: venv\Scripts\activate
```

3. **Instala las dependencias**
```bash
pip install -r requirements.txt
```

4. **Aplica las migraciones necesarias**
```bash
python manage.py migrate
```

5. **Crea un superusuario para acceder al panel administrativo**
```bash
python manage.py createsuperuser
```
6. **Ejecuta el servidor**
```bash
python manage.py runserver
```

### ⚡ Notas
- El proyecto incluye un archivo SQLite preconfigurado, por lo que no es necesario configurar la base de datos manualmente.
- Asegúrate de tener Python 3.11.9 instalado.

## 📄 Licencia
Este proyecto está licenciado bajo la GNU General Public License v3.0 (GPL-3.0).
Esto significa que puedes usar, modificar y distribuir este software libremente, siempre que las versiones derivadas también se distribuyan bajo la misma licencia.