from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, DateField, SelectField, StringField
from wtforms.validators import DataRequired


class AddAppointmentForm(FlaskForm):
    message = TextAreaField('Сообщение', validators=[DataRequired()])
    date = DateField('Удобное время для собеседования', validators=[DataRequired()])
    platform = SelectField(
        label='Платформа для собеседования',
        choices=[(1, 'Telegram'), (2, 'Discord')],
        validators=[DataRequired()])
    link = StringField('Ссылка на профиль', validators=[DataRequired()])
    submit = SubmitField('Предложить')
