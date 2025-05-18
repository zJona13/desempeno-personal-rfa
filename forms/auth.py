from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Correo Electrónico', validators=[
        DataRequired('Este campo es obligatorio'),
        Email('Por favor ingrese un correo válido')
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired('Este campo es obligatorio')
    ])
    remember = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')

class PasswordResetForm(FlaskForm):
    email = StringField('Correo Electrónico', validators=[
        DataRequired('Este campo es obligatorio'),
        Email('Por favor ingrese un correo válido')
    ])
    submit = SubmitField('Enviar Instrucciones')

class PasswordChangeForm(FlaskForm):
    current_password = PasswordField('Contraseña Actual', validators=[
        DataRequired('Este campo es obligatorio')
    ])
    new_password = PasswordField('Nueva Contraseña', validators=[
        DataRequired('Este campo es obligatorio'),
        Length(min=8, message='La contraseña debe tener al menos 8 caracteres')
    ])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[
        DataRequired('Este campo es obligatorio'),
        EqualTo('new_password', message='Las contraseñas deben coincidir')
    ])
    submit = SubmitField('Cambiar Contraseña')