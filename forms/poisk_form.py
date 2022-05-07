from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class PoiskForm(FlaskForm):
    poisk_data = StringField('Я ищу...', validators=[DataRequired()])
    submit = SubmitField('Погнали')