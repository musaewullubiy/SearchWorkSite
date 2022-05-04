from flask import jsonify
from flask_restful import Resource, abort
from werkzeug.security import generate_password_hash

from data import db_session
from data.vacancies import Vacancy
from data.reqparse_vacancy import parser


def abort_if_vacancy_not_found(vacancy_id):
    session = db_session.create_session()
    vacancy = session.query(Vacancy).get(vacancy_id)
    if not vacancy:
        abort(404, message=f"Vacancy {vacancy_id} not found")


def set_password(password):
    return generate_password_hash(password)


class VacancyResource(Resource):
    def get(self, vacancy_id):
        abort_if_vacancy_not_found(vacancy_id)
        session = db_session.create_session()
        vacancies = session.query(Vacancy).get(vacancy_id)
        return jsonify(
            {'Vacancy': vacancies.to_dict(only=('title', 'tags', 'text', 'salary', 'is_actual', "hr_manager"))})

    def delete(self, vacancy_id):
        abort_if_vacancy_not_found(vacancy_id)
        session = db_session.create_session()
        vacancy = session.query(Vacancy).get(vacancy_id)
        session.delete(vacancy)
        session.commit()
        return jsonify({'success': 'OK'})


class VacancyListResource(Resource):
    def get(self):
        session = db_session.create_session()
        vacancies = session.query(Vacancy).all()
        return jsonify(
            {'vacancies': [item.to_dict(only=('title', "tags", 'text', 'salary', 'is_actual', "hr_manager")) for item in
                           vacancies]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        vacancy = Vacancy()
        vacancy.title = args["title"]
        vacancy.tags = args["tags"]
        vacancy.text = args["text"]
        vacancy.salary = args["salary"]
        vacancy.is_actual = bool(args["is_actual"])
        vacancy.hr_manager = args["hr_manager"]
        session.add(vacancy)
        session.commit()
        return jsonify({'success': 'OK'})
