import re, os, unicodedata, uuid
from PIL import Image, ImageOps
from werkzeug.utils import secure_filename
from flask import current_app

from models import Photo


def generar_slug(titulo):
    texto = unicodedata.normalize('NFKD', titulo)
    texto = texto.encode('ascii', 'ignore').decode('ascii')
    texto = texto.lower()
    texto = re.sub(r'[^a-z0-9]+', '-', texto).strip('-')
    
    slug_base = texto
    slug = slug_base
    contador = 2
    while Photo.query.filter_by(slug=slug).first() is not None:
        slug = f"{slug_base}-{contador}"
        contador += 1
    return slug

def procesar_imagen(archivo):
    """
    Recibe el FileStorage del formulario, guarda la imagen original,
    genera una versión de visualización y una miniatura.
    Devuelve (filename_visualizacion, filename_miniatura, filename_original).
    """
    nombre_original = secure_filename(archivo.filename)
    extension = nombre_original.rsplit(".", 1)[1].lower()

    # Nombre único para evitar colisiones y no depender del nombre que puso el usuario
    identificador = uuid.uuid4().hex
    nombre_base = f"{identificador}.{extension}"

    ruta_upload = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(ruta_upload, exist_ok=True)

    imagen = Image.open(archivo)
    imagen = ImageOps.exif_transpose(imagen)  # corrige la rotación según el EXIF

    if imagen.mode not in ("RGB", "L"):
        imagen = imagen.convert("RGB")

    # Versión de visualización
    display_filename = f"display_{nombre_base}"
    imagen_display = imagen.copy()
    imagen_display.thumbnail(current_app.config["DISPLAY_SIZE"])
    imagen_display.save(os.path.join(ruta_upload, display_filename), quality=85, optimize=True)

    # Miniatura
    thumb_filename = f"thumb_{nombre_base}"
    imagen_thumb = imagen.copy()
    imagen_thumb.thumbnail(current_app.config["THUMBNAIL_SIZE"])
    imagen_thumb.save(os.path.join(ruta_upload, thumb_filename), quality=85, optimize=True)

    return display_filename, thumb_filename, nombre_original


def eliminar_imagen(filename):
    """
    Elimina la imagen de visualización, la miniatura y la original del sistema de archivos.
    """
    ruta_upload = current_app.config["UPLOAD_FOLDER"]
    display_path = os.path.join(ruta_upload, f"display_{filename}")
    thumb_path = os.path.join(ruta_upload, f"thumb_{filename}")
    original_path = os.path.join(ruta_upload, filename)

    for path in [display_path, thumb_path, original_path]:
        if os.path.exists(path):
            os.remove(path)