from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField
from wtforms.validators import DataRequired


class AddPhotoForm(FlaskForm):
    add_photo = FileField('Выберите фото', validators=[DataRequired()])
    submit = SubmitField('Добавить')
