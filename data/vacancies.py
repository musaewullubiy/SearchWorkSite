import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Vacancy(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'vacancies'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    tags = sqlalchemy.Column(sqlalchemy.Text)
    text = sqlalchemy.Column(sqlalchemy.Text)
    salary = sqlalchemy.Column(sqlalchemy.String)
    is_actual = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    hr_manager = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
