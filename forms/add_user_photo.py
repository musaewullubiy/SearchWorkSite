from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField
from wtforms.validators import DataRequired


class AddAboutForm(FlaskForm):
    add_photo = FileField('Описание', validators=[DataRequired()])
    submit = SubmitField('Добавить')
