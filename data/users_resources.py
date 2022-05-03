from flask import jsonify
from flask_restful import Resource, abort
from werkzeug.security import generate_password_hash

from data import db_session
from data.users import User
from data.reqparse_user import parser


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    users = session.query(User).get(user_id)
    if not users:
        abort(404, message=f"User {user_id} not found")


def set_password(password):
    return generate_password_hash(password)


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        users = session.query(User).get(user_id)
        return jsonify({'user': users.to_dict(only=('name', 'surname', 'about', 'age',
                                                    'email', 'hashed_password', 'modified_date',
                                                    'user_type'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        args = parser.parse_args()
        user = session.query(User).get(user_id)
        user.name = args['name']
        user.surname = args['surname']
        user.about = args['about']
        user.age = args['age']
        user.email = args['email']
        user.hashed_password = args['hashed_password']
        user.user_type = args['user_type']
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(only=('name', 'surname', 'about', 'age',
                                                     'email', 'hashed_password', 'modified_date',
                                                     'user_type')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            name=args['name'],
            surname=args['surname'],
            about=args['about'],
            age=args['age'],
            email=args['email'],
            hashed_password=set_password(args['hashed_password']),
            user_type=args['user_type']
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
