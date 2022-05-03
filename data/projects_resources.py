from flask import jsonify
from flask_restful import Resource, abort
from werkzeug.security import generate_password_hash

from data import db_session
from data.projects import Project
from data.reqparse_project import parser


def abort_if_vacancy_not_found(project_id):
    session = db_session.create_session()
    project = session.query(Project).get(project_id)
    if not project:
        abort(404, message=f"Vacancy {project_id} not found")


def set_password(password):
    return generate_password_hash(password)


class ProjectResource(Resource):
    def get(self, project_id):
        abort_if_vacancy_not_found(project_id)
        session = db_session.create_session()
        projects = session.query(Project).get(project_id)
        return jsonify({'Project': projects.to_dict(only=('title', 'link', 'developer_id'))})

    def delete(self, project_id):
        abort_if_vacancy_not_found(project_id)
        session = db_session.create_session()
        project = session.query(Project).get(project_id)
        session.delete(project)
        session.commit()
        return jsonify({'success': 'OK'})


class ProjectListResource(Resource):
    def get(self):
        session = db_session.create_session()
        projects = session.query(Project).all()
        return jsonify(
            {'projects': [item.to_dict(only=('title', 'link', 'developer_id')) for item in projects]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        project = Project()
        project.title = args["title"]
        project.link = args["link"]
        project.developer_id = args["developer_id"]

        session.add(project)
        session.commit()
        return jsonify({'success': 'OK'})
