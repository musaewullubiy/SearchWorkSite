from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, EmailField, BooleanField, StringField, TextAreaField
from wtforms.validators import DataRequired


class VacancyForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    tags = TextAreaField('Теги', validators=[DataRequired()])
    text = TextAreaField('Опишите вакансию', validators=[DataRequired()])
    salary = StringField('Зарплата', validators=[DataRequired()])
    is_actual = BooleanField('Актуальная вакансия')

    submit = SubmitField('Сохранить')