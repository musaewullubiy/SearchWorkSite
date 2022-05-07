import datetime
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Appointments(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'appointment'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)  # id собес-ния
    message = sqlalchemy.Column(sqlalchemy.Text, nullable=True)  # сообщение
    datetime = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)  # дата собес-ния
    platform = sqlalchemy.Column(sqlalchemy.String, default="Discord")  # платформа для собеседования
    link = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # ссылка на профиль
    hr = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))  #  id отправляющего заявку на собеседования
    finder = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))  #  id принимающегт заявку на собеседования
    is_actual = sqlalchemy.Column(sqlalchemy.Boolean, default=True)  #  актуальность
