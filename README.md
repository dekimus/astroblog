# 🔭 Astroblog

Blog personal de astrofotografía construido con Flask. Permite subir fotos desde el propio sitio (con autenticación), genera automáticamente miniaturas y versiones optimizadas para web, y muestra los datos técnicos de cada captura (telescopio, montura, cámara, exposición).

## Características

- **Autenticación de administrador** con Flask-Login — sin registro público, solo tú puedes subir contenido
- **Subida de fotos** con procesamiento automático (Pillow): genera una miniatura para la galería y una versión redimensionada para el detalle, corrigiendo la rotación EXIF
- **Ficha técnica por foto**: fecha de captura, ubicación, telescopio, montura, cámara y datos de exposición
- **URLs legibles** mediante slugs generados automáticamente a partir del título
- **Diseño propio** con tema oscuro inspirado en el cielo nocturno, fondo de estrellas animado en canvas y animaciones de scroll

## Stack

- [Flask](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) — ORM y base de datos (SQLite)
- [Flask-Login](https://flask-login.readthedocs.io/) — gestión de sesión del administrador
- [Flask-WTF](https://flask-wtf.readthedocs.io/) — formularios con protección CSRF
- [Pillow](https://pillow.readthedocs.io/) — procesamiento de imágenes
- [python-dotenv](https://pypi.org/project/python-dotenv/) — variables de entorno

## Puesta en marcha

### 1. Clonar y crear el entorno virtual

```bash
git clone https://github.com/tu-usuario/astroblog.git
cd astroblog
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Copia la plantilla y genera tu propia clave secreta:

```bash
cp .env.example .env
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Pega el resultado como valor de `SECRET_KEY` en tu `.env`.

### 4. Crear el usuario administrador

```bash
flask --app app:create_app create-admin tu_usuario
```

Te pedirá la contraseña dos veces.

### 5. Arrancar la app

```bash
python app.py
```

La app estará disponible en `http://127.0.0.1:5000`.

