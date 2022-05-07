from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    search_text = StringField('Введите запрос', validators=[DataRequired()])
    submit = SubmitField('Отправить')
