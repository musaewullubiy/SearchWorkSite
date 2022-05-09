from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class AddAboutForm(FlaskForm):
    text = TextAreaField('Описание', validators=[DataRequired()])
    submit = SubmitField('Добавить')
