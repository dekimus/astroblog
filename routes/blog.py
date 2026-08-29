from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from models import Photo
from extensions import db
from forms import PhotoUploadForm
from utils import generar_slug, procesar_imagen, eliminar_imagen




blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/')
def index():
    photos = Photo.query.order_by(Photo.created_at.desc()).all()
    return render_template('index.html', photos=photos)


@blog_bp.route('/photo/<slug>')
def photo_detail(slug):
    photo = Photo.query.filter_by(slug=slug).first_or_404()
    return render_template('photo.html', photo=photo)

@blog_bp.route("/subir", methods=["GET", "POST"])
@login_required
def upload():
    form = PhotoUploadForm()

    if form.validate_on_submit():
        display_filename, thumb_filename, original_filename = procesar_imagen(form.image.data)
        slug = generar_slug(form.title.data)

        photo = Photo(
            title=form.title.data,
            slug=slug,
            description=form.description.data,
            filename=display_filename,
            thumbnail_filename=thumb_filename,
            original_filename=original_filename,
            capture_date=form.capture_date.data,
            location=form.location.data,
            bortle=form.bortle.data,
            telescopio=form.telescopio.data,
            montura=form.montura.data,
            camara=form.camara.data,
            exposure_info=form.exposure_info.data,
            
        )
        db.session.add(photo)
        db.session.commit()

        flash("Foto subida correctamente.", "success")
        return redirect(url_for("blog.photo_detail", slug=photo.slug))

    return render_template("upload.html", form=form)

@blog_bp.route('/photo/<int:photo_id>/delete', methods=['POST'])
@login_required
def delete_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)

    # Guardar el nombre del archivo antes de borrar el registro
    filename = photo.filename

    db.session.delete(photo)
    db.session.commit()

    # Borrar también el archivo físico
    eliminar_imagen(filename)

    flash('Foto eliminada correctamente.', 'success')

    return redirect(url_for('blog.index'))