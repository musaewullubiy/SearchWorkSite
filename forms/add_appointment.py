from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, DateField, SelectField, StringField, TimeField, BooleanField
from wtforms.validators import DataRequired


class AddAppointmentForm(FlaskForm):
    message = TextAreaField('Сообщение', validators=[DataRequired()])
    date = DateField('Удобное день для собеседования', validators=[DataRequired()])
    time = TimeField('Удобное время для собеседования', validators=[DataRequired()])
    platform = SelectField(
        label='Платформа для собеседования',
        choices=[('Telegram', 'Telegram'), ('Discord', 'Discord')],
        validators=[DataRequired()])
    link = StringField('Ссылка на профиль', validators=[DataRequired()])
    submit = SubmitField('Предложить')
