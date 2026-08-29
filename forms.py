from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField, SelectField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length, Optional


class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')
    

class PhotoUploadForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=150)])
    description = TextAreaField('Descripción', validators=[Optional(), Length(max=500)])    
    capture_date = DateField("Fecha de captura", validators=[Optional()], format="%Y-%m-%d")
    location = StringField('Ubicación', validators=[Optional(), Length(max=150)])
    bortle = SelectField(
        'Escala de Bortle',
        choices=[(str(i), str(i)) for i in range(1, 10)],
        validators=[],
        validate_choice=True
    )
    telescopio = StringField('Telescopio', validators=[Optional(), Length(max=100)])
    montura = StringField('Montura', validators=[Optional(), Length(max=100)])
    camara = StringField('Cámara', validators=[Optional(), Length(max=100)])
    exposure_info = StringField('Exposición', validators=[Optional(), Length(max=100)])
    image = FileField('Imagen',
                      validators=[FileRequired("Seleccione una imagen"),
                     FileAllowed(['jpg', 'jpeg', 'png'], 'Solo se permiten imágenes en formato JPG o PNG.')])
    submit = SubmitField('Guardar')